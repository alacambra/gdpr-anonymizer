# Iteration Package 5: Basic Preact UI

## Document Control

**Version**: 2.0
**Date**: 2025-10-10
**Status**: Active (UPDATED)
**Dependencies**: Iteration 1-4 (Complete), Backend API (src/ directory)
**Target**: Frontend developer with Preact/TypeScript experience

---

## 1. Iteration Overview

### 1.1 Purpose

Implement a minimal working Preact frontend that allows users to:
1. Input original text
2. View anonymized text (received from backend API)
3. View replacements and validation results
4. View risk assessment (received from backend API)
5. View workflow insights (LLM info, iterations, etc.)

This iteration establishes the foundation for the UI layer following the repackaging structure (client/ directory) and reorganizes the backend into server/ directory.

### 1.2 Business Value

- Users can interact with the anonymization system via web browser
- No command-line knowledge required
- Visual feedback improves user experience
- Transparency into anonymization process (replacements, validation)
- Clear project structure (client/ + server/ separation)
- Foundation for future iterations (file upload, configuration, etc.)

### 1.3 Success Criteria

✅ User can enter text in a textarea
✅ Five tabs are visible: Original, Anonymized, Replacements, Risk, Insights
✅ UI calls backend API `/api/v1/anonymize` (REST API versioning in place)
✅ Application follows Preact architecture guidelines
✅ Clean separation: client/ (frontend) and server/ (backend)
✅ Backend moved to server/ directory structure

---

## 2. Requirements Implemented

This iteration implements the following requirements:

### From Architectural Requirements (REQ-A-090)

**REQ-A-090** (Partial): Web UI (React/Vue frontend)
- **Scope in this iteration**: Basic Preact UI with five tabs
- **Out of scope**: Advanced features (file upload, configuration panel, history)

### New Functional Requirements

**REQ-F-UI-001**: The UI SHALL provide a text input area for original text
- Multiline textarea
- Minimum height: 200px
- Placeholder text: "Enter text to anonymize..."

**REQ-F-UI-002**: The UI SHALL display five tabs
- Tab 1: "Original Text" - displays user input
- Tab 2: "Anonymized Text" - displays API response (anonymized_text)
- Tab 3: "Replacements" - displays mappings and validation issues
- Tab 4: "Risk Assessment" - displays risk analysis
- Tab 5: "Insights" - displays LLM provider, model, iterations, workflow info

**REQ-F-UI-003**: The UI SHALL maintain state across tab switches
- Switching tabs does not lose data
- Last viewed tab is highlighted

**REQ-F-UI-004**: The UI SHALL trigger anonymization when user submits
- Button labeled "Anonymize"
- Disabled during processing
- Shows loading state

**REQ-F-UI-005**: The Replacements tab SHALL display
- All mappings (original → placeholder)
- Validation issues (if any)
- Visual distinction between successful replacements and missed identifiers

**REQ-F-UI-006**: The Insights tab SHALL display
- LLM provider and model used
- Number of iterations performed
- Success status
- Validation confidence score
- Risk assessment confidence score

### New Non-Functional Requirements

**REQ-NF-UI-001**: The UI SHALL load in <2 seconds on modern browsers

**REQ-NF-UI-002**: The UI SHALL be responsive (desktop and tablet)
- Minimum width: 768px (tablet)
- Desktop-first design

**REQ-NF-UI-003**: The UI SHALL follow accessibility basics
- Semantic HTML
- Keyboard navigation support
- ARIA labels where appropriate

**REQ-NF-API-001**: The backend API SHALL use versioned endpoints
- Pattern: `/api/v1/*`
- Allows future API evolution without breaking clients
- Example: `/api/v1/anonymize`

### New Structural Requirements

**REQ-S-001**: Backend SHALL be organized in `server/` directory
- Move existing `src/` Python code to `server/src/`
- Move `run_api.py` to `server/run_api.py`
- Maintain existing package structure within server/

**REQ-S-002**: Frontend SHALL be organized in `client/` directory
- All Preact/TypeScript code in client/
- Separate package.json and dependencies
- Independent build/dev process

---

