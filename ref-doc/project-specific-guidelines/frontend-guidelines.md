---
alwaysApply: true
projectName: RealWorld Frontend (Conduit)
---
#####
Title: RealWorld Frontend - Project-Specific Development Guidelines

Applies to: All Frontend Development in the RealWorld (Conduit) Application

Project: React + Redux Toolkit + TypeScript + Vite Implementation

Rule:
You will develop and maintain the RealWorld frontend application following these project-specific patterns and conventions established in the codebase.

## 1. Project Overview

### 1.1 Technology Stack
- **Framework**: React 18.2.0 with TypeScript 5.3.3
- **State Management**: Redux Toolkit 2.2.1 with React-Redux 9.1.0
- **Routing**: React Router DOM 6.22.2
- **Build Tool**: Vite 5.1.4
- **HTTP Client**: Axios 1.6.7
- **Error Handling**: @hqoss/monads 0.5.0
- **Utilities**: Ramda 0.29.1, date-fns 3.3.1
- **Validation**: decoders 2.0.1

### 1.2 Application Structure
```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── App/            # Main application component
│   │   ├── Pages/          # Page components
│   │   │   ├── ArticlePage/
│   │   │   ├── EditArticle/
│   │   │   ├── Home/
│   │   │   ├── Login/
│   │   │   ├── NewArticle/
│   │   │   ├── ProfilePage/
│   │   │   ├── Register/
│   │   │   └── Settings/
│   │   ├── ArticleEditor/  # Article editing component
│   │   ├── ArticlePreview/ # Article preview component
│   │   ├── ArticlesViewer/ # Articles list component
│   │   ├── Footer/         # Footer component
│   │   ├── Header/         # Header component
│   │   ├── GenericForm/    # Reusable form component
│   │   └── UserInfo/       # User information component
│   ├── config/             # Application configuration
│   ├── services/           # API services
│   ├── state/              # Redux store configuration
│   └── types/              # TypeScript type definitions
├── index.html              # Entry HTML file
├── tsconfig.json           # TypeScript configuration
└── vite.config.ts          # Vite configuration
```

## 2. Component Architecture

### 2.1 Component Structure Pattern
Every component follows this pattern with Redux Toolkit slice:

```typescript
// components/Pages/Login/Login.tsx
import { FC, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../../../services/conduit';
import { store } from '../../../state/store';
import { useStore } from '../../../state/storeHooks';
import { loadUserIntoApp } from '../../App/App.slice';
import { LoginState, startLoginIn, updateEmail, updatePassword } from './Login.slice';

export function Login() {
  const { email, password, loginIn, errors } = useStore(({ login }) => login);
  const navigate = useNavigate();

  async function signIn(ev: FormEvent) {
    ev.preventDefault();
    store.dispatch(startLoginIn());
    
    const result = await login(email, password);
    result.match({
      ok: (user) => {
        location.hash = '#/';
        store.dispatch(loadUserIntoApp(user));
      },
      err: (errors) => {
        store.dispatch(updateErrors(errors));
      },
    });
  }

  return (
    <div className='auth-page'>
      {/* Component JSX */}
    </div>
  );
}
```

### 2.2 Slice Pattern (Redux Toolkit)
Each feature has its own slice file:

```typescript
// components/Pages/Login/Login.slice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { GenericErrors } from '../../../types/error';

export interface LoginState {
  email: string;
  password: string;
  loginIn: boolean;
  errors: GenericErrors;
}

const initialState: LoginState = {
  email: '',
  password: '',
  loginIn: false,
  errors: {},
};

const slice = createSlice({
  name: 'login',
  initialState,
  reducers: {
    initialize: () => initialState,
    updateEmail: (state, { payload: email }: PayloadAction<string>) => {
      state.email = email;
    },
    updatePassword: (state, { payload: password }: PayloadAction<string>) => {
      state.password = password;
    },
    startLoginIn: (state) => {
      state.loginIn = true;
    },
    updateErrors: (state, { payload: errors }: PayloadAction<GenericErrors>) => {
      state.errors = errors;
      state.loginIn = false;
    },
  },
});

export const { initialize, updateEmail, updatePassword, startLoginIn, updateErrors } = slice.actions;
export default slice.reducer;
```

