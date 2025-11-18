---
alwaysApply: true
---
## Backend MCP Server Response Format Standard

### Rule 1: MCP API Response Structure
All MCP server endpoints MUST return responses in this exact format:

```typescript
{
  "result": {
    "status": "success" | "error",
    "message": string,
    "operation": string,
    "data": any,
    "metadata": {
      "total_count": number,
      "page": number,
      "page_size": number,
      "timestamp": ISO8601_string
    }
  },
  "timestamp": ISO8601_string
}
```

**Success Response Example:**
```json
{
  "result": {
    "status": "success",
    "message": "Found 51 journeys",
    "operation": "list_journeys",
    "data": [...],
    "metadata": {
      "total_count": 51
    }
  },
  "timestamp": "2025-10-11T16:45:06Z"
}
```

**Error Response Example:**
```json
{
  "result": {
    "status": "error",
    "message": "Journey not found",
    "operation": "read_journey",
    "error_code": "NOT_FOUND",
    "error_details": {}
  },
  "timestamp": "2025-10-11T16:45:06Z"
}
```

### Rule 2: Backend Field Naming Convention
- Use **camelCase** for all field names in API responses
- Journey ID field MUST be: `journeyId` (not `journey_id` or `JourneyId`)
- Status field MUST be: `status` (lowercase)
- Created/Updated timestamps MUST be: `createdAt`, `updatedAt` (ISO 8601 format)
- Current stage MUST be: `currentStageId`

**Example Journey Object:**
```typescript
{
  "journeyId": "JRN-ABC123",
  "name": "Journey Name",
  "status": "pending" | "running" | "completed" | "failed" | "paused" | "cancelled",
  "priority": "low" | "medium" | "high" | "critical",
  "odaComponentType": string,
  "overallProgress": number,  // 0-100
  "currentStageId": string,
  "createdAt": "2025-10-11T10:34:21.333919Z",
  "updatedAt": "2025-10-11T10:34:21.333919Z",
  "createdBy": string,
  "description": string
}
```

### Rule 3: Backend CORS Configuration
All backend servers MUST configure CORS to allow frontend origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://10.0.0.3:8080",
        # Add production origins
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)
```

**CRITICAL:** CORS middleware MUST be added BEFORE any other middleware or routes.

---

## UI Frontend Data Parsing Standard

### Rule 4: HTTP Service Layer Pattern
All API calls MUST go through a centralized HTTP service (`tmfOdaHttpService.ts`):

```typescript
// In tmfOdaHttpService.ts
async fetchJourneys(journeyId?: string): Promise<any> {
  const response = await fetch(`${this.baseUrl}/tools/journeys_tool`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({action: journeyId ? 'read' : 'list', journey_id: journeyId}),
    signal: AbortSignal.timeout(this.timeout),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
  }

  const result = await response.json();
  
  // Return the inner 'result' object
  if (result.result) {
    return result.result;
  }
  return result;
}
```

**IMPORTANT:** The HTTP service extracts `result.result` and returns it, so consumers receive the inner object directly.

### Rule 5: Service Layer Data Access Pattern
Business logic services MUST access data from HTTP service responses correctly:

```typescript
// In transformationJourneyService.ts
private async refreshJourneysFromAPI(): Promise<void> {
  const apiResponse = await tmfOdaHttpService.fetchJourneys();
  
  // ✅ CORRECT: Access data directly
  if (apiResponse && apiResponse.status === 'success') {
    const journeys = apiResponse.data;
  }
  
  // ❌ WRONG: Don't add extra .result
  // if (apiResponse && apiResponse.result.status === 'success') {
}
```

**Key Point:** Since HTTP service returns `result.result`, the service layer accesses:
- `apiResponse.status` NOT `apiResponse.result.status`
- `apiResponse.data` NOT `apiResponse.result.data`
- `apiResponse.metadata` NOT `apiResponse.result.metadata`

### Rule 6: Type Safety and Validation
Always define TypeScript interfaces for API responses:

```typescript
interface ApiResponse<T = any> {
  status: 'success' | 'error';
  message: string;
  operation: string;
  data?: T;
  metadata?: {
    total_count?: number;
    page?: number;
    page_size?: number;
  };
  error_code?: string;
  error_details?: any;
}

interface JourneyApiData {
  journeyId: string;
  name: string;
  status: string;
  priority: string;
  odaComponentType: string;
  overallProgress: number;
  currentStageId: string;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  description: string;
}
```

### Rule 7: Error Handling Pattern
Always handle both network errors and API errors:

```typescript
try {
  const response = await fetch(url, options);
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }
  
  const result = await response.json();
  
  if (result.result?.status === 'error') {
    throw new Error(result.result.message || 'API error');
  }
  
  return result.result;
  
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

### Rule 8: Environment Configuration
Always use environment variables for API URLs:

```typescript
// .env.local
VITE_TMF_ODA_API_BASE_URL=http://10.0.0.3:8000
VITE_TMF_ODA_API_TIMEOUT=30000

// In code
const baseUrl = import.meta.env.VITE_TMF_ODA_API_BASE_URL;
if (!baseUrl) {
  throw new Error('VITE_TMF_ODA_API_BASE_URL is not configured');
}
```

