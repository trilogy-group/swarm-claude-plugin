---
alwaysApply: true
---
#####
Title: API Development Standards and Guidelines

Applies to: All Backend API Development Tasks

Rule:
You will develop backend APIs following these comprehensive standards, patterns, and processes derived from the promodeagro-ecommerce-api project structure and industry best practices.

## 🚨 CRITICAL: Implementation Methodology

### The Standard API Development Process

**The standard way of developing APIs is to follow this strict methodology:**

1. **First: Study the CLI Scripts** 
   - Navigate to the `python-scripts/` directory in your project
   - Thoroughly understand each CLI script (e.g., `products_cli.py`, `customer_portal.py`, `warehouse_manager_portal.py`)
   - These scripts are the **source of truth** for all business logic and data management patterns

2. **Second: Understand Database Operations**
   - Analyze how each CLI script interacts with DynamoDB tables
   - Study the data models, validation rules, and business constraints
   - Document the exact database operations performed for each function
   - Pay special attention to:
     - Table schemas and relationships
     - Data transformation logic
     - Transaction patterns
     - Error handling approaches
     - Status management workflows

3. **Third: Read the API Specification**
   - Open `/doc/api-spec/openapi-3.1.0.yaml`
   - Understand the API contracts, request/response formats, and endpoints
   - Map each API endpoint to its corresponding CLI function

4. **Fourth: Implement APIs to Match CLI Behavior**
   - Your API implementation must **exactly replicate** how the CLI scripts manage data
   - Do not deviate from the CLI's database operations
   - Maintain the same validation rules, business logic, and data transformations
   - Example mapping:
     ```
     CLI Function                    →  API Endpoint
     products_cli.create_product()   →  POST /products
     products_cli.list_products()    →  GET /products
     products_cli.update_product()   →  PUT /products/{id}
     ```

### Implementation Example

```javascript
// ❌ WRONG: Creating your own logic
async createProduct(data) {
  // Don't invent your own validation or business rules
  const product = {
    id: generateId(),
    ...data
  };
  await dynamoDB.put(product);
}

// ✅ CORRECT: Following CLI script logic exactly
async createProduct(data) {
  // Mirror the products_cli.py create_product() function exactly
  
  // 1. Validate using same rules as CLI
  const validationErrors = this.validateProductInput(data); // Same validation as CLI
  
  // 2. Check category exists (as CLI does)
  const category = await this.getCategoryById(data.categoryId);
  if (!category) {
    throw new Error('Category not found');
  }
  
  // 3. Generate ID using same pattern as CLI
  const productId = `prod_${uuid.v4()}`;
  
  // 4. Calculate status same way as CLI
  const status = this.calculateProductStatus(data.stock, data.lowStockAlert);
  
  // 5. Create product object with exact same fields as CLI
  const product = {
    id: productId,
    name: data.name,
    categoryId: data.categoryId,
    categoryName: category.name,
    // ... exact same fields as in CLI
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  
  // 6. Save to database using same method as CLI
  await this.products_table.put({ Item: product });
  
  return product;
}
```

### Key Principles

- **CLI Scripts are Law**: The Python CLI scripts define the canonical way to interact with the database
- **No Improvisation**: Do not create alternative implementations or "improvements"
- **Exact Replication**: Your APIs must produce identical database states as the CLI operations
- **Validation Parity**: Use the same validation rules, error messages, and constraints
- **Business Logic Consistency**: Implement the exact same business rules and workflows

### Directory Structure Reference

```
project-root/
├── python-scripts/           # 📌 START HERE - Source of truth
│   ├── products_cli.py       # Product management logic
│   ├── customer_portal.py    # Customer operations
│   ├── warehouse_manager_portal.py  # Inventory management
│   ├── super_admin_portal.py # Admin operations
│   ├── supplier_portal.py    # Supplier management
│   └── delivery_portal.py    # Delivery operations
├── doc/
│   └── api-spec/
│       └── openapi-3.1.0.yaml  # 📌 API contracts to implement
└── [your API implementation]    # Must match CLI behavior exactly
```

---

## 1. Project Structure

### 1.1 Standard Directory Organization
Every API project must follow this standardized directory structure:

```
project-root/
├── handlers/           # Lambda function handlers (entry points)
├── services/           # Business logic layer
├── database/           # Database access layer
│   ├── models/         # Data models/schemas
│   ├── queries/        # Database queries
│   └── migrations/     # Schema migrations
├── utils/              # Utility functions
│   ├── logger/         # Logging utilities
│   ├── errorHandler/   # Error handling
│   └── validators/     # Input validation
├── middleware/         # API middleware
│   ├── auth/           # Authentication middleware
│   └── cors/           # CORS configuration
├── config/             # Configuration files
├── tests/              # Test files
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end tests
├── scripts/            # Deployment and utility scripts
├── doc/                # API documentation
└── serverless.yml      # Serverless framework config
```

### 1.2 Module-Based Organization for Large APIs
For APIs with multiple domains, use module-based organization:

```
project-root/
├── products/
│   ├── handlers/       # Product-specific handlers
│   ├── services/       # Product business logic
│   ├── database/       # Product data access
│   ├── tests/          # Product tests
│   └── function.yml    # Product functions config
├── orders/
│   ├── handlers/
│   ├── services/
│   └── function.yml
├── users/
│   ├── handlers/
│   ├── services/
│   └── function.yml
└── serverless.yml      # Main serverless config
```

### 1.3 File Naming Conventions
- **Handlers**: camelCase with descriptive action (e.g., `createProduct.js`, `listOrders.js`)
- **Services**: PascalCase for classes, camelCase for files (e.g., `productService.js`)
- **Database**: camelCase with descriptive suffix (e.g., `queries.js`, `dynamodb.js`)
- **Utils**: camelCase (e.g., `responseFormatter.js`, `errorHandler.js`)
- **Config**: lowercase with hyphens (e.g., `database-config.js`)
- **Tests**: match source file with `.test.js` suffix (e.g., `createProduct.test.js`)

## 2. API Architecture Patterns

### 2.1 Three-Layer Architecture
Every API must implement clean separation of concerns:

```javascript
// 1. Handler Layer (Entry Point)
// handlers/createProduct.js
module.exports.handler = async (event) => {
  try {
    const data = JSON.parse(event.body);
    const product = await ProductService.createProduct(data);
    return ResponseFormatter.created(product);
  } catch (error) {
    return ErrorHandler.handle(error);
  }
};

// 2. Service Layer (Business Logic)
// services/productService.js
class ProductService {
  static async createProduct(data) {
    // Validate input
    const errors = ProductValidator.validate(data);
    if (errors.length > 0) {
      throw new ValidationError(errors);
    }
    
    // Apply business rules
    const processedData = this.applyBusinessRules(data);
    
    // Save to database
    return await ProductRepository.create(processedData);
  }
}

// 3. Data Access Layer (Database)
// database/productRepository.js
class ProductRepository {
  static async create(data) {
    const params = {
      TableName: process.env.PRODUCTS_TABLE,
      Item: {
        id: generateId(),
        ...data,
        createdAt: new Date().toISOString(),
      }
    };
    
    await dynamoDB.put(params).promise();
    return params.Item;
  }
}
```

### 2.2 Request/Response Flow
```
Request → Handler → Middleware → Service → Repository → Database
                                     ↓
Response ← Formatter ← Service ← Repository ←
```

### 2.3 Error Handling Pattern
Implement centralized error handling:

```javascript
// utils/errorHandler.js
class ErrorHandler {
  static ERROR_CODES = {
    VALIDATION_ERROR: { status: 400, code: 'VALIDATION_ERROR' },
    NOT_FOUND: { status: 404, code: 'NOT_FOUND' },
    UNAUTHORIZED: { status: 401, code: 'UNAUTHORIZED' },
    FORBIDDEN: { status: 403, code: 'FORBIDDEN' },
    CONFLICT: { status: 409, code: 'CONFLICT' },
    INTERNAL_ERROR: { status: 500, code: 'INTERNAL_ERROR' },
  };

  static handle(error) {
    const errorConfig = this.ERROR_CODES[error.code] || this.ERROR_CODES.INTERNAL_ERROR;
    
    return {
      statusCode: errorConfig.status,
      headers: this.getCorsHeaders(),
      body: JSON.stringify({
        status: 'error',
        code: errorConfig.code,
        message: error.message,
        timestamp: new Date().toISOString(),
      })
    };
  }
}
```

## 3. Serverless Configuration