### 2.3 Page Component Pattern
All page components follow this structure:
- Located in `components/Pages/{PageName}/`
- Has accompanying `.slice.tsx` file for Redux state
- Uses custom hooks for initialization
- Handles routing with React Router

## 3. State Management

### 3.1 Store Configuration
The store is configured with all feature slices:

```typescript
// state/store.ts
import { configureStore } from '@reduxjs/toolkit';
import app from '../components/App/App.slice';
import home from '../components/Pages/Home/Home.slice';
import login from '../components/Pages/Login/Login.slice';
// ... other slices

export const store = configureStore({
  reducer: { app, home, login, settings, register, editor, articleViewer, profile, articlePage },
  devTools: {
    name: 'Conduit',
  },
});

export type State = ReturnType<typeof store.getState>;
```

### 3.2 Custom Hooks
The project uses custom hooks for store access:

```typescript
// state/storeHooks.ts
import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { State, store } from './store';

export function useStore<Result>(selector: (state: State) => Result): Result {
  return useSelector(selector);
}

export function useStoreWithInitializer<Result>(
  selector: (state: State) => Result,
  initializer: () => void,
): Result {
  useEffect(initializer, []);
  return useStore(selector);
}
```

## 4. API Service Layer

### 4.1 Conduit Service
All API calls are centralized in `services/conduit.ts`:

```typescript
// services/conduit.ts
import { Err, Ok, Result } from '@hqoss/monads';
import axios, { AxiosError } from 'axios';
import settings from '../config/settings';

axios.defaults.baseURL = settings.baseApiUrl;

// API methods follow this pattern
export async function login(email: string, password: string): Promise<Result<User, GenericErrors>> {
  try {
    const { data } = await axios.post('users/login', { user: { email, password } });
    return Ok(object({ user: userDecoder }).verify(data).user);
  } catch (error) {
    const axiosError = error as AxiosError;
    return Err(object({ errors: genericErrorsDecoder }).verify(axiosError.response?.data).errors);
  }
}
```

### 4.2 Error Handling with Monads
The project uses Result monads for error handling:

```typescript
const result = await login(email, password);
result.match({
  ok: (user) => {
    // Handle success
    store.dispatch(loadUserIntoApp(user));
  },
  err: (errors) => {
    // Handle errors
    store.dispatch(updateErrors(errors));
  },
});
```

## 5. Type System

### 5.1 Type Definitions
All types are centralized in the `types/` directory:

```typescript
// types/user.ts
export interface User {
  email: string;
  token: string;
  username: string;
  bio: string;
  image: string;
}

// types/article.ts
export interface Article {
  slug: string;
  title: string;
  description: string;
  body: string;
  tagList: string[];
  createdAt: Date;
  updatedAt: Date;
  favorited: boolean;
  favoritesCount: number;
  author: Profile;
}
```

### 5.2 Decoders for Runtime Validation
The project uses decoders for API response validation:

```typescript
// types/user.ts
import { object, string, optional } from 'decoders';

export const userDecoder = object({
  email: string,
  token: string,
  username: string,
  bio: optional(string),
  image: optional(string),
});
```

## 6. Routing

### 6.1 HashRouter Configuration
The app uses HashRouter with protected routes:

```typescript
// components/App/App.tsx
import { HashRouter, Navigate, Route, Routes } from 'react-router-dom';

function createGuestOnlyRoute(path: string, element: JSX.Element, userIsLogged: boolean) {
  return <Route path={path} element={userIsLogged ? <Navigate to='/' /> : element} />;
}

function createUserOnlyRoute(path: string, element: JSX.Element, userIsLogged: boolean) {
  return <Route path={path} element={!userIsLogged ? <Navigate to='/' /> : element} />;
}

export function App() {
  const userIsLogged = !!user;
  
  return (
    <HashRouter>
      <Routes>
        {createGuestOnlyRoute('/login', <Login />, userIsLogged)}
        {createGuestOnlyRoute('/register', <Register />, userIsLogged)}
        {createUserOnlyRoute('/settings', <Settings />, userIsLogged)}
        {createUserOnlyRoute('/editor', <NewArticle />, userIsLogged)}
        <Route path='/profile/:username' element={<ProfilePage />} />
        <Route path='/article/:slug' element={<ArticlePage />} />
        <Route path='/' element={<Home />} />
      </Routes>
    </HashRouter>
  );
}
```