**NEVER** hardcode API URLs in source code.

---

## Data Transformation Standards

### Rule 9: API to UI Data Mapping
Always create explicit mapping functions:

```typescript
private convertApiJourneyToUiJourney(apiJourney: JourneyApiData): TransformationJourney {
  return {
    // Direct mappings
    id: apiJourney.journeyId,
    name: apiJourney.name,
    description: apiJourney.description,
    
    // Type conversions
    status: this.mapApiStatusToUiStatus(apiJourney.status),
    priority: apiJourney.priority as JourneyPriority,
    
    // Date conversions
    createdAt: new Date(apiJourney.createdAt),
    updatedAt: new Date(apiJourney.updatedAt),
    
    // Nested object construction
    source: {
      type: 'schema-based',
      schemaName: apiJourney.name,
      schemaVersion: '1.0.0'
    },
    
    // Defaults for missing fields
    overallProgress: apiJourney.overallProgress || 0,
  };
}

private mapApiStatusToUiStatus(apiStatus: string): JourneyStatus {
  const statusMap: Record<string, JourneyStatus> = {
    'pending': 'created',
    'running': 'running',
    'completed': 'completed',
    'failed': 'failed',
    'paused': 'paused',
    'cancelled': 'cancelled'
  };
  return statusMap[apiStatus.toLowerCase()] || 'created';
}
```

### Rule 10: Null Safety and Defaults
Always provide defaults for optional fields:

```typescript
// ✅ CORRECT: Provide defaults
const journeyName = apiJourney.name || 'Untitled Journey';
const progress = apiJourney.overallProgress ?? 0;
const createdAt = apiJourney.createdAt ? new Date(apiJourney.createdAt) : new Date();

// ❌ WRONG: Assume fields exist
const journeyName = apiJourney.name.toUpperCase(); // May crash if null
```

---

## Testing & Validation Standards

### Rule 11: API Contract Testing
Always validate backend responses match expected format:

```typescript
// Test script example
function validateApiResponse(response: any): void {
  assert(response.result, 'Response must have result property');
  assert(response.result.status, 'Result must have status property');
  assert(['success', 'error'].includes(response.result.status), 'Status must be success or error');
  
  if (response.result.status === 'success') {
    assert(response.result.data !== undefined, 'Success response must have data');
  }
  
  if (response.result.status === 'error') {
    assert(response.result.message, 'Error response must have message');
  }
}
```

### Rule 12: Use Test Scripts for Validation
Always run test scripts before deploying:

```bash
# Backend validation
cd /opt/mycode/trilogy/tmf-oda-transformer-ui/testscripts/journey-crud
./quick_test.sh http://10.0.0.3:8000

# Expected output:
# ✅ List action working - Found X journeys
# ✅ Create action working - Journey ID: JRN-xxx
# ✅ Read action working
# ✅ Delete action working
```

### Rule 13: Debug Utility Usage
Use the built-in debug utility to verify API integration:

```
http://localhost:8080/tools/debug-api
```

Expected results:
- ✅ Environment Configuration: Pass
- ✅ API Connectivity: Pass  
- ✅ CORS Preflight: Pass
- ✅ Journeys API: Pass

---

## Common Pitfalls to Avoid

### ❌ Don't: Access nested result twice
```typescript
// Wrong - adding extra .result
if (apiResponse.result.status === 'success') {
  const data = apiResponse.result.data;
}
```

### ✅ Do: Access result directly
```typescript
// Correct - apiResponse IS the result
if (apiResponse.status === 'success') {
  const data = apiResponse.data;
}
```

### ❌ Don't: Mix snake_case and camelCase
```typescript
// Backend sends: journey_id (inconsistent)
// Frontend expects: journeyId (camelCase)
```

### ✅ Do: Use consistent camelCase
```typescript
// Backend sends: journeyId
// Frontend expects: journeyId
```

### ❌ Don't: Hardcode API URLs
```typescript
const response = await fetch('http://localhost:8000/api/journeys');
```

### ✅ Do: Use environment variables
```typescript
const response = await fetch(`${this.baseUrl}/api/journeys`);
```

### ❌ Don't: Swallow errors silently
```typescript
try {
  await fetchData();
} catch (error) {
  // Silent failure
}
```

### ✅ Do: Log and propagate errors
```typescript
try {
  await fetchData();
} catch (error) {
  console.error('Failed to fetch data:', error);
  throw error; // Let caller handle it
}
```

---

## Checklist for New API Endpoints

When adding a new API endpoint, verify:

- [ ] Backend returns response in standard format (`result.status`, `result.data`)
- [ ] Backend uses camelCase for all field names
- [ ] Backend has CORS configured for frontend origin
- [ ] HTTP service extracts and returns `result.result`
- [ ] Service layer accesses `apiResponse.status` (not `apiResponse.result.status`)
- [ ] TypeScript interfaces defined for request/response
- [ ] Error handling covers network, timeout, and API errors
- [ ] Mapping functions convert API data to UI types
- [ ] Null safety with default values
- [ ] Test script validates the endpoint
- [ ] Debug utility can test the endpoint
- [ ] Environment variables used (no hardcoded URLs)

---

