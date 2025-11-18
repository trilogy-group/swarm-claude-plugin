---
alwaysApply: true
---
#####
Title: Web UI Development Standards and Guidelines

Applies to: All Frontend Development Tasks

Rule:
You will develop web UI applications following these comprehensive standards, patterns, and processes derived from the alert-engine-ui project structure and industry best practices.

## 1. Project Structure

### 1.1 Standard Directory Organization
Every UI project must follow this standardized directory structure:

```
src/
├── components/          # Reusable UI components
│   ├── ui/              # Base UI components (shadcn/ui)
│   ├── dashboards/      # Dashboard-specific components
│   ├── modals/          # Modal components
│   └── wizards/         # Multi-step wizard components
├── pages/               # Page components (routes)
│   └── PageName/        # Complex pages with sub-components
├── services/            # API integration and business logic
├── hooks/               # Custom React hooks
├── context/             # React Context providers
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
├── lib/                 # Third-party library configurations
├── config/              # Application configuration
└── assets/              # Static assets (images, fonts)
```

### 1.2 File Naming Conventions
- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Pages**: PascalCase (e.g., `AlertEngine.tsx`)
- **Services**: camelCase with descriptive suffix (e.g., `tmfOdaHttpService.ts`)
- **Hooks**: camelCase starting with 'use' (e.g., `useAlertData.ts`)
- **Utils**: camelCase (e.g., `formatDate.ts`)
- **Types**: PascalCase for interfaces/types, camelCase for files (e.g., `transformationJourney.ts`)

### 1.3 Component Organization
For complex features, create a dedicated folder:
```
pages/AlertEngine/
├── index.tsx                    # Main component
├── AlertCorrelation.tsx         # Sub-component
├── NetworkAnalysis.tsx          # Sub-component
├── RootCauseAnalysis.tsx        # Sub-component
└── types.ts                     # Local type definitions
```

## 2. Code Structure

### 2.1 Component Architecture
Every React component must follow this structure:

```typescript
// 1. Imports - organized by category
import { useState, useEffect, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { realAlertService } from "@/services/realAlertService";
import type { AlertData } from "@/types/alert";

// 2. Type definitions
interface ComponentProps {
  dataSource: "json" | "api";
  onUpdate?: (data: AlertData) => void;
}

// 3. Component definition
const ComponentName = ({ dataSource, onUpdate }: ComponentProps) => {
  // 4. State declarations
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<AlertData | null>(null);
  
  // 5. Custom hooks
  const { user } = useAuth();
  
  // 6. Effects
  useEffect(() => {
    loadData();
  }, [dataSource]);
  
  // 7. Event handlers
  const handleClick = useCallback(() => {
    // Handle event
  }, []);
  
  // 8. Helper functions
  const loadData = async () => {
    try {
      const result = await realAlertService.getData();
      setData(result);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // 9. Render
  return (
    <div className="space-y-4">
      {/* Component JSX */}
    </div>
  );
};

export default ComponentName;
```

### 2.2 TypeScript Standards
- **Always use TypeScript** for type safety
- **Define interfaces** for all props, API responses, and complex data structures
- **Use type imports**: `import type { TypeName } from './types'`
- **Avoid 'any' type**: Use `unknown` or specific types instead
- **Export types** that other components might need

### 2.3 State Management
- **Local state**: Use `useState` for component-specific state
- **Global state**: Use React Context for cross-component state
- **Server state**: Use React Query for API data caching
- **Form state**: Use react-hook-form with zod validation

## 3. Themes and Layouts

### 3.1 Design System
Use shadcn/ui as the base component library with Tailwind CSS:

```typescript
// Use shadcn components
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

// Apply consistent spacing
<div className="container mx-auto p-6 space-y-6">
  <Card>
    <CardHeader>
      <CardTitle>Title</CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      {/* Content */}
    </CardContent>
  </Card>
</div>
```

### 3.2 Theme Provider
Implement dark/light mode support:
```typescript
// Wrap app with ThemeProvider
<ThemeProvider defaultTheme="system" storageKey="ui-theme">
  <App />
</ThemeProvider>
```

### 3.3 Responsive Design
- **Mobile-first approach**: Start with mobile layout
- **Breakpoints**: Use Tailwind's responsive prefixes (sm:, md:, lg:, xl:)
- **Grid system**: Use CSS Grid or Flexbox for layouts
- **Test on devices**: Ensure UI works on all screen sizes

## 4. Feature Pages/Dashboard Implementation

### 4.1 Dashboard Components
Every dashboard must include:
- **KPI Cards**: Display key metrics at the top
- **Charts**: Use Recharts for data visualization
- **Data Tables**: Implement with sorting, filtering, pagination
- **Action Buttons**: Provide clear CTAs
- **Loading States**: Show skeletons or spinners
- **Error States**: Display user-friendly error messages

### 4.2 Page Structure Template
```typescript
const DashboardPage = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [timeRange, setTimeRange] = useState("24h");
  
  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard Title</h1>
        <div className="flex gap-2">
          {/* Action buttons */}
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* KPI cards */}
      </div>
      
      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          {/* Tab content */}
        </TabsContent>
      </Tabs>
    </div>
  );
};
```

