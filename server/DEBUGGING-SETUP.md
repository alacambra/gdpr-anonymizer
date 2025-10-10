# Debugging Setup Complete ✅

Your GDPR Anonymizer project is now fully configured for debugging in VS Code!

## 📁 What Was Added

### 1. **launch.json** - Debug Configurations
Located: `.vscode/launch.json`

**7 Debug Configurations Available**:

1. ⭐ **FastAPI: Run API Server** - Debug the API with hot reload
2. **FastAPI: Uvicorn (Alternative)** - Alternative API debugging method
3. **Test: Iteration 4 Integration Test** - Debug end-to-end workflow
4. **Debug: Agent 1 (ANON-EXEC)** - Debug entity anonymization
5. **Debug: Orchestrator** - Debug workflow coordination
6. **Python: Current File** - Debug any open Python file
7. **Python: Demo Script (Legacy)** - Debug original demo.py

### 2. **settings.json** - VS Code Project Settings
Located: `.vscode/settings.json`

**Configured**:
- ✅ Python interpreter path (virtual environment)
- ✅ PYTHONPATH for imports
- ✅ Type checking and IntelliSense
- ✅ File associations and exclusions
- ✅ Auto-save settings
- ✅ Editor rulers at 88 and 120 characters

### 3. **api-tests.http** - REST Client Test File
Located: `.vscode/api-tests.http`

**20+ Ready-to-Use API Tests**:
- Health checks
- Single document anonymization
- Batch processing
- Edge cases and error scenarios
- Special formats (international, emails)
- Documentation examples

### 4. **DEBUG-GUIDE.md** - Comprehensive Debugging Guide
Located: `.vscode/DEBUG-GUIDE.md`

**Includes**:
- How to use each debug configuration
- Common debugging scenarios
- Strategic breakpoint placement
- Async debugging tips
- Troubleshooting guide
- Keyboard shortcuts reference

---

## 🚀 Quick Start - Debugging

### Option 1: Debug the API (Most Common)

1. **Open VS Code**
2. **Press F5** or click Run → Start Debugging
3. **Select**: "FastAPI: Run API Server"
4. **Set a breakpoint**:
   - Open `src/anonymization/interfaces/rest/routers/anonymization.py`
   - Click left margin at line 40
5. **Trigger it**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/anonymize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Contact John at john@test.com"}'
   ```

### Option 2: Debug Integration Test

1. **Press F5**
2. **Select**: "Test: Iteration 4 Integration Test"
3. **Watch** the complete workflow execute step by step

### Option 3: Use REST Client (No curl needed!)

1. **Install Extension**: [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
2. **Open**: `.vscode/api-tests.http`
3. **Click**: "Send Request" above any test
4. **View**: Response appears in split window

---

## 🎯 Recommended Workflow

### For API Development:

1. **Start with breakpoint**:
   ```
   src/anonymization/interfaces/rest/routers/anonymization.py:40
   ```

2. **Run**: "FastAPI: Run API Server" (F5)

3. **Test**: Use `.vscode/api-tests.http` or curl

4. **Debug**: Step through with F10/F11

5. **Iterate**: Code changes reload automatically

### For Agent Development:

1. **Set breakpoints in**:
   - `infrastructure/agents/agent1_anon_exec.py`
   - `infrastructure/agents/agent2_direct_check.py`
   - `infrastructure/agents/agent3_risk_assess.py`

2. **Run**: "Test: Iteration 4 Integration Test"

3. **Step through**: Agent logic execution

### For Orchestration Logic:

1. **Breakpoint at**:
   ```
   src/anonymization/application/orchestrator.py:74
   ```

2. **Run**: "Test: Iteration 4 Integration Test"

3. **Observe**: Retry loop and agent coordination

---

## 🔍 Key Features

### ✅ Automatic Hot Reload
- Code changes reload automatically when debugging API
- No need to restart debugger

### ✅ Proper PYTHONPATH
- All imports work correctly
- `from anonymization.domain...` resolves properly

### ✅ Step Into Framework Code
- `justMyCode: false` allows stepping into FastAPI, Pydantic, etc.
- Great for understanding how libraries work

### ✅ Environment Variables
- `.env` file loaded automatically
- API keys and config available during debugging

### ✅ Integrated Terminal
- See all output including print statements
- Run additional commands while debugging

---

## 📋 Available Debug Commands

While debugging, use these keyboard shortcuts:

| Key | Action |
|-----|--------|
| **F5** | Start/Continue debugging |
| **F9** | Toggle breakpoint |
| **F10** | Step over (next line) |
| **F11** | Step into (enter function) |
| **Shift+F11** | Step out (exit function) |
| **Shift+F5** | Stop debugging |
| **Ctrl+Shift+F5** | Restart debugging |

### Debug Console Commands

While paused at breakpoint, try in Debug Console:
```python
# Inspect variables
request.text
result.anonymization.mappings