## 3. Architecture & Design

### 3.1 Directory Structure

**UPDATED** - Following the repackaging structure:

```
gdpr-anonymizer/
├── client/                     # NEW - Preact frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── primitives/     # Basic UI elements
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Textarea.tsx
│   │   │   │   └── Tabs.tsx
│   │   │   └── presenters/     # Display components
│   │   │       ├── OriginalText.tsx
│   │   │       ├── AnonymizedText.tsx
│   │   │       ├── ReplacementsView.tsx      # NEW
│   │   │       ├── RiskAssessment.tsx
│   │   │       └── InsightsView.tsx          # NEW
│   │   ├── services/
│   │   │   └── api.ts          # API client for /api/v1/anonymize
│   │   ├── store/
│   │   │   └── anonymization.ts # Global signals
│   │   ├── App.tsx             # Main component
│   │   ├── main.tsx            # Entry point
│   │   └── style.css           # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── server/                     # MOVED - Python backend
    ├── src/
    │   └── anonymization/      # Existing code moved here
    │       ├── domain/
    │       ├── infrastructure/
    │       ├── application/
    │       └── interfaces/
    │           └── rest/
    │               ├── routers/
    │               │   ├── anonymization.py
    │               │   └── health.py
    │               └── main.py
    ├── run_api.py              # Moved from root
    ├── requirements.txt
    └── README.md
```

### 3.2 Component Architecture

Following `preact-architecture-guide.md`:

#### Primitives (Basic UI)
- **Button**: Reusable button component
- **Textarea**: Styled textarea component
- **Tabs**: Tab navigation component (5 tabs)

#### Presenters (Pure Display)
- **OriginalText**: Displays user input
- **AnonymizedText**: Displays anonymized result
- **ReplacementsView**: Displays mappings + validation issues (NEW)
- **RiskAssessment**: Displays risk analysis
- **InsightsView**: Displays LLM/workflow metadata (NEW)

#### State Management
- Use **@preact/signals** for global state
- Local state (useState) for UI-only state (active tab)

### 3.3 Data Flow

```
User Input (Textarea)
    ↓
[Anonymize Button Click]
    ↓
API Call (/api/v1/anonymize) ← api.ts service
    ↓
Update Signals (store/anonymization.ts)
    ↓
Re-render Tabs (AnonymizedText, Replacements, Risk, Insights)
```

### 3.4 API Contract

**UPDATED** - Matches actual backend implementation

**Endpoint**: `POST /api/v1/anonymize`

**Request**:
```typescript
{
  text: string,
  document_id?: string
}
```

**Response** (actual backend schema):
```typescript
{
  document_id?: string,
  anonymized_text: string,
  mappings: Record<string, string>,
  validation: {
    passed: boolean,
    issues: Array<{
      identifier_type: string,
      value: string,
      context: string,
      location_hint: string
    }>,
    reasoning: string,
    confidence: number
  },
  risk_assessment: {
    overall_score: number,
    risk_level: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "NEGLIGIBLE",
    gdpr_compliant: boolean,
    confidence: number,
    reasoning: string,
    assessment_date: string  // ISO datetime
  },
  iterations: number,
  success: boolean,
  llm_provider: string,
  llm_model: string
}
```

**Note**: Backend API must be running for manual testing. Component tests use mock data.

---

## 4. Interface Specifications

### 4.1 Component Interfaces

#### App.tsx (Main Container)

```typescript
// Main application component
export function App() {
  const [activeTab, setActiveTab] = useState('original');

  return (
    <div className="app">
      <header>
        <h1>GDPR Text Anonymization</h1>
      </header>
      <main>
        <InputSection />
        <Tabs activeTab={activeTab} onTabChange={setActiveTab} />
        <TabContent activeTab={activeTab} />
      </main>
    </div>
  );
}
```

#### Tabs.tsx (Primitive)