### 3.1 Standard serverless.yml Structure
```yaml
service: api-service-name

frameworkVersion: "4"

provider:
  name: aws
  stage: ${opt:stage, 'dev'}
  region: ${opt:region, 'us-east-1'}
  runtime: nodejs18.x
  timeout: 29
  memorySize: 512
  
  # Environment variables
  environment:
    STAGE: ${self:provider.stage}
    NODE_ENV: ${self:provider.stage}
    REGION: ${self:provider.region}
    
  # IAM permissions
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:*
          Resource:
            - "arn:aws:dynamodb:${self:provider.region}:*:table/*"
            
  # API Gateway configuration
  httpApi:
    cors:
      allowedOrigins:
        - "*"
      allowedHeaders:
        - "*"
      allowedMethods:
        - OPTIONS
        - GET
        - POST
        - PUT
        - DELETE
        - PATCH

functions:
  - ${file(modules/products/function.yml)}
  - ${file(modules/orders/function.yml)}
  - ${file(modules/users/function.yml)}

resources:
  - ${file(resources/dynamodb.yml)}
  - ${file(resources/s3.yml)}
  - ${file(resources/cognito.yml)}
```

### 3.2 Function Configuration
```yaml
# modules/products/function.yml
createProduct:
  handler: products/handlers/createProduct.handler
  events:
    - httpApi:
        path: /products
        method: post
        authorizer: ${self:custom.authorizer}

listProducts:
  handler: products/handlers/listProducts.handler
  events:
    - httpApi:
        path: /products
        method: get
        
getProduct:
  handler: products/handlers/getProduct.handler
  events:
    - httpApi:
        path: /products/{id}
        method: get
```

## 4. API Standards and Patterns

### 4.1 RESTful API Design
Follow REST principles:

```
GET    /resources       - List all resources
GET    /resources/{id}  - Get specific resource
POST   /resources       - Create new resource
PUT    /resources/{id}  - Update entire resource
PATCH  /resources/{id}  - Partial update
DELETE /resources/{id}  - Delete resource
```

### 4.2 Request Validation
Implement comprehensive input validation:

```javascript
// services/validators/productValidator.js
class ProductValidator {
  static validateProductInput(data) {
    const errors = [];
    
    // Required fields
    if (!data.name) {
      errors.push({
        field: 'name',
        message: 'Product name is required'
      });
    }
    
    // Field types
    if (data.price && typeof data.price !== 'number') {
      errors.push({
        field: 'price',
        message: 'Price must be a number'
      });
    }
    
    // Business rules
    if (data.price && data.price < 0) {
      errors.push({
        field: 'price',
        message: 'Price cannot be negative'
      });
    }
    
    return errors;
  }
}
```

### 4.3 Response Format Standardization
Consistent response structure across all endpoints:

```javascript
// Success Response
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operation completed successfully",
  "meta": {
    "timestamp": "2024-01-01T12:00:00Z",
    "requestId": "req_123456",
    "version": "1.0.0"
  }
}

// Paginated Response
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5,
    "hasNextPage": true,
    "hasPrevPage": false
  },
  "message": "Resources retrieved successfully"
}

// Error Response
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 4.4 Status Codes
Use appropriate HTTP status codes:

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server errors
- **502 Bad Gateway**: External service errors
- **503 Service Unavailable**: Service temporarily unavailable

## 5. Authentication and Authorization

### 5.1 JWT-Based Authentication
Implement JWT authentication:

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

class AuthMiddleware {
  static async authenticate(event) {
    const token = this.extractToken(event.headers);
    
    if (!token) {
      throw new UnauthorizedError('No token provided');
    }
    
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      return decoded;
    } catch (error) {
      throw new UnauthorizedError('Invalid token');
    }
  }
  
  static extractToken(headers) {
    const authorization = headers.Authorization || headers.authorization;
    if (authorization && authorization.startsWith('Bearer ')) {
      return authorization.substring(7);
    }
    return null;
  }
}
```

### 5.2 Lambda Authorizer
Implement custom authorizer for API Gateway:

```javascript
// authorizers/customAuthorizer.js
exports.handler = async (event) => {
  try {
    const token = event.headers.Authorization.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    return {
      principalId: decoded.userId,
      policyDocument: {
        Version: '2012-10-17',
        Statement: [{
          Action: 'execute-api:Invoke',
          Effect: 'Allow',
          Resource: event.methodArn
        }]
      },
      context: {
        userId: decoded.userId,
        role: decoded.role
      }
    };
  } catch (error) {
    throw new Error('Unauthorized');
  }
};
```

### 5.3 Role-Based Access Control (RBAC)
Implement role-based permissions:

