"""Anonymization API router."""

from datetime import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_orchestrator, get_config
from ..schemas import (
    AnonymizeRequest,
    AnonymizeResponse,
    BatchAnonymizeRequest,
    BatchAnonymizeResponse,
    ValidationIssueResponse,
    ValidationResponse,
    RiskAssessmentResponse
)
from ....application.orchestrator import AnonymizationOrchestrator, AnonymizationResult
from ....application.config import AppConfig
from ....domain.models import Document

router = APIRouter(prefix="/api/v1", tags=["anonymization"])


@router.post("/anonymize", response_model=AnonymizeResponse)
async def anonymize_document(
    request: AnonymizeRequest,
    orchestrator: AnonymizationOrchestrator = Depends(get_orchestrator),
    config: AppConfig = Depends(get_config)
) -> AnonymizeResponse:
    """Anonymize a single document.

    Args:
        request: Document to anonymize
        orchestrator: Injected orchestrator instance

    Returns:
        AnonymizeResponse with anonymized text and analysis

    Raises:
        HTTPException: If anonymization fails
    """
    try:
        # Create document
        document = Document(
            content=request.text,
            document_id=request.document_id
        )

        result: AnonymizationResult = await orchestrator.anonymize_document(document)

        validation_issues = [
            ValidationIssueResponse(
                identifier_type=issue.identifier_type,
                value=issue.value,
                context=issue.context,
                location_hint=issue.location_hint
            )
            for issue in result.validation.issues
        ]

        # Build response - return even if validation failed
        return AnonymizeResponse(
            document_id=request.document_id,
            anonymized_text=result.anonymizationMapping.anonymized_text,
            mappings=result.anonymizationMapping.mappings,
            validation=ValidationResponse(
                passed=result.validation.passed,
                issues=validation_issues,
                reasoning=result.validation.reasoning,
                confidence=result.validation.confidence
            ),
            risk_assessment=RiskAssessmentResponse(
                overall_score=result.risk_assessment.overall_score,
                risk_level=result.risk_assessment.risk_level,
                gdpr_compliant=result.risk_assessment.gdpr_compliant,
                confidence=result.risk_assessment.confidence,
                reasoning=result.risk_assessment.reasoning,
                assessment_date=result.risk_assessment.assessment_date
            ),
            iterations=result.iterations,
            success=result.success,
            llm_provider=config.llm.provider,
            llm_model=config.llm.model,
            error=json.dumps(result.anonymizationMapping.skippedEntites)  # No error on success
        )

    except ValueError as e:
        # Parsing/validation error - return 200 OK with success=false and error field
        # UI will show this in an error box
        error_detail = str(e)

        return AnonymizeResponse(
            document_id=request.document_id,
            anonymized_text="",  # Empty when no valid entities found
            mappings={},
            validation=ValidationResponse(
                passed=False,
                issues=[],
                reasoning=f"Parsing error: {error_detail}",
                confidence=0.0
            ),
            risk_assessment=RiskAssessmentResponse(
                overall_score=25,
                risk_level="CRITICAL",
                gdpr_compliant=False,
                confidence=0.0,
                reasoning=f"Cannot assess risk due to parsing failure",
                assessment_date=datetime.now()
            ),
            iterations=0,
            success=False,
            llm_provider=config.llm.provider,
            llm_model=config.llm.model,
            # error=error_detail  # Full error message for UI error box
        )

    except Exception as e:
        # Unexpected errors - return as 500
        error_detail = f"Anonymization failed: {str(e)}"
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/anonymize/batch", response_model=BatchAnonymizeResponse)
async def batch_anonymize(
    request: BatchAnonymizeRequest,
    orchestrator: AnonymizationOrchestrator = Depends(get_orchestrator),
    config: AppConfig = Depends(get_config)
) -> BatchAnonymizeResponse:
    """Anonymize multiple documents.

    Args:
        request: Batch of documents to anonymize
        orchestrator: Injected orchestrator instance

    Returns:
        BatchAnonymizeResponse with results for all documents

    Raises:
        HTTPException: If batch processing fails
    """
    results: List[AnonymizeResponse] = []
    successful = 0
    failed = 0

    for doc_request in request.documents:
        try:
            # Anonymize each document
            response = await anonymize_document(doc_request, orchestrator, config)
            results.append(response)
            successful += 1
        except HTTPException as e:
            # Record failure but continue processing
            failed += 1
            # Create error response
            results.append(
                AnonymizeResponse(
                    document_id=doc_request.document_id,
                    anonymized_text="",
                    mappings={},
                    validation=ValidationResponse(
                        passed=False,
                        issues=[],
                        reasoning=f"Error: {e.detail}",
                        confidence=0.0
                    ),
                    risk_assessment=RiskAssessmentResponse(
                        overall_score=25,
                        risk_level="CRITICAL",
                        gdpr_compliant=False,
                        confidence=0.0,
                        reasoning=f"Processing failed: {e.detail}",
                        assessment_date=None  # type: ignore
                    ),
                    iterations=0,
                    success=False,
                    llm_provider=config.llm.provider,
                    llm_model=config.llm.model
                )
            )

    return BatchAnonymizeResponse(
        results=results,
        total=len(request.documents),
        successful=successful,
        failed=failed
    )