```typescript
interface TabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function Tabs({ activeTab, onTabChange }: TabsProps) {
  const tabs = [
    { id: 'original', label: 'Original Text' },
    { id: 'anonymized', label: 'Anonymized Text' },
    { id: 'replacements', label: 'Replacements' },
    { id: 'risk', label: 'Risk Assessment' },
    { id: 'insights', label: 'Insights' }
  ];

  return (
    <div className="tabs">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={activeTab === tab.id ? 'active' : ''}
          onClick={() => onTabChange(tab.id)}
          aria-selected={activeTab === tab.id}
          role="tab"
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

#### api.ts (Service)

```typescript
export interface AnonymizeRequest {
  text: string;
  document_id?: string;
}

export interface ValidationIssue {
  identifier_type: string;
  value: string;
  context: string;
  location_hint: string;
}

export interface ValidationResult {
  passed: boolean;
  issues: ValidationIssue[];
  reasoning: string;
  confidence: number;
}

export interface RiskAssessment {
  overall_score: number;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'NEGLIGIBLE';
  gdpr_compliant: boolean;
  confidence: number;
  reasoning: string;
  assessment_date: string;
}

export interface AnonymizeResponse {
  document_id?: string;
  anonymized_text: string;
  mappings: Record<string, string>;
  validation: ValidationResult;
  risk_assessment: RiskAssessment;
  iterations: number;
  success: boolean;
  llm_provider: string;
  llm_model: string;
}

export async function anonymizeText(
  text: string,
  documentId?: string
): Promise<AnonymizeResponse> {
  const response = await fetch('/api/v1/anonymize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      document_id: documentId
    })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.detail || `API error: ${response.status}`
    );
  }

  return response.json();
}
```

#### store/anonymization.ts (Signals)

```typescript
import { signal } from '@preact/signals';
import type { AnonymizeResponse } from '../services/api';

export const originalText = signal('');
export const isLoading = signal(false);
export const error = signal<string | null>(null);
export const result = signal<AnonymizeResponse | null>(null);

// Helper computed signals
export const hasValidationIssues = computed(() =>
  result.value?.validation.issues.length ?? 0 > 0
);

export const isSuccessful = computed(() =>
  result.value?.success ?? false
);
```

#### ReplacementsView.tsx (NEW Presenter)

```typescript
interface ReplacementsViewProps {
  mappings: Record<string, string>;
  validationIssues: ValidationIssue[];
  validationPassed: boolean;
}