## 7. Forms and Validation

### 7.1 Generic Form Component
The project uses a reusable GenericForm component:

```typescript
// components/GenericForm/GenericForm.tsx
export interface GenericFormField {
  name: string;
  placeholder: string;
  type?: string;
  rows?: number;
  fieldType?: string;
}

export function GenericForm({
  fields,
  disabled,
  formObject,
  submitButtonText,
  errors,
  onChange,
  onSubmit,
}: GenericFormProps) {
  // Form implementation with dynamic field rendering
}
```

### 7.2 Form State Management
Forms use Redux slices for state management:

```typescript
// Update form fields through Redux actions
store.dispatch(updateField({ name: 'email', value: 'user@example.com' }));
```

## 8. Authentication

### 8.1 Token Management
JWT tokens are stored and managed through the user slice:

```typescript
// Store token after login
localStorage.setItem('token', user.token);
axios.defaults.headers.Authorization = `Token ${user.token}`;

// Load user on app initialization
async function load() {
  const token = localStorage.getItem('token');
  if (token) {
    axios.defaults.headers.Authorization = `Token ${token}`;
    const user = await getUser();
    store.dispatch(loadUser(user));
  }
}
```

## 9. Development Workflow

### 9.1 Available Scripts
```bash
# Start development server
npm start

# Build for production
npm run build

# Preview production build
npm run preview
```

### 9.2 Environment Configuration
```typescript
// config/settings.ts
const settings = {
  baseApiUrl: import.meta.env.VITE_API_URL || 'https://api.realworld.io/api',
};

export default settings;
```

## 10. Code Standards

### 10.1 Component Checklist
- [ ] Component has TypeScript interfaces for props
- [ ] Component has accompanying Redux slice if stateful
- [ ] API calls use Result monad for error handling
- [ ] Forms use GenericForm component
- [ ] Types are defined and use decoders for validation
- [ ] Component is exported from index file

### 10.2 Naming Conventions
- **Components**: PascalCase (e.g., `ArticleEditor.tsx`)
- **Slices**: PascalCase with `.slice.tsx` extension
- **Services**: camelCase (e.g., `conduit.ts`)
- **Types**: PascalCase for interfaces, camelCase for files
- **Utils**: camelCase

### 10.3 File Organization
```
ComponentFolder/
├── ComponentName.tsx       # Component implementation
├── ComponentName.slice.tsx # Redux slice (if needed)
└── index.tsx              # Re-export
```

## 11. Testing Strategy

### 11.1 Component Testing
- Test components with React Testing Library
- Mock Redux store for connected components
- Test user interactions and state changes

### 11.2 Slice Testing
- Test reducers independently
- Verify state updates for each action
- Test async thunks with mock API calls

## 12. Performance Optimization

### 12.1 Code Splitting
- Lazy load page components
- Use dynamic imports for heavy dependencies

### 12.2 State Optimization
- Use Redux Toolkit's createSelector for memoization
- Avoid unnecessary re-renders with proper selector usage

## Project-Specific Rules

1. **Always use Result monads** for API error handling
2. **Never access store directly in components** - use custom hooks
3. **All API calls must go through conduit.ts service**
4. **Use decoders for all API response validation**
5. **Follow the established slice pattern for state management**
6. **Use GenericForm for all form implementations**
7. **Maintain type safety** - no `any` types
8. **Use HashRouter** for routing (not BrowserRouter)
9. **Store JWT token in localStorage**
10. **Follow the existing component structure patterns**

---

Remember: This is a RealWorld specification implementation. Maintain compatibility with the RealWorld API specification and follow the established patterns in the codebase.