## 5. Integration Rules For UI-MCP Tools

### 5.1 Service Layer Pattern
Create dedicated service files for API integration:

```typescript
// services/tmfOdaHttpService.ts
class TmfOdaHttpService {
  private baseUrl: string;
  private timeout: number;
  
  constructor() {
    this.baseUrl = import.meta.env.VITE_TMF_ODA_API_BASE_URL || 'http://localhost:8000';
    this.timeout = parseInt(import.meta.env.VITE_TMF_ODA_API_TIMEOUT || '30000');
  }
  
  async fetchJourneys(journeyId?: string): Promise<ApiResponse> {
    const response = await fetch(`${this.baseUrl}/tools/journeys_tool`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        action: journeyId ? 'read' : 'list', 
        journey_id: journeyId 
      }),
      signal: AbortSignal.timeout(this.timeout),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.result; // Extract inner result
  }
}

export const tmfOdaHttpService = new TmfOdaHttpService();
```

### 5.2 Error Handling
Implement comprehensive error handling:
```typescript
try {
  const response = await fetch(url, options);
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }
  
  const result = await response.json();
  
  if (result.status === 'error') {
    throw new Error(result.message || 'API error');
  }
  
  return result;
} catch (error) {
  if (error.name === 'AbortError') {
    console.error('Request timeout');
  } else if (error.message.includes('Failed to fetch')) {
    console.error('Network error - backend not accessible');
  } else {
    console.error('API error:', error.message);
  }
  throw error;
}
```

### 5.3 Data Transformation
Always transform API data to UI models:
```typescript
private convertApiToUi(apiData: ApiJourney): UiJourney {
  return {
    id: apiData.journeyId,
    name: apiData.name,
    status: this.mapStatus(apiData.status),
    createdAt: new Date(apiData.createdAt),
    progress: apiData.overallProgress ?? 0,
  };
}
```

## 6. Standard Auth and RBAC Implementation

### 6.1 Authentication Context
Implement centralized authentication:

```typescript
// context/EnterpriseAuthContext.tsx
const EnterpriseAuthContext = createContext<AuthContextType>();

export const EnterpriseAuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const signIn = async (email: string, password: string) => {
    // Cognito or other auth implementation
  };
  
  const hasPermission = (permission: Permission): boolean => {
    return profile?.permissions?.includes(permission) ?? false;
  };
  
  return (
    <EnterpriseAuthContext.Provider value={{ 
      user, 
      profile, 
      signIn, 
      hasPermission 
    }}>
      {children}
    </EnterpriseAuthContext.Provider>
  );
};
```

### 6.2 Protected Routes
Implement route protection:
```typescript
const ProtectedRoute = ({ children, requiredPermission }) => {
  const { user, hasPermission } = useEnterpriseAuth();
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <Navigate to="/unauthorized" />;
  }
  
  return children;
};
```

### 6.3 Role-Based UI
Conditionally render based on permissions:
```typescript
{hasPermission('manage_alerts') && (
  <Button onClick={handleManage}>Manage Alerts</Button>
)}
```

## 7. Standard Chat Interface with BSS Studio Implementation

### 7.1 Langflow Integration
Integrate with Langflow for AI chat:

```typescript
// components/LangflowChat.tsx
export default function LangflowChat({ isOpen, onClose }) {
  const apiKey = import.meta.env.VITE_LANGFLOW_API_KEY;
  const chatRef = useRef(null);
  
  useEffect(() => {
    if (chatRef.current && apiKey) {
      chatRef.current.setAttribute('flow_id', FLOW_ID);
      chatRef.current.setAttribute('host_url', HOST_URL);
      chatRef.current.setAttribute('api_key', apiKey);
      chatRef.current.setAttribute('chat_position', 'bottom-right');
    }
  }, [apiKey]);
  
  return (
    <langflow-chat ref={chatRef} />
  );
}
```

### 7.2 Chat Service
Implement chat service for custom chat:
```typescript
// services/chatbotService.ts
class ChatbotService {
  async sendMessage(message: string, context: any) {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context }),
    });
    
    return response.json();
  }
}
```

### 7.3 Chat UI Components
Build consistent chat interfaces:
```typescript
const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>
      <div className="p-4 border-t">
        <Input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleSend}
        />
      </div>
    </div>
  );
};
```

## 8. Standard CDN-based Deployment

### 8.1 Build Configuration
Configure Vite for production builds:
```json
// vite.config.ts
export default defineConfig({
  base: '/',
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-tabs'],
        }
      }
    }
  }
});
```

### 8.2 Environment Configuration
Use environment-specific configs:
```bash
# .env.production
VITE_API_BASE_URL=https://api.production.com
VITE_APP_ENV=production

# .env.staging
VITE_API_BASE_URL=https://api.staging.com
VITE_APP_ENV=staging
```