export function ReplacementsView({
  mappings,
  validationIssues,
  validationPassed
}: ReplacementsViewProps) {
  const mappingEntries = Object.entries(mappings);

  return (
    <div className="replacements-view">
      <section className="mappings">
        <h3>Replacements Performed</h3>
        {mappingEntries.length === 0 ? (
          <p className="empty-state">No replacements were made.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Original</th>
                <th>Replacement</th>
              </tr>
            </thead>
            <tbody>
              {mappingEntries.map(([original, replacement]) => (
                <tr key={original}>
                  <td className="original">{original}</td>
                  <td className="replacement">{replacement}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {!validationPassed && validationIssues.length > 0 && (
        <section className="validation-issues">
          <h3 className="warning">⚠️ Validation Issues Found</h3>
          <p>The following identifiers were detected but not anonymized:</p>
          <ul>
            {validationIssues.map((issue, idx) => (
              <li key={idx} className="issue-item">
                <strong>{issue.identifier_type}:</strong> {issue.value}
                <br />
                <span className="context">Context: {issue.context}</span>
                <br />
                <span className="hint">Location: {issue.location_hint}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
```

#### InsightsView.tsx (NEW Presenter)

```typescript
interface InsightsViewProps {
  llmProvider: string;
  llmModel: string;
  iterations: number;
  success: boolean;
  validationConfidence: number;
  riskConfidence: number;
}

export function InsightsView({
  llmProvider,
  llmModel,
  iterations,
  success,
  validationConfidence,
  riskConfidence
}: InsightsViewProps) {
  return (
    <div className="insights-view">
      <section className="workflow-info">
        <h3>Workflow Information</h3>
        <dl>
          <dt>Status</dt>
          <dd className={success ? 'success' : 'failure'}>
            {success ? '✓ Success' : '✗ Failed'}
          </dd>

          <dt>Iterations</dt>
          <dd>{iterations}</dd>

          <dt>LLM Provider</dt>
          <dd>{llmProvider}</dd>

          <dt>LLM Model</dt>
          <dd>{llmModel}</dd>
        </dl>
      </section>

      <section className="confidence-scores">
        <h3>Confidence Scores</h3>
        <dl>
          <dt>Validation Confidence</dt>
          <dd>
            <meter
              value={validationConfidence}
              min="0"
              max="1"
              optimum="1"
            >
              {(validationConfidence * 100).toFixed(0)}%
            </meter>
            <span>{(validationConfidence * 100).toFixed(1)}%</span>
          </dd>

          <dt>Risk Assessment Confidence</dt>
          <dd>
            <meter
              value={riskConfidence}
              min="0"
              max="1"
              optimum="1"
            >
              {(riskConfidence * 100).toFixed(0)}%
            </meter>
            <span>{(riskConfidence * 100).toFixed(1)}%</span>
          </dd>
        </dl>
      </section>
    </div>
  );
}
```

---

## 5. Behavioral Requirements

### 5.1 User Flow

**Step 1: Initial State**
- User sees empty textarea with placeholder
- All five tabs visible
- "Original Text" tab is active
- "Anonymize" button is enabled

**Step 2: User Enters Text**
- User types text in textarea
- Text updates `originalText` signal
- "Original Text" tab shows live preview

**Step 3: User Clicks "Anonymize"**
- Button becomes disabled
- Loading spinner appears
- API call initiated via `api.anonymizeText()`
- If API unavailable: show error message
- If API succeeds: update `result` signal

**Step 4: Results Display**
- "Anonymized Text" tab shows `anonymized_text`
- "Replacements" tab shows `mappings` and `validation.issues`
- "Risk Assessment" tab shows `risk_assessment`
- "Insights" tab shows workflow metadata
- User can switch between tabs
- User can edit original text and re-anonymize

### 5.2 Error Handling

**Scenario 1: API Not Available**
- Show message: "Backend API not available. Please ensure server is running."
- Show command: `cd server && python run_api.py`
- Disable "Anonymize" button
- Show retry option

**Scenario 2: Validation Failed (validation.passed = false)**
- Show successful anonymization in "Anonymized Text" tab
- Highlight "Replacements" tab with warning indicator
- Display validation issues clearly
- Allow user to review and decide next action

**Scenario 3: API Returns Error**
- Parse error.detail from response
- Show user-friendly error message
- Keep original text
- Allow user to retry

**Scenario 4: Network Error**
- Show message: "Network error. Please check connection."
- Allow retry

### 5.3 Loading States

**During API Call**:
- "Anonymize" button: disabled, shows spinner
- Tabs: remain accessible but show previous data
- No automatic tab switch

**After API Response**:
- "Anonymize" button: re-enabled
- Tabs: updated with new data
- Optional: auto-switch to "Anonymized Text" tab if successful
- Optional: auto-switch to "Replacements" tab if validation failed

---

## 6. Quality Criteria

### 6.1 Code Quality

✅ All components have TypeScript interfaces
✅ Presenter components are pure (props-only)
✅ No `localStorage` or `sessionStorage` usage
✅ Follows Preact architecture guidelines
✅ Code is formatted with Prettier
✅ Linting passes (ESLint)

### 6.2 Testing Strategy

**Component Testing** (No Backend Required):
- Use mock data for AnonymizeResponse
- Test each presenter component in isolation
- Test tab switching behavior
- Test loading states

**Manual Testing** (Backend Required):
- Backend must be running: `cd server && python run_api.py`
- Can use VS Code Tasks & Launch for convenience
- Test full user flow with real API
- Test error scenarios (stop backend, invalid input)

**Out of Scope**:
- E2E testing with LLM integration (future iteration)
- Automated integration tests (future iteration)

**Manual Test Cases**:
1. Enter text → verify it appears in "Original Text" tab
2. Click "Anonymize" → verify loading state
3. Switch tabs → verify data persists
4. Check "Replacements" tab → verify mappings displayed
5. Check "Insights" tab → verify LLM info displayed
6. Test with validation failures → verify issues shown
7. Test with API unavailable → verify error message

### 6.3 Performance Targets

- Initial load: <2 seconds
- Tab switch: <100ms
- Text input lag: <50ms

---

## 7. Implementation Guidance

### 7.1 Setup Steps

**Step 0: Backend Reorganization**
```bash
# Create server directory
mkdir -p server

# Move backend files
mv src server/
mv run_api.py server/
cp requirements.txt server/  # or move if no root requirements.txt

# Update imports if needed (paths should still work)
```

**Terminal 1: Backend**
```bash
cd server
python run_api.py  # Runs on :8000
# API available at http://localhost:8000/api/v1/anonymize
```

**Terminal 2: Frontend**
```bash
cd client
npm create vite@latest . -- --template preact-ts
npm install @preact/signals
npm run dev  # Runs on :5173
```

### 7.2 Vite Configuration

**client/vite.config.ts**:
```typescript
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});
```

### 7.3 Development Order

**Phase 0: Backend Reorganization** (30 min)
1. Create server/ directory
2. Move Python code to server/src/
3. Move run_api.py to server/
4. Test backend still works
5. Update any paths if needed

**Phase 1: Frontend Setup** (30 min)
1. Initialize Vite + Preact + TypeScript
2. Install @preact/signals
3. Configure Vite proxy
4. Create directory structure

**Phase 2: Primitives** (1 hour)
1. Implement Button component
2. Implement Textarea component
3. Implement Tabs component (5 tabs)
4. Add basic styles

**Phase 3: Services** (30 min)
1. Implement api.ts service (updated types)
2. Create store/anonymization.ts signals
3. Add error handling

**Phase 4: Presenters** (1.5 hours)
1. Implement OriginalText presenter
2. Implement AnonymizedText presenter
3. Implement ReplacementsView presenter (NEW)
4. Implement RiskAssessment presenter
5. Implement InsightsView presenter (NEW)

**Phase 5: Integration** (1 hour)
1. Build App.tsx main component
2. Wire up state management
3. Test user flow
4. Handle edge cases

**Total Estimated Time**: 5.5 hours (including backend reorganization)

---

## 8. Scope Boundaries

### 8.1 IN SCOPE

✅ Five-tab UI (Original, Anonymized, Replacements, Risk, Insights)
✅ Text input for original text
✅ API call to `/api/v1/anonymize`
✅ Display anonymized text
✅ Display mappings and validation issues (NEW)
✅ Display risk assessment
✅ Display workflow insights (NEW)
✅ Error handling (basic)
✅ Loading states
✅ Responsive design (desktop/tablet)
✅ Backend reorganization into server/ directory (NEW)
✅ REST API versioning (/api/v1/*) (NEW)

### 8.2 OUT OF SCOPE

❌ File upload functionality
❌ Configuration panel
❌ Anonymization history
❌ User authentication
❌ Automated E2E tests with LLM
❌ Mobile optimization (<768px)
❌ Dark mode
❌ Export functionality
❌ Advanced error recovery
❌ Real-time collaboration

---

## 9. Acceptance Criteria

### 9.1 Functional Acceptance

1. ✅ User can enter text in textarea
2. ✅ Five tabs are visible and labeled correctly
3. ✅ "Original Text" tab shows user input
4. ✅ "Anonymized Text" tab shows result (when available)
5. ✅ "Replacements" tab shows mappings and validation issues (NEW)
6. ✅ "Risk Assessment" tab shows risk analysis (when available)
7. ✅ "Insights" tab shows LLM/workflow info (NEW)
8. ✅ Clicking "Anonymize" triggers API call to `/api/v1/anonymize`
9. ✅ Loading state displays during API call
10. ✅ Error message displays when API unavailable
11. ✅ Tab switching preserves data
12. ✅ UI is responsive on desktop (>1024px) and tablet (768px)
13. ✅ Validation issues are clearly displayed when present
14. ✅ Backend is organized in server/ directory

### 9.2 Technical Acceptance

1. ✅ TypeScript compiles without errors
2. ✅ ESLint passes with no errors
3. ✅ Components follow Preact architecture guidelines
4. ✅ No use of `localStorage` or `sessionStorage`
5. ✅ API service properly typed (matches backend schema)
6. ✅ Signals used for global state
7. ✅ Vite dev server runs without errors
8. ✅ Code is formatted consistently
9. ✅ REST API uses versioned endpoints (/api/v1/*)
10. ✅ Backend imports still work after reorganization

### 9.3 UX Acceptance

1. ✅ UI loads in <2 seconds
2. ✅ Tab switches feel instant (<100ms)
3. ✅ Text input has no lag
4. ✅ Button states are clear (enabled/disabled/loading)
5. ✅ Error messages are user-friendly
6. ✅ Validation issues are visually distinct from successful replacements

---

## 10. Deliverables

### 10.1 Backend Reorganization

**Updated structure**:
```
server/
├── src/anonymization/    # All existing Python code
├── run_api.py            # Moved from root
├── requirements.txt
└── README.md             # Setup instructions
```

### 10.2 Frontend Code Files

Required files in `client/`:
- `src/components/primitives/Button.tsx`
- `src/components/primitives/Textarea.tsx`
- `src/components/primitives/Tabs.tsx`
- `src/components/presenters/OriginalText.tsx`
- `src/components/presenters/AnonymizedText.tsx`
- `src/components/presenters/ReplacementsView.tsx` (NEW)
- `src/components/presenters/RiskAssessment.tsx`
- `src/components/presenters/InsightsView.tsx` (NEW)
- `src/services/api.ts` (UPDATED types)
- `src/store/anonymization.ts`
- `src/App.tsx`
- `src/main.tsx`
- `src/style.css`
- `index.html`
- `package.json`
- `vite.config.ts`
- `tsconfig.json`

### 10.3 Documentation

- README.md in `client/` directory with:
  - Setup instructions
  - Development workflow
  - Testing instructions
- README.md in `server/` directory with:
  - API documentation
  - Running instructions

---

## 11. Dependencies

### 11.1 Technical Dependencies

**Required**:
- Python 3.10+ (backend)
- Node.js 18+ (LTS)
- npm 9+ or pnpm 8+
- Modern browser (Chrome 90+, Firefox 88+, Safari 14+)

**npm Packages**:
```json
{
  "dependencies": {
    "preact": "^10.19.0",
    "@preact/signals": "^1.2.0"
  },
  "devDependencies": {
    "@preact/preset-vite": "^2.7.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### 11.2 Iteration Dependencies

**Depends On**:
- Iteration 1-4: Complete (provides working API)
- Backend API: Must implement actual response schema

**Blocks**:
- None (frontend and backend can be developed in parallel)

---

## 12. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Backend reorganization breaks imports | MEDIUM | HIGH | Test thoroughly; update imports systematically; use relative imports |
| API schema mismatch | LOW | HIGH | Use actual backend types; validate with Postman/curl first |
| Preact signals learning curve | MEDIUM | LOW | Provide examples; signals are simple for this use case |
| Responsive design complexity | LOW | LOW | Desktop-first approach; minimal responsive requirements |
| State management confusion | LOW | MEDIUM | Clear separation: signals for global, useState for local |
| 5 tabs increase complexity | LOW | MEDIUM | Follow component patterns consistently; test thoroughly |

---

## 13. Testing Strategy

### 13.1 Component Testing (No Backend Required)

**Mock Data Setup**:
```typescript
// test/fixtures/mockResponse.ts
export const mockSuccessResponse: AnonymizeResponse = {
  document_id: 'test-doc-1',
  anonymized_text: 'Contact [NAME_1] at [EMAIL_1]',
  mappings: {
    'John Smith': '[NAME_1]',
    'john@example.com': '[EMAIL_1]'
  },
  validation: {
    passed: true,
    issues: [],
    reasoning: 'All identifiers properly anonymized',
    confidence: 0.95
  },
  risk_assessment: {
    overall_score: 92,
    risk_level: 'LOW',
    gdpr_compliant: true,
    confidence: 0.9,
    reasoning: 'All PII removed',
    assessment_date: '2025-10-10T12:00:00Z'
  },
  iterations: 1,
  success: true,
  llm_provider: 'claude',
  llm_model: 'claude-3-5-sonnet-20241022'
};

export const mockValidationFailure: AnonymizeResponse = {
  ...mockSuccessResponse,
  validation: {
    passed: false,
    issues: [
      {
        identifier_type: 'EMAIL',
        value: 'hidden@example.com',
        context: 'found in signature',
        location_hint: 'line 15'
      }
    ],
    reasoning: 'One email address not anonymized',
    confidence: 0.85
  }
};
```

**Test Cases**:
```typescript
describe('ReplacementsView', () => {
  it('displays all mappings', () => {
    render(
      <ReplacementsView
        mappings={mockSuccessResponse.mappings}
        validationIssues={[]}
        validationPassed={true}
      />
    );
    expect(screen.getByText('John Smith')).toBeInTheDocument();
    expect(screen.getByText('[NAME_1]')).toBeInTheDocument();
  });

  it('shows validation issues when present', () => {
    const issues = mockValidationFailure.validation.issues;
    render(
      <ReplacementsView
        mappings={{}}
        validationIssues={issues}
        validationPassed={false}
      />
    );
    expect(screen.getByText(/Validation Issues Found/i)).toBeInTheDocument();
    expect(screen.getByText('hidden@example.com')).toBeInTheDocument();
  });
});
```

### 13.2 Manual Testing Checklist (Backend Required)

**Prerequisites**:
- Backend running: `cd server && python run_api.py`
- Frontend running: `cd client && npm run dev`
- Open http://localhost:5173

**Test Case 1: Basic Text Input**
- [ ] Open app in browser
- [ ] Type text in textarea
- [ ] Verify text appears in "Original Text" tab
- [ ] Switch to other tabs → verify empty state or previous data
- [ ] Switch back to "Original Text" → verify text persists

**Test Case 2: Successful Anonymization**
- [ ] Enter sample text: "Contact John Smith at john@example.com"
- [ ] Click "Anonymize" button
- [ ] Verify button becomes disabled
- [ ] Verify loading indicator appears
- [ ] Wait for response
- [ ] Verify "Anonymized Text" tab shows result
- [ ] Verify "Replacements" tab shows mappings table
- [ ] Verify "Risk Assessment" tab shows risk level
- [ ] Verify "Insights" tab shows LLM info

**Test Case 3: Tab Navigation**
- [ ] Switch between all five tabs
- [ ] Verify active tab is highlighted
- [ ] Verify tab content matches tab name
- [ ] Verify no data loss during navigation

**Test Case 4: Validation Failure Scenario**
- [ ] Enter text with intentionally complex PII
- [ ] Anonymize
- [ ] Check if validation.passed === false
- [ ] Verify "Replacements" tab shows warning
- [ ] Verify validation issues are displayed clearly

**Test Case 5: Error Handling**
- [ ] Stop backend (Ctrl+C)
- [ ] Try to anonymize
- [ ] Verify error message: "Backend API not available..."
- [ ] Verify helpful command shown
- [ ] Verify button remains enabled for retry

**Test Case 6: Responsive Design**
- [ ] Resize browser to 1920px width
- [ ] Verify layout looks good
- [ ] Resize to 768px width
- [ ] Verify layout adapts appropriately
- [ ] Verify all five tabs are still accessible

### 13.3 Future Testing

Automated tests will be added in a future iteration:
- Unit tests for all components (Vitest + Testing Library)
- Integration tests for API calls with mock server
- E2E tests for user flows (Playwright)
- LLM integration tests (when testing infrastructure ready)

---

## 14. Transition to Next Iteration

### 14.1 Foundation for Iteration 6

This iteration establishes:
- ✅ Complete UI architecture
- ✅ Component structure (5 tabs)
- ✅ State management pattern
- ✅ API service layer with proper typing
- ✅ Clear project structure (client/ + server/)
- ✅ REST API versioning

**Iteration 6** can build on this by adding:
- File upload functionality
- Configuration panel
- Anonymization history
- Advanced error handling
- Export functionality (download results)
- Batch processing UI

### 14.2 Open Questions for Iteration 6

1. Should file upload support multiple formats? (txt, docx, pdf?)
2. What configuration options should be exposed in UI?
3. Should anonymization history persist across sessions?
4. What export formats should be supported? (JSON, CSV, PDF?)
5. Should batch processing show progress for each document?

---

## 15. Definition of Done

### 15.1 Backend Reorganization Complete

- [ ] Backend code moved to server/src/
- [ ] run_api.py moved to server/
- [ ] API still runs successfully from server/
- [ ] All imports work correctly
- [ ] README.md updated with new paths

### 15.2 Code Complete

- [ ] All components implemented per specifications
- [ ] Five tabs working correctly
- [ ] TypeScript compiles without errors
- [ ] No ESLint errors
- [ ] Code formatted with Prettier
- [ ] Vite dev server runs successfully

### 15.3 Functionality Complete

- [ ] User can input text
- [ ] Five tabs display correctly
- [ ] API service makes requests to `/api/v1/anonymize`
- [ ] All response fields displayed appropriately
- [ ] Loading states work
- [ ] Error messages display appropriately
- [ ] Tab switching preserves state
- [ ] Validation issues shown in Replacements tab
- [ ] Insights tab shows workflow metadata

### 15.4 Documentation Complete

- [ ] README.md in client/ directory
- [ ] README.md in server/ directory
- [ ] Setup instructions verified
- [ ] Code comments added where needed
- [ ] API contract documented

### 15.5 Testing Complete

- [ ] All component tests pass (with mock data)
- [ ] All manual test cases passed
- [ ] Edge cases tested
- [ ] Responsive design verified
- [ ] No console errors
- [ ] Backend runs successfully from new location

---

## 16. Handoff Checklist

### 16.1 Architect Validation

- [ ] Architecture follows preact-architecture-guide.md
- [ ] Component classification is correct (primitives vs presenters)
- [ ] State management uses signals appropriately
- [ ] No over-prescription (tech lead has implementation freedom)
- [ ] Interface contracts are clear and match backend
- [ ] API versioning requirement documented

### 16.2 Tech Lead Review

- [ ] Requirements are clear and actionable
- [ ] Sufficient detail to begin implementation
- [ ] Development order makes sense
- [ ] Estimated time is realistic (5.5 hours)
- [ ] Integration points with backend are clear
- [ ] Backend reorganization steps are clear

### 16.3 Developer Handoff

- [ ] Document delivered
- [ ] Example code provided
- [ ] Backend reorganization strategy clear
- [ ] Questions channel established
- [ ] Architect available for clarifications

---

## 17. Revision History

| Version | Date       | Changes                                           | Author    |
|---------|------------|---------------------------------------------------|-----------|
| 1.0     | 2025-10-10 | Initial iteration package                         | Architect |
| 2.0     | 2025-10-10 | Updated: API contract, 5 tabs, server/ structure, versioning | Architect |

---

## 18. Summary of Changes (v1.0 → v2.0)

### Major Changes

1. **API Contract Updated**: Now matches actual backend schema (snake_case, all fields)
2. **API Versioning**: All endpoints use `/api/v1/*` pattern
3. **5 Tabs Instead of 3**:
   - Added "Replacements" tab (mappings + validation issues)
   - Added "Insights" tab (LLM info + workflow metadata)
4. **Backend Reorganization**: Move all Python code to `server/` directory
5. **Enhanced Error Handling**: Better coverage of validation failures and partial success
6. **Testing Strategy**: Clear separation between component tests (mock) and manual tests (real backend)

### New Components

- `ReplacementsView.tsx`: Display mappings and validation issues
- `InsightsView.tsx`: Display workflow metadata

### Updated Types

- Complete TypeScript interfaces matching backend
- Added `ValidationIssue`, `ValidationResult` types
- Enhanced `AnonymizeResponse` with all backend fields

---

**END OF ITERATION PACKAGE 5 (v2.0)**

**Status**: READY FOR IMPLEMENTATION
**Estimated Effort**: 5.5 hours
**Next Iteration**: Advanced UI Features (File Upload, Configuration, History)