```javascript
// services/rbacService.js
class RBACService {
  static PERMISSIONS = {
    'admin': ['*'],
    'manager': ['products:*', 'orders:*', 'users:read'],
    'user': ['products:read', 'orders:create', 'orders:read:own'],
  };
  
  static hasPermission(userRole, resource, action) {
    const permissions = this.PERMISSIONS[userRole] || [];
    
    return permissions.some(permission => {
      if (permission === '*') return true;
      if (permission === `${resource}:*`) return true;
      if (permission === `${resource}:${action}`) return true;
      return false;
    });
  }
}
```

## 6. Database Patterns

### 6.1 DynamoDB Best Practices
```javascript
// database/dynamodb.js
const AWS = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient } = require('@aws-sdk/lib-dynamodb');

const client = new AWS.DynamoDBClient({
  region: process.env.REGION,
  endpoint: process.env.DYNAMODB_ENDPOINT, // For local development
});

const dynamoDB = DynamoDBDocumentClient.from(client);

// Single Table Design Pattern
class DynamoDBRepository {
  constructor(tableName) {
    this.tableName = tableName;
  }
  
  async create(item) {
    const params = {
      TableName: this.tableName,
      Item: {
        ...item,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
      ConditionExpression: 'attribute_not_exists(id)',
    };
    
    await dynamoDB.put(params);
    return params.Item;
  }
  
  async findById(id) {
    const params = {
      TableName: this.tableName,
      Key: { id },
    };
    
    const result = await dynamoDB.get(params);
    return result.Item;
  }
  
  async update(id, updates) {
    const updateExpression = this.buildUpdateExpression(updates);
    
    const params = {
      TableName: this.tableName,
      Key: { id },
      UpdateExpression: updateExpression.expression,
      ExpressionAttributeValues: updateExpression.values,
      ReturnValues: 'ALL_NEW',
    };
    
    const result = await dynamoDB.update(params);
    return result.Attributes;
  }
}
```

### 6.2 Database Transactions
```javascript
// Implement atomic operations
async createOrderWithInventoryUpdate(orderData, inventoryUpdates) {
  const transactItems = [
    {
      Put: {
        TableName: 'Orders',
        Item: orderData,
      }
    },
    ...inventoryUpdates.map(update => ({
      Update: {
        TableName: 'Inventory',
        Key: { productId: update.productId },
        UpdateExpression: 'SET stock = stock - :qty',
        ExpressionAttributeValues: {
          ':qty': update.quantity,
        },
        ConditionExpression: 'stock >= :qty',
      }
    }))
  ];
  
  await dynamoDB.transactWrite({ TransactItems: transactItems });
}
```

## 7. Testing Standards

### 7.1 Test Structure
```javascript
// tests/unit/productService.test.js
describe('ProductService', () => {
  describe('createProduct', () => {
    it('should create product with valid data', async () => {
      const productData = {
        name: 'Test Product',
        price: 99.99,
      };
      
      const product = await ProductService.createProduct(productData);
      
      expect(product).toHaveProperty('id');
      expect(product.name).toBe(productData.name);
      expect(product.price).toBe(productData.price);
    });
    
    it('should throw validation error for invalid data', async () => {
      const invalidData = {
        name: '',
        price: -10,
      };
      
      await expect(ProductService.createProduct(invalidData))
        .rejects.toThrow('VALIDATION_ERROR');
    });
  });
});
```

### 7.2 Integration Testing
```javascript
// tests/integration/createProduct.integration.test.js
const request = require('supertest');
const app = require('../../../app');

describe('POST /products', () => {
  it('should create new product', async () => {
    const response = await request(app)
      .post('/products')
      .send({
        name: 'Integration Test Product',
        price: 49.99,
      })
      .expect(201);
      
    expect(response.body.status).toBe('success');
    expect(response.body.data).toHaveProperty('id');
  });
  
  it('should return 400 for invalid input', async () => {
    const response = await request(app)
      .post('/products')
      .send({})
      .expect(400);
      
    expect(response.body.status).toBe('error');
    expect(response.body.code).toBe('VALIDATION_ERROR');
  });
});
```

### 7.3 Test Coverage Requirements
- **Minimum 80% code coverage**
- **100% coverage for critical paths**
- **All API endpoints must have integration tests**
- **All service methods must have unit tests**
- **Error scenarios must be tested**

## 8. Logging and Monitoring

