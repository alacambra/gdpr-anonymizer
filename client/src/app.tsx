import { useState } from 'preact/hooks';
import { Textarea } from './components/primitives/Textarea';
import { Button } from './components/primitives/Button';
import { Tabs, type TabId } from './components/primitives/Tabs';
import { OriginalText } from './components/presenters/OriginalText';
import { AnonymizedText } from './components/presenters/AnonymizedText';
import { ReplacementsView } from './components/presenters/ReplacementsView';
import { RiskAssessment } from './components/presenters/RiskAssessment';
import { InsightsView } from './components/presenters/InsightsView';
import { originalText, isLoading, error, result } from './store/anonymization';
import { anonymizeText } from './services/api';
import './style.css';

export function App() {
  const [activeTab, setActiveTab] = useState<TabId>('original');

  const handleAnonymize = async () => {
    if (!originalText.value.trim()) {
      error.value = 'Please enter some text to anonymize';
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await anonymizeText(originalText.value);
      result.value = response;
      // Optionally switch to anonymized tab on success
      setActiveTab('anonymized');
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred';
      console.error('Anonymization error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'original':
        return <OriginalText text={originalText.value} />;

      case 'anonymized':
        return <AnonymizedText text={result.value?.anonymized_text ?? null} />;

      case 'replacements':
        return (
          <ReplacementsView
            mappings={result.value?.mappings ?? null}
            validationIssues={result.value?.validation.issues ?? []}
            validationPassed={result.value?.validation.passed ?? true}
          />
        );

      case 'risk':
        return <RiskAssessment assessment={result.value?.risk_assessment ?? null} />;

      case 'insights':
        return (
          <InsightsView
            llmProvider={result.value?.llm_provider ?? null}
            llmModel={result.value?.llm_model ?? null}
            iterations={result.value?.iterations ?? null}
            success={result.value?.success ?? null}
            validationConfidence={result.value?.validation.confidence ?? null}
            riskConfidence={result.value?.risk_assessment.confidence ?? null}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="app">
      <header>
        <h1>GDPR Text Anonymization</h1>
        <p className="subtitle">Anonymize personal identifiable information using AI</p>
      </header>

      <main>
        <section className="input-section">
          <label htmlFor="input-text">
            <h2>Enter Text to Anonymize</h2>
          </label>
          <Textarea
            value={originalText.value}
            onChange={(value) => { originalText.value = value; }}
            placeholder="Enter text to anonymize..."
            rows={8}
            disabled={isLoading.value}
          />

          <div className="actions">
            <Button
              onClick={handleAnonymize}
              loading={isLoading.value}
              disabled={isLoading.value}
            >
              Anonymize
            </Button>
          </div>

          {error.value && (
            <div className="error-message" role="alert">
              <strong>Error:</strong> {error.value}
            </div>
          )}
        </section>

        <section className="results-section">
          <Tabs activeTab={activeTab} onTabChange={setActiveTab} />
          <div className="tab-content">
            {renderTabContent()}
          </div>
        </section>
      </main>

      <footer>
        <p>GDPR Anonymizer - Iteration 5</p>
      </footer>
    </div>
  );
}
