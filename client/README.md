# GDPR Anonymizer - Frontend Client

Preact + TypeScript frontend for the GDPR Text Anonymization system.

## Features

- **5-Tab Interface**: Original Text, Anonymized Text, Replacements, Risk Assessment, and Insights
- **Real-time Anonymization**: Click "Anonymize" to process text through the backend API
- **Validation Feedback**: See which identifiers were successfully replaced and any issues
- **Risk Assessment**: View GDPR compliance and risk level analysis
- **Workflow Insights**: See LLM provider, model, iterations, and confidence scores

## Prerequisites

- Node.js 18+ (LTS)
- npm 9+ or pnpm 8+
- Backend API running on `http://localhost:8000`

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. The app will be available at: `http://localhost:5173`

## Development

### Project Structure

```
client/
├── src/
│   ├── components/
│   │   ├── primitives/      # Basic UI elements (Button, Textarea, Tabs)
│   │   └── presenters/      # Display components (5 tab views)
│   ├── services/
│   │   └── api.ts           # API client for /api/v1/anonymize
│   ├── store/
│   │   └── anonymization.ts # Global state with @preact/signals
│   ├── app.tsx              # Main component
│   ├── main.tsx             # Entry point
│   └── style.css            # Global styles
├── index.html
├── package.json
├── vite.config.ts           # Vite config with API proxy
└── tsconfig.json
```

### Running the Application

**Terminal 1 - Backend** (from project root):
```bash
cd server
source venv_python3/bin/activate
python run_api.py
```

**Terminal 2 - Frontend** (from project root):
```bash
cd client
npm run dev
```

### Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

## API Integration

The frontend connects to the backend API via Vite proxy:

- **Development**: `/api/*` → `http://localhost:8000/api/*`
- **Endpoint**: `POST /api/v1/anonymize`

## Architecture

This project follows the Preact architecture guidelines:

- **Primitives**: Reusable UI components (Button, Textarea, Tabs)
- **Presenters**: Pure display components (5 tab views)
- **Signals**: Global state management with `@preact/signals`
- **Services**: API communication layer

## Testing

### Manual Testing

1. Start both backend and frontend servers
2. Open `http://localhost:5173`
3. Enter text with PII (e.g., "Contact John Smith at john@example.com")
4. Click "Anonymize"
5. Switch between the 5 tabs to see results

### Expected Behavior

- **Original Text**: Shows your input
- **Anonymized Text**: Shows processed text with placeholders
- **Replacements**: Shows mapping table and validation issues (if any)
- **Risk Assessment**: Shows GDPR compliance and risk level
- **Insights**: Shows LLM provider, model, iterations, and confidence scores

## Troubleshooting

### Backend Not Available

If you see "API error" or network errors:

1. Ensure backend is running: `cd server && python run_api.py`
2. Check backend is on port 8000: `curl http://localhost:8000/health`
3. Check browser console for CORS errors

### Build Errors

```bash
npm run build
```

Should complete without TypeScript errors. If you see errors, check:
- All imports are correct
- TypeScript types match the API response

## Technology Stack

- **Preact**: Lightweight React alternative
- **TypeScript**: Type safety
- **Vite**: Fast build tool and dev server
- **@preact/signals**: Reactive state management

## Iteration 5 - Completed Features

✅ Text input with textarea
✅ Five-tab navigation
✅ API integration with backend
✅ Loading states and error handling
✅ Replacements view with validation issues
✅ Risk assessment display
✅ Insights view with LLM metadata
✅ Responsive design (desktop/tablet)
✅ REST API versioning (/api/v1/*)

## Future Iterations

- File upload functionality
- Configuration panel
- Anonymization history
- Export results (JSON, CSV, PDF)
- Batch processing
- Dark mode