# Call methods
document.is_empty()
len(validation.issues)

# Import and test
import os
os.getenv('ANTHROPIC_API_KEY')
```

---

## 🧪 Testing the Setup

### Test 1: API Debugging Works

```bash
# Terminal 1: Start debugging
# Press F5 → "FastAPI: Run API Server"

# Terminal 2: Send request
curl http://localhost:8000/health
```

**Expected**: API responds, debugger works

### Test 2: Breakpoints Work

1. Open `routers/anonymization.py`
2. Set breakpoint at line 40
3. Press F5 → "FastAPI: Run API Server"
4. Send request via REST Client or curl
5. **Expected**: Execution pauses at breakpoint

### Test 3: Integration Test Works

1. Press F5 → "Test: Iteration 4 Integration Test"
2. **Expected**: Test runs, you can step through

---

## 🛠️ Troubleshooting

### Issue: "Cannot find module 'anonymization'"

**Fix**: Check `.vscode/settings.json` has:
```json
"python.analysis.extraPaths": ["${workspaceFolder}/src"]
```

### Issue: Environment variables not loaded

**Fix**: Create `.env` file:
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Issue: Port 8000 already in use

**Fix**: Kill existing process:
```bash
lsof -i :8000  # Find PID
kill -9 <PID>  # Kill process
```

### Issue: Breakpoints greyed out

**Fix**:
- Ensure code is actually executing
- Check `justMyCode: false` in launch.json
- Restart VS Code

---

## 📚 Learn More

- **DEBUG-GUIDE.md** - Comprehensive debugging guide
- **api-tests.http** - All API test scenarios
- **README-ITERATION-4.md** - Full project documentation

---

## 🎓 Pro Tips

1. **Use Conditional Breakpoints**:
   - Right-click breakpoint → Edit Breakpoint
   - Add condition: `request.text == "test"`

2. **Use Logpoints** (non-breaking logs):
   - Right-click line → Add Logpoint
   - Enter message: `Request received: {request.text}`

3. **Watch Expressions**:
   - Add to Watch panel: `result.validation.passed`
   - Updates automatically as you step

4. **Exception Breakpoints**:
   - Debug panel → Breakpoints
   - Check "Raised Exceptions"
   - Pause on any exception

5. **Quick File Access**:
   - `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
   - Type filename to quickly open

---

## 🚀 Next Steps

1. **Try debugging the API**:
   - Set breakpoint in anonymization.py
   - Send test request
   - Step through code

2. **Explore the test file**:
   - Open `.vscode/api-tests.http`
   - Try different scenarios
   - See how API responds

3. **Debug an agent**:
   - Set breakpoint in agent1_anon_exec.py
   - Run integration test
   - Watch entity processing

4. **Read the guide**:
   - Open `.vscode/DEBUG-GUIDE.md`
   - Learn advanced techniques
   - Become a debugging pro!

---

**Happy Debugging!** 🐛🔍

Your development environment is now production-ready for debugging the GDPR Anonymizer.