### 8.1 Structured Logging
```javascript
// utils/logger.js
class Logger {
  static log(level, message, meta = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...meta,
      environment: process.env.NODE_ENV,
      service: process.env.SERVICE_NAME,
    };
    
    console.log(JSON.stringify(logEntry));
  }
  
  static info(message, meta) {
    this.log('INFO', message, meta);
  }
  
  static error(message, error, meta) {
    this.log('ERROR', message, {
      ...meta,
      error: {
        message: error.message,
        stack: error.stack,
        code: error.code,
      }
    });
  }
  
  static logRequest(method, path, body) {
    this.info('API Request', {
      method,
      path,
      body: this.sanitizeBody(body),
    });
  }
  
  static logResponse(method, path, statusCode, duration) {
    this.info('API Response', {
      method,
      path,
      statusCode,
      duration: `${duration}ms`,
    });
  }
}
```

### 8.2 Performance Monitoring
```javascript
// middleware/performanceMonitor.js
class PerformanceMonitor {
  static async monitor(handler) {
    const startTime = Date.now();
    const startMemory = process.memoryUsage().heapUsed;
    
    try {
      const result = await handler();
      
      const duration = Date.now() - startTime;
      const memoryUsed = process.memoryUsage().heapUsed - startMemory;
      
      Logger.info('Performance metrics', {
        duration: `${duration}ms`,
        memoryUsed: `${memoryUsed / 1024 / 1024}MB`,
      });
      
      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      Logger.error('Request failed', error, { duration });
      throw error;
    }
  }
}
```

## 9. Security Best Practices

### 9.1 Input Sanitization
```javascript
// utils/sanitizer.js
class Sanitizer {
  static sanitizeInput(data) {
    if (typeof data === 'string') {
      return this.sanitizeString(data);
    }
    
    if (Array.isArray(data)) {
      return data.map(item => this.sanitizeInput(item));
    }
    
    if (typeof data === 'object' && data !== null) {
      const sanitized = {};
      for (const [key, value] of Object.entries(data)) {
        sanitized[key] = this.sanitizeInput(value);
      }
      return sanitized;
    }
    
    return data;
  }
  
  static sanitizeString(str) {
    return str
      .replace(/[<>]/g, '') // Remove HTML tags
      .replace(/javascript:/gi, '') // Remove javascript: protocol
      .trim();
  }
}
```

### 9.2 Rate Limiting
```javascript
// middleware/rateLimiter.js
class RateLimiter {
  static async checkLimit(userId, endpoint) {
    const key = `rate_limit:${userId}:${endpoint}`;
    const limit = 100; // requests per minute
    const window = 60; // seconds
    
    const count = await redis.incr(key);
    
    if (count === 1) {
      await redis.expire(key, window);
    }
    
    if (count > limit) {
      throw new TooManyRequestsError('Rate limit exceeded');
    }
    
    return {
      limit,
      remaining: limit - count,
      reset: await redis.ttl(key),
    };
  }
}
```

### 9.3 API Key Management
```javascript
// Use AWS Secrets Manager
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

class SecretsManager {
  static async getSecret(secretName) {
    const client = new SecretsManagerClient({ region: process.env.REGION });
    
    try {
      const command = new GetSecretValueCommand({ SecretId: secretName });
      const response = await client.send(command);
      
      if (response.SecretString) {
        return JSON.parse(response.SecretString);
      }
      
      return Buffer.from(response.SecretBinary, 'base64').toString('ascii');
    } catch (error) {
      Logger.error('Failed to retrieve secret', error, { secretName });
      throw error;
    }
  }
}
```

## 10. External Service Integration

### 10.1 Payment Gateway Integration
```javascript
// services/payment/razorpayService.js
const Razorpay = require('razorpay');

class RazorpayService {
  constructor() {
    this.client = new Razorpay({
      key_id: process.env.RAZORPAY_KEY_ID,
      key_secret: process.env.RAZORPAY_KEY_SECRET,
    });
  }
  
  async createPaymentOrder(amount, currency = 'INR') {
    try {
      const options = {
        amount: amount * 100, // Convert to paise
        currency,
        receipt: `receipt_${Date.now()}`,
        payment_capture: 1,
      };
      
      const order = await this.client.orders.create(options);
      
      Logger.info('Payment order created', {
        orderId: order.id,
        amount: order.amount,
      });
      
      return order;
    } catch (error) {
      Logger.error('Payment order creation failed', error);
      throw new PaymentError('Failed to create payment order');
    }
  }
  
  verifyWebhookSignature(body, signature) {
    const expectedSignature = crypto
      .createHmac('sha256', process.env.RAZORPAY_WEBHOOK_SECRET)
      .update(JSON.stringify(body))
      .digest('hex');
      
    return signature === expectedSignature;
  }
}
```