### 8.3 CDN Deployment Script
```bash
#!/bin/bash
# deploy.sh
ENVIRONMENT=$1
source ./deploy/config/${ENVIRONMENT}.conf

# Build
npm run build:${ENVIRONMENT}

# Upload to S3
aws s3 sync dist/ s3://${BUCKET_NAME} --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id ${DISTRIBUTION_ID} \
  --paths "/*"
```

### 8.4 CloudFormation Template
Use IaC for infrastructure:
```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${ProjectName}-ui-${Environment}"
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: index.html
  
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt S3Bucket.DomainName
        DefaultRootObject: index.html
        CustomErrorResponses:
          - ErrorCode: 404
            ResponseCode: 200
            ResponsePagePath: /index.html
```

## 9. Standard Git Workflow

### 9.1 Branch Strategy
Follow GitFlow pattern:
- **main**: Production-ready code
- **stage**: Staging environment
- **dev**: Development integration
- **feature/**: Feature branches
- **bugfix/**: Bug fix branches
- **hotfix/**: Emergency fixes

### 9.2 Commit Standards
Use conventional commits:
```bash
# Format: <type>(<scope>): <subject>
feat(alert-engine): add root cause analysis tab
fix(auth): resolve token refresh issue
docs(readme): update deployment instructions
style(dashboard): improve responsive layout
refactor(services): extract common API logic
test(journey): add unit tests for service
chore(deps): update dependencies
```

### 9.3 Pull Request Process
1. Create feature branch from dev
2. Implement changes with tests
3. Run linting and tests locally
4. Create PR with description
5. Code review by team
6. Merge after approval

### 9.4 Pre-commit Hooks
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm run lint && npm run test",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  }
}
```

## 10. Standard Test Guidelines

### 10.1 Testing Strategy
Implement comprehensive testing:
- **Unit Tests**: Test individual components/functions
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user flows
- **Visual Tests**: Test UI consistency

### 10.2 Unit Testing
```typescript
// ComponentName.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
  
  it('should handle click events', () => {
    const handleClick = jest.fn();
    render(<ComponentName onClick={handleClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### 10.3 Service Testing
```typescript
// service.test.ts
import { tmfOdaService } from './tmfOdaService';

jest.mock('fetch');

describe('TmfOdaService', () => {
  it('should fetch journeys successfully', async () => {
    const mockData = { journeys: [] };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });
    
    const result = await tmfOdaService.fetchJourneys();
    expect(result).toEqual(mockData);
  });
});
```

### 10.4 E2E Testing with Playwright
```typescript
// e2e/alert-engine.spec.ts
import { test, expect } from '@playwright/test';

test('should navigate to alert engine and view correlations', async ({ page }) => {
  await page.goto('/alert-engine');
  await page.click('text=Alarm Correlation');
  await expect(page.locator('.correlation-table')).toBeVisible();
});
```

### 10.5 Test Coverage Requirements
- **Minimum 80% code coverage**
- **100% coverage for critical paths**
- **All API integrations must be tested**
- **All user interactions must be tested**

### 10.6 Testing Commands
```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:watch": "vitest --watch"
  }
}
```

## Additional Standards

### Performance Optimization
- **Code splitting**: Use dynamic imports for large components
- **Lazy loading**: Implement React.lazy() for routes
- **Memoization**: Use React.memo, useMemo, useCallback
- **Virtual scrolling**: For large lists
- **Image optimization**: Use WebP, lazy load images

### Accessibility (a11y)
- **Semantic HTML**: Use proper HTML elements
- **ARIA labels**: Add for interactive elements
- **Keyboard navigation**: Ensure all features are keyboard accessible
- **Color contrast**: Meet WCAG AA standards
- **Screen reader support**: Test with screen readers

### Security
- **Input validation**: Validate all user inputs
- **XSS prevention**: Sanitize rendered content
- **CSP headers**: Configure Content Security Policy
- **Secure storage**: Use secure methods for sensitive data
- **API security**: Implement proper authentication/authorization

### Monitoring and Analytics
- **Error tracking**: Integrate Sentry or similar
- **Performance monitoring**: Use Web Vitals
- **User analytics**: Implement Google Analytics or similar
- **Custom metrics**: Track business-specific KPIs
- **Logging**: Implement structured logging

### Documentation
- **README**: Comprehensive project documentation
- **API documentation**: Document all service methods
- **Component documentation**: Use Storybook or similar
- **Inline comments**: Explain complex logic
- **Type definitions**: Document interfaces and types

---

## Checklist for New Features

When implementing new features, verify:

- [ ] Follows project structure standards
- [ ] TypeScript types defined for all data
- [ ] Component follows architectural pattern
- [ ] Services created for API integration
- [ ] Error handling implemented
- [ ] Loading and error states handled
- [ ] Responsive design tested
- [ ] Authentication/authorization checked
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests for API calls
- [ ] E2E tests for user flows
- [ ] Accessibility standards met
- [ ] Performance optimized
- [ ] Security considerations addressed
- [ ] Documentation updated
- [ ] Code reviewed and approved
- [ ] Deployed to staging for testing
- [ ] Production deployment completed

---

Remember: These standards ensure consistency, maintainability, and quality across all UI development. Always refer to the alert-engine-ui project as the reference implementation for these patterns.