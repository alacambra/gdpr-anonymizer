# Preact Application Architecture Guidelines

## Table of Contents

1. [Core Architectural Principles](#core-architectural-principles)
2. [Component Classification System](#component-classification-system)
3. [State Management Strategy](#state-management-strategy)
4. [Hooks Usage Guidelines](#hooks-usage-guidelines)
5. [Signals Implementation Patterns](#signals-implementation-patterns)
6. [File Structure Standards](#file-structure-standards)
7. [Testing Strategy](#testing-strategy)
8. [Performance Considerations](#performance-considerations)

---

## Core Architectural Principles

### Separation of Concerns

Applications should maintain clear boundaries between:

- **Presentation Logic** - How things look (Presenter components)
- **Business Logic** - What things do (Container components, custom hooks)
- **State Management** - Where data lives (Signals, Context, local state)
- **Side Effects** - External interactions (API calls, DOM manipulation)

### Component Hierarchy

```
Application Layer
├── Pages (routing targets)
│   └── Containers (logic orchestration)
│       └── Presenters (pure display)
│           └── Primitives (basic UI elements)
```

### API-First Design

All data interactions should go through well-defined API contracts:

- Backend services expose REST/GraphQL APIs
- Frontend components consume APIs through dedicated service layers
- UI remains decoupled from backend implementation

---

## Component Classification System

### 1. Presenter Components (Pure Display)

**Purpose:** Render UI based solely on props, no side effects or state management.

**Rules:**

- Must be pure functions
- All data comes from props
- No `useState`, `useEffect`, or `useSignal`
- Only `useMemo` and `useCallback` allowed for optimization
- Should have TypeScript interfaces for all props

**Example:**

```javascript
interface UserCardProps {
  name: string;
  email: string;
  avatar: string;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

export function UserCard({
  name,
  email,
  avatar,
  onSelect,
  isSelected,
}: UserCardProps) {
  return (
    <div className={isSelected ? "card selected" : "card"}>
      <img src={avatar} alt={name} />
      <h3>{name}</h3>
      <p>{email}</p>
      <button onClick={() => onSelect(email)}>Select</button>
    </div>
  );
}
```

**When to Use:**

- Design system components
- Reusable UI elements
- Components that need visual testing
- When UI requirements change frequently

---

### 2. Container Components (Logic Orchestration) - Optional Pattern

**Purpose:** Manage state, side effects, and business logic. Pass data to presenters.

**Modern Context:** With hooks, this pattern is less necessary than it once was. You can often achieve the same separation by extracting logic into custom hooks rather than creating wrapper components. Consider this pattern when:

- You have complex orchestration logic that would clutter a component
- You're building design system components that need pure display versions
- Team conventions or project requirements favor explicit separation

**Rules:**

- Handle all hooks and signals
- Manage API calls and data fetching
- Coordinate multiple presenters
- Minimal direct rendering (delegate to presenters)
- Name with `Container` suffix

**Example:**

```javascript
import { useSignal } from "@preact/signals";
import { useEffect } from "preact/hooks";
import { UserCard } from "./UserCard";

export function UserListContainer() {
  const users = useSignal([]);
  const selectedId = useSignal(null);
  const loading = useSignal(true);

  useEffect(() => {
    fetchUsers().then((data) => {
      users.value = data;
      loading.value = false;
    });
  }, []);

  if (loading.value) return <LoadingSpinner />;

  return (
    <div className="user-list">
      {users.value.map((user) => (
        <UserCard
          key={user.id}
          {...user}
          isSelected={selectedId.value === user.id}
          onSelect={(id) => (selectedId.value = id)}
        />
      ))}
    </div>
  );
}
```

**Modern Alternative with Custom Hooks:**

```javascript
// Extract logic into a custom hook instead
function useUserList() {
  const users = useSignal([]);
  const selectedId = useSignal(null);
  const loading = useSignal(true);

  useEffect(() => {
    fetchUsers().then((data) => {
      users.value = data;
      loading.value = false;
    });
  }, []);

  return {
    users: users.value,
    selectedId: selectedId.value,
    loading: loading.value,
    setSelectedId: (id) => (selectedId.value = id),
  };
}

// Component uses the hook directly
export function UserList() {
  const { users, selectedId, loading, setSelectedId } = useUserList();

  if (loading) return <LoadingSpinner />;

  return (
    <div className="user-list">
      {users.map((user) => (
        <UserCard
          key={user.id}
          {...user}
          isSelected={selectedId === user.id}
          onSelect={setSelectedId}
        />
      ))}
    </div>
  );
}
```

---

### 3. Layout Components

**Purpose:** Structure page layout, navigation, and composition.

**Rules:**

- Define page structure and grid systems
- Handle routing and navigation
- Compose containers and presenters
- Minimal business logic

**Example:**

```javascript
export function DashboardLayout({ children }) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main className="content">
        <Header />
        {children}
      </main>
    </div>
  );
}
```

---

### 4. Custom Hooks (Reusable Logic)

**Purpose:** Extract and share stateful logic across components.

**Rules:**

- Name with `use` prefix
- Return consistent interface (object or array)
- Handle one logical concern
- Include cleanup in effects

**Example:**

```javascript
function useApi(endpoint) {
  const data = useSignal(null);
  const error = useSignal(null);
  const loading = useSignal(false);

  const fetch = useCallback(async () => {
    loading.value = true;
    try {
      const response = await api.get(endpoint);
      data.value = response.data;
    } catch (err) {
      error.value = err;
    } finally {
      loading.value = false;
    }
  }, [endpoint]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return {
    data: data.value,
    error: error.value,
    loading: loading.value,
    refetch: fetch,
  };
}
```

**When to Create:**

- Logic used in 2+ components
- Complex stateful patterns (3+ `useState` calls)
- Side effects requiring cleanup
- API interaction patterns

---

## State Management Strategy

### Decision Tree

```
Is state needed across entire app?
├─ YES → Global Signals
│
└─ NO → Is state shared between 2-5 components?
    ├─ YES → Context API
    │
    └─ NO → Is state complex with multiple updates?
        ├─ YES → useReducer or useSignal
        │
        └─ NO → useState
```

### 1. Local Component State (useState)

**Use for:**

- UI state (modals, dropdowns, form inputs)
- Simple toggles and flags
- State not shared with other components

```javascript
function SearchBar() {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
    />
  );
}
```

---

### 2. Local Reactive State (useSignal)

**Use for:**

- Local state with computed values
- Frequent updates requiring optimization
- State used in multiple places within component

```javascript
function Counter() {
  const count = useSignal(0);
  const double = useComputed(() => count.value * 2);
  const triple = useComputed(() => count.value * 3);

  return (
    <div>
      <p>Count: {count.value}</p>
      <p>Double: {double.value}</p>
      <p>Triple: {triple.value}</p>
      <button onClick={() => count.value++}>Increment</button>
    </div>
  );
}
```

---

### 3. Shared Component State (Context API)

**Use for:**

- State shared across 2-5 related components
- Theme, locale, or configuration data
- Prop-drilling avoidance (3+ levels deep)

```javascript
import { createContext } from "preact";
import { useContext, useState } from "preact/hooks";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState("light");

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

---

### 4. Global Application State (Signals)

**Use for:**

- User authentication state
- Shopping cart, notifications
- Application-wide configuration
- Real-time data (websockets)

```javascript
// store/user.js
import { signal, computed } from "@preact/signals";

export const user = signal(null);
export const isAuthenticated = computed(() => user.value !== null);
export const userRole = computed(() => user.value?.role || "guest");

export function login(userData) {
  user.value = userData;
}

export function logout() {
  user.value = null;
}

// Component usage
import { user, isAuthenticated } from "./store/user";

function Header() {
  return (
    <header>
      {isAuthenticated.value ? (
        <span>Welcome, {user.value.name}</span>
      ) : (
        <button onClick={handleLogin}>Login</button>
      )}
    </header>
  );
}
```

---

### 5. Server State (Custom Hooks + Caching)

**Use for:**

- API data fetching
- Server-synchronized state
- Data requiring refetch/invalidation

```javascript
// hooks/useQuery.js
import { useSignal } from "@preact/signals";
import { useEffect } from "preact/hooks";

const cache = new Map();

export function useQuery(key, fetcher) {
  const data = useSignal(cache.get(key) || null);
  const error = useSignal(null);
  const loading = useSignal(!cache.has(key));

  useEffect(() => {
    if (cache.has(key)) return;

    fetcher()
      .then((result) => {
        data.value = result;
        cache.set(key, result);
      })
      .catch((err) => (error.value = err))
      .finally(() => (loading.value = false));
  }, [key]);

  return { data: data.value, error: error.value, loading: loading.value };
}

// Usage
function UserProfile({ userId }) {
  const {
    data: user,
    loading,
    error,
  } = useQuery(`user-${userId}`, () => api.getUser(userId));

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <UserCard {...user} />;
}
```

---

## Hooks Usage Guidelines

### Standard Hooks

| Hook          | Use Case                                                                             | When NOT to Use                                                                            |
| ------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `useState`    | Simple local state                                                                   | When state updates are complex and interdependent (use `useReducer`)                       |
| `useEffect`   | Side effects, subscriptions                                                          | Data fetching without cleanup, or logic that doesn't need to sync with render              |
| `useRef`      | DOM access, mutable values that don't trigger renders                                | As a state replacement that should trigger re-renders                                      |
| `useMemo`     | **Expensive** computations identified through profiling                              | Premature optimization, simple calculations, or when dependencies change frequently        |
| `useCallback` | Stabilizing function references for optimized child components                       | Every function by default - only when passing to memoized children or in dependency arrays |
| `useContext`  | Access context values                                                                | Heavy computation in provider value                                                        |
| `useReducer`  | Complex state logic with multiple sub-values, or when next state depends on previous | Simple toggles or single values                                                            |

**Performance Hook Warning:** Only use `useMemo` and `useCallback` **after** identifying performance problems through profiling (React DevTools Profiler). Premature optimization with these hooks can:

- Increase code complexity and reduce readability
- Actually decrease performance (hooks have overhead)
- Make code harder to maintain

**Rule of thumb:** Start simple. Optimize when measurements show a need.

### Signal Hooks (Preact)

| Hook              | Use Case                 | Example                                             |
| ----------------- | ------------------------ | --------------------------------------------------- |
| `useSignal`       | Local reactive state     | `const count = useSignal(0)`                        |
| `useComputed`     | Derived values           | `const double = useComputed(() => count.value * 2)` |
| `useSignalEffect` | Effects tracking signals | `useSignalEffect(() => console.log(count.value))`   |

### Hooks Best Practices

**1. Always call hooks at the top level**

```javascript
// ✅ Correct
function Component() {
  const [state, setState] = useState(0);
  if (state > 10) return <div>Too high</div>;
  return <div>{state}</div>;
}

// ❌ Wrong
function Component() {
  if (someCondition) {
    const [state, setState] = useState(0); // Conditional hook!
  }
}
```

**2. Extract complex logic into custom hooks**

```javascript
// ✅ Correct
function useFormValidation(values) {
  const errors = useSignal({});
  const isValid = useComputed(() => Object.keys(errors.value).length === 0);

  useSignalEffect(() => {
    errors.value = validate(values);
  });

  return { errors: errors.value, isValid: isValid.value };
}

// ❌ Wrong - too much logic in component
function FormComponent() {
  const [errors, setErrors] = useState({});
  const [isValid, setIsValid] = useState(false);
  // ... 50 lines of validation logic
}
```

**3. Use dependency arrays correctly**

```javascript
// ✅ Correct - includes all dependencies
useEffect(() => {
  fetchData(userId, filter);
}, [userId, filter]);

// ❌ Wrong - missing dependencies
useEffect(() => {
  fetchData(userId, filter);
}, []); // Will use stale values!
```

---

## Signals Implementation Patterns

### Why Signals?

Signals provide fine-grained reactivity that updates the DOM directly without triggering full component re-renders. This means:

- **Better performance** for frequently updating values
- **Automatic dependency tracking** for computed values and effects
- **No need for manual optimization** with useMemo/useCallback
- **Simpler mental model** for global state

**When to use Signals over useState:**

- Global or shared state across components
- Values that update frequently (animations, real-time data)
- When you need derived/computed values
- When you want to avoid Context boilerplate

### Global Store Pattern

```javascript
// store/cart.js
import { signal, computed } from "@preact/signals";

// State
export const items = signal([]);

// Computed values
export const total = computed(() =>
  items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
);

export const itemCount = computed(() =>
  items.value.reduce((sum, item) => sum + item.quantity, 0)
);

// Actions
export function addItem(product) {
  const existing = items.value.find((i) => i.id === product.id);

  if (existing) {
    items.value = items.value.map((i) =>
      i.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
    );
  } else {
    items.value = [...items.value, { ...product, quantity: 1 }];
  }
}

export function removeItem(productId) {
  items.value = items.value.filter((i) => i.id !== productId);
}

export function clearCart() {
  items.value = [];
}
```

### Component Integration

```javascript
import { total, itemCount, addItem } from "./store/cart";

function CartSummary() {
  return (
    <div className="cart-summary">
      <span>{itemCount.value} items</span>
      <span>${total.value.toFixed(2)}</span>
    </div>
  );
}

function ProductCard({ product }) {
  return (
    <div className="product">
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button onClick={() => addItem(product)}>Add to Cart</button>
    </div>
  );
}
```

### Signals with Effects

```javascript
import { signal, effect } from "@preact/signals";

const user = signal(null);

// Persist to localStorage
effect(() => {
  if (user.value) {
    localStorage.setItem("user", JSON.stringify(user.value));
  } else {
    localStorage.removeItem("user");
  }
});

// Send analytics
effect(() => {
  if (user.value) {
    analytics.identify(user.value.id, {
      name: user.value.name,
      email: user.value.email,
    });
  }
});
```

---

## File Structure Standards

### Project Organization

```
src/
├── components/          # Reusable UI components
│   ├── primitives/      # Basic UI elements (Button, Input, Card)
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   ├── Button.test.jsx       # Test co-located with component
│   │   │   ├── Button.module.css
│   │   │   └── index.js
│   │   └── Input/
│   ├── presenters/      # Display-only components (with tests)
│   └── containers/      # Logic-heavy components (with tests)
├── pages/               # Route components
│   ├── Home/
│   │   ├── HomeContainer.jsx
│   │   ├── HomeContainer.test.jsx    # Test co-located
│   │   ├── HomeView.jsx
│   │   ├── HomeView.test.jsx         # Test co-located
│   │   └── index.js
│   └── Dashboard/
├── hooks/               # Custom hooks
│   ├── useApi.js
│   ├── useApi.test.js               # Test co-located
│   ├── useAuth.js
│   └── useForm.js
├── store/               # Global signals
│   ├── user.js
│   ├── user.test.js                 # Test co-located
│   ├── cart.js
│   └── notifications.js
├── services/            # API integrations
│   ├── api.js
│   ├── api.test.js                  # Test co-located
│   ├── auth.js
│   └── storage.js
├── utils/               # Helper functions (with tests)
├── types/               # TypeScript types
├── styles/              # Global styles
└── __tests__/           # Integration/E2E tests only
    ├── integration/
    └── e2e/
```

### Test Co-location Principle

**Tests should live next to the code they test.** This means:

- Component tests in the same folder as the component
- Hook tests in the same folder as the hook
- Store tests in the same folder as the store

**Exception:** Only place tests in separate directories when they:

- Test multiple components together (integration tests)
- Test full user flows (E2E tests)
- Are cross-cutting concerns (accessibility audits, performance tests)

**Benefits of co-location:**

- Easier to find tests when modifying code
- Tests more likely to be updated with code changes
- Clear ownership and responsibility
- Better IDE integration

### Component File Naming

```
UserProfile/
├── UserProfile.jsx              # Main component (or UserProfileContainer.jsx if using pattern)
├── UserProfile.test.jsx         # Tests co-located
├── UserProfile.module.css       # Component styles
└── index.js                     # Public exports
```

### Export Pattern

```javascript
// index.js - Single public interface
export { UserProfileContainer as UserProfile } from "./UserProfileContainer";

// Usage in other files
import { UserProfile } from "@/components/UserProfile";
```

---

## Testing Strategy

### Testing Philosophy

**Test behavior, not implementation.** Focus on:

- What the user sees and does
- How the component responds to interactions
- Outcomes and side effects
- NOT internal state, variable names, or implementation details

**Use React Testing Library principles:**

- Query elements by their accessible role, label, or text content
- Interact with components as a user would
- Assert on visible changes and outputs

### Test Pyramid

```
        E2E Tests (10%)
        Full user flows
    ───────────────────
   Integration Tests (30%)
   Multiple components
  ─────────────────────────
 Unit Tests (60%)
 Individual components/hooks
```

**Note:** The boundaries between unit and integration tests are often blurry with UI components. A "unit test" for a form might naturally test its buttons and inputs together. This is fine - focus on testing behavior at the appropriate level.

### 1. Component Tests (Behavior-Focused)

**Test user interactions and outcomes, not implementation:**

```javascript
import { render, screen, fireEvent } from "@testing-library/preact";
import { UserCard } from "./UserCard";

describe("UserCard", () => {
  const mockUser = {
    name: "John Doe",
    email: "john@example.com",
    avatar: "/avatar.jpg",
  };

  it("displays user information to the user", () => {
    render(<UserCard {...mockUser} onSelect={() => {}} isSelected={false} />);

    // Query by what the user sees
    expect(screen.getByText("John Doe")).toBeInTheDocument();
    expect(screen.getByText("john@example.com")).toBeInTheDocument();
    expect(screen.getByRole("img", { name: "John Doe" })).toBeInTheDocument();
  });

  it("allows user to select the card", () => {
    const onSelect = jest.fn();
    render(<UserCard {...mockUser} onSelect={onSelect} isSelected={false} />);

    // Interact as a user would
    fireEvent.click(screen.getByRole("button", { name: /select/i }));
    expect(onSelect).toHaveBeenCalledWith("john@example.com");
  });

  it("shows selected state visually", () => {
    const { container } = render(
      <UserCard {...mockUser} onSelect={() => {}} isSelected={true} />
    );

    // Test visual feedback that affects user
    expect(container.firstChild).toHaveClass("selected");
  });
});
```

**Anti-patterns to avoid:**

```javascript
// ❌ Don't test internal state
expect(component.state.isOpen).toBe(true);

// ❌ Don't test implementation details
expect(mockFunction).toHaveBeenCalledTimes(1); // Unless this affects user experience

// ✅ Do test user-visible behavior
expect(screen.getByRole("dialog")).toBeVisible();
```

### 2. Integration Tests (Component Interactions)

**Test how components work together:**

```javascript
import { render, screen, waitFor } from "@testing-library/preact";
import { UserListContainer } from "./UserListContainer";
import * as api from "@/services/api";

jest.mock("@/services/api");

describe("UserListContainer", () => {
  it("loads and displays users to the user", async () => {
    const mockUsers = [
      { id: 1, name: "John", email: "john@example.com" },
      { id: 2, name: "Jane", email: "jane@example.com" },
    ];

    api.fetchUsers.mockResolvedValue(mockUsers);

    render(<UserListContainer />);

    // User sees loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Then sees the data
    await waitFor(() => {
      expect(screen.getByText("John")).toBeInTheDocument();
      expect(screen.getByText("Jane")).toBeInTheDocument();
    });
  });

  it("handles errors gracefully for the user", async () => {
    api.fetchUsers.mockRejectedValue(new Error("Network error"));

    render(<UserListContainer />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

### 3. Signal/Store Testing

**Test state behavior and side effects:**

```javascript
import { signal, computed } from "@preact/signals";
import { addItem, removeItem, total, items, clearCart } from "./store/cart";

describe("Cart Store", () => {
  beforeEach(() => {
    clearCart(); // Reset state between tests
  });

  it("calculates total correctly", () => {
    addItem({ id: 1, name: "Product", price: 10 });
    addItem({ id: 1, name: "Product", price: 10 }); // Add same item twice

    expect(total.value).toBe(20);
  });

  it("removes items", () => {
    addItem({ id: 1, name: "Product", price: 10 });
    removeItem(1);

    expect(items.value).toHaveLength(0);
    expect(total.value).toBe(0);
  });

  it("handles quantity updates", () => {
    const product = { id: 1, name: "Product", price: 10 };
    addItem(product);
    addItem(product);
    addItem(product);

    expect(items.value[0].quantity).toBe(3);
    expect(total.value).toBe(30);
  });
});
```

### 4. Custom Hook Testing

**Test hooks using `renderHook` from Testing Library:**

```javascript
import { renderHook, waitFor } from "@testing-library/preact";
import { useApi } from "./useApi";
import * as api from "@/services/api";

jest.mock("@/services/api");

describe("useApi", () => {
  it("fetches data successfully", async () => {
    const mockData = { id: 1, name: "Test" };
    api.get.mockResolvedValue({ data: mockData });

    const { result } = renderHook(() => useApi("/users/1"));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toEqual(mockData);
      expect(result.current.error).toBe(null);
    });
  });

  it("handles errors", async () => {
    const error = new Error("Network error");
    api.get.mockRejectedValue(error);

    const { result } = renderHook(() => useApi("/users/1"));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBe(error);
    });
  });
});
```

### Testing Best Practices

**DO:**

- Test from the user's perspective
- Use semantic queries (`getByRole`, `getByLabelText`, `getByText`)
- Test accessibility features (ARIA labels, keyboard navigation)
- Wait for async operations with `waitFor`
- Mock external dependencies (APIs, third-party libraries)
- Reset state between tests

**DON'T:**

- Test implementation details (internal state, function names)
- Use `querySelector` when semantic queries are available
- Test framework internals (React/Preact behavior itself)
- Rely on CSS selectors for critical tests
- Forget to clean up side effects

---

## Performance Considerations

### Performance Philosophy

**Measure first, optimize second.** React and Preact are highly optimized by default. Premature optimization:

- Makes code harder to read and maintain
- Can actually decrease performance (optimization has overhead)
- Distracts from real performance issues

**Use React DevTools Profiler** to identify actual bottlenecks before applying optimizations.

### 1. When to Optimize Components

**Use Signals for Frequent Updates**

Signals bypass the virtual DOM and update directly, making them ideal for high-frequency updates:

```javascript
// ✅ Good - only the <div> updates, component doesn't re-render
const counter = signal(0);

function Display() {
  return <div>{counter.value}</div>;
}

function Increment() {
  return <button onClick={() => counter.value++}>+</button>;
}

// ✅ Also good for animations
const mouseX = signal(0);
const mouseY = signal(0);

function Cursor() {
  return <div style={{ left: mouseX.value, top: mouseY.value }} />;
}
```

**Memoize Only When Proven Slow**

```javascript
function DataTable({ data }) {
  // ⚠️ Only add useMemo if profiling shows this sort is slow
  const sorted = useMemo(() => {
    console.log("Sorting..."); // Add logging to verify it's actually expensive
    return data.sort((a, b) => a.score - b.score);
  }, [data]);

  return <table>{/* render sorted data */}</table>;
}

// ❌ Don't memoize cheap operations
const doubled = useMemo(() => count * 2, [count]); // Unnecessary overhead

// ✅ Just compute directly
const doubled = count * 2;
```

**useCallback for Optimized Children Only**

```javascript
// ✅ Good - child is memoized and won't re-render unnecessarily
const MemoizedChild = memo(ExpensiveChild);

function Parent() {
  const handleClick = useCallback(() => {
    doSomething();
  }, []);

  return <MemoizedChild onClick={handleClick} />;
}

// ❌ Unnecessary - child isn't memoized
function Parent() {
  const handleClick = useCallback(() => {
    doSomething();
  }, []);

  return <RegularChild onClick={handleClick} />;
}
```

### 2. List Rendering Best Practices

**Always Use Stable Keys**

Keys help Preact identify which items have changed, been added, or removed:

```javascript
// ✅ Correct - stable, unique keys
{
  users.map((user) => <UserCard key={user.id} {...user} />);
}

// ❌ Wrong - no keys (causes bugs and performance issues)
{
  users.map((user) => <UserCard {...user} />);
}

// ❌ Wrong - array index as key (breaks when list reorders)
{
  users.map((user, index) => <UserCard key={index} {...user} />);
}
```

**Virtualize Long Lists**

For lists with hundreds/thousands of items, only render what's visible:

```javascript
import { useVirtualList } from "@/hooks/useVirtualList";

function LongList({ items }) {
  const { visibleItems, containerProps, innerProps } = useVirtualList({
    items,
    itemHeight: 50,
    containerHeight: 600,
  });

  return (
    <div {...containerProps}>
      <div {...innerProps}>
        {visibleItems.map((item) => (
          <ListItem key={item.id} {...item} />
        ))}
      </div>
    </div>
  );
}
```

**When to virtualize:**

- Lists with 100+ items
- After profiling shows rendering performance issues
- When scroll performance is poormap(user => (
  <UserCard key={user.id} {...user} />
  ))}

// ❌ Wrong
{users.map(user => (
<UserCard {...user} />
))}

````

**Virtualize Long Lists**
```javascript
import { useVirtualList } from '@/hooks/useVirtualList';

function LongList({ items }) {
  const { visibleItems, containerProps, innerProps } = useVirtualList({
    items,
    itemHeight: 50,
    containerHeight: 600
  });

  return (
    <div {...containerProps}>
      <div {...innerProps}>
        {visibleItems.map(item => (
          <ListItem key={item.id} {...item} />
        ))}
      </div>
    </div>
  );
}
````

### 3. Code Splitting

```javascript
import { lazy, Suspense } from "preact/compat";

const Dashboard = lazy(() => import("./pages/Dashboard"));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Dashboard />
    </Suspense>
  );
}
```

---

## Summary Checklist

### Component Design

- [ ] Presenters are pure and receive all data via props
- [ ] Containers handle logic and pass data to presenters
- [ ] Custom hooks extract reusable logic
- [ ] Components have single responsibility

### State Management

- [ ] Local UI state uses `useState`
- [ ] Shared state (2-5 components) uses Context
- [ ] Global state uses Signals
- [ ] Server state has dedicated hooks with caching

### Code Quality

- [ ] All components have TypeScript interfaces
- [ ] Hooks follow rules (top-level, dependencies)
- [ ] Effects have cleanup functions
- [ ] Components are testable (unit + integration)

### Performance

- [ ] Lists use keys
- [ ] Expensive computations are memoized
- [ ] Heavy components are code-split
- [ ] Signals used for frequent updates

### File Organization

- [ ] Clear folder structure (components/pages/hooks/store)
- [ ] Consistent naming conventions
- [ ] Single export point per module
- [ ] Co-located tests and styles