### 10.2 Notification Service
```javascript
// services/notification/whatsappService.js
class WhatsAppService {
  async sendMessage(phoneNumber, message) {
    const apiUrl = process.env.WHATSAPP_API_URL;
    const apiKey = process.env.WHATSAPP_API_KEY;
    
    try {
      const response = await axios.post(apiUrl, {
        to: phoneNumber,
        message: message,
        type: 'text',
      }, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        }
      });
      
      Logger.info('WhatsApp message sent', {
        phoneNumber,
        messageId: response.data.id,
      });
      
      return response.data;
    } catch (error) {
      Logger.error('WhatsApp message failed', error, { phoneNumber });
      throw new NotificationError('Failed to send WhatsApp message');
    }
  }
}
```

## 11. Deployment and CI/CD

### 11.1 Environment Configuration
```bash
# .env.development
NODE_ENV=development
API_BASE_URL=http://localhost:3000
DYNAMODB_ENDPOINT=http://localhost:8000

# .env.staging
NODE_ENV=staging
API_BASE_URL=https://staging-api.example.com

# .env.production
NODE_ENV=production
API_BASE_URL=https://api.example.com
```

### 11.2 Deployment Scripts
```json
// package.json
{
  "scripts": {
    "deploy:dev": "serverless deploy --stage dev",
    "deploy:staging": "serverless deploy --stage staging",
    "deploy:prod": "serverless deploy --stage prod",
    "remove:dev": "serverless remove --stage dev",
    "logs": "serverless logs -f",
    "test": "jest",
    "test:coverage": "jest --coverage",
    "lint": "eslint .",
    "validate": "serverless validate"
  }
}
```

### 11.3 GitHub Actions CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy API

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm ci
      - name: Deploy to Production
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: npm run deploy:prod
```

## 12. API Documentation

### 12.1 OpenAPI/Swagger Specification
```yaml
# api-spec.yaml
openapi: 3.0.0
info:
  title: E-commerce API
  version: 1.0.0
  description: RESTful API for e-commerce platform

servers:
  - url: https://api.example.com
    description: Production server
  - url: https://staging-api.example.com
    description: Staging server

paths:
  /products:
    get:
      summary: List all products
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
        - in: query
          name: limit
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductList'
                
    post:
      summary: Create new product
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProductInput'
      responses:
        '201':
          description: Product created successfully

components:
  schemas:
    Product:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        price:
          type: number
```

### 12.2 API Documentation Template
```markdown
# API Endpoint: [Endpoint Name]

## Description
Brief description of what the endpoint does.

## Method
- **Method**: POST/GET/PUT/DELETE

## URL
- **URL**: `https://api.example.com/endpoint`

## Headers
- **Authorization**: Bearer {token}
- **Content-Type**: application/json

## Request Body
\`\`\`json
{
  "field1": "string",
  "field2": "number"
}
\`\`\`

## Response
### Success (200/201)
\`\`\`json
{
  "status": "success",
  "data": {},
  "message": "Success message"
}
\`\`\`

### Error (400/404/500)
\`\`\`json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Error message"
}
\`\`\`

## Example
\`\`\`bash
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value1"}'
\`\`\`
```

## Checklist for New API Development

When implementing new APIs, verify:

- [ ] **CLI script studied and understood for the relevant domain**
- [ ] **Database operations match CLI script implementation exactly**
- [ ] **OpenAPI specification reviewed for endpoint contract**
- [ ] Follows project structure standards
- [ ] Three-layer architecture implemented (Handler → Service → Repository)
- [ ] Input validation matches CLI script validation
- [ ] Error handling with proper status codes
- [ ] Authentication/authorization configured
- [ ] Request/response logging added
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests for endpoints
- [ ] API documentation updated
- [ ] OpenAPI specification updated
- [ ] Security headers configured
- [ ] CORS settings configured
- [ ] Rate limiting implemented (if needed)
- [ ] Database indexes optimized
- [ ] Performance monitoring added
- [ ] Deployment scripts updated
- [ ] Environment variables documented
- [ ] Code reviewed and approved
- [ ] Deployed to staging for testing
- [ ] Load testing performed
- [ ] Production deployment completed

---

Remember: These standards ensure consistency, maintainability, scalability, and security across all API development. Always refer to the promodeagro-ecommerce-api project as the reference implementation for these patterns.
