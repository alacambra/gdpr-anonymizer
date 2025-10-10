#!/usr/bin/env python3
"""Run the GDPR Anonymizer API server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "anonymization.interfaces.rest.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
