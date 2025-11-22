---
alwaysApply: true
projectName: RealWorld Backend (Conduit API)
---
#####
Title: RealWorld Backend - Project-Specific Development Guidelines

Applies to: All Backend Development in the RealWorld (Conduit) API

Project: NestJS + MikroORM + MySQL Implementation

Rule:
You will develop and maintain the RealWorld backend API following these project-specific patterns and conventions established in the codebase.

## 1. Project Overview

### 1.1 Technology Stack
- **Framework**: NestJS 10.0.5
- **ORM**: MikroORM 5.7.14 with MySQL driver
- **Database**: MySQL
- **Authentication**: JWT with Passport
- **API Documentation**: Swagger/OpenAPI
- **Runtime**: Node.js with TypeScript 5.1.6
- **Development**: ts-node-dev for hot reloading

### 1.2 Application Structure
```
backend/
├── src/
│   ├── article/            # Article module
│   │   ├── article.controller.ts
│   │   ├── article.service.ts
│   │   ├── article.entity.ts
│   │   ├── article.interface.ts
│   │   ├── article.module.ts
│   │   ├── comment.entity.ts
│   │   └── dto/
│   ├── user/               # User module
│   │   ├── user.controller.ts
│   │   ├── user.service.ts
│   │   ├── user.entity.ts
│   │   ├── user.interface.ts
│   │   ├── user.module.ts
│   │   ├── user.decorator.ts
│   │   └── dto/
│   ├── profile/            # Profile module
│   │   ├── profile.controller.ts
│   │   ├── profile.service.ts
│   │   ├── profile.interface.ts
│   │   └── profile.module.ts
│   ├── tag/                # Tag module
│   │   ├── tag.controller.ts
│   │   ├── tag.service.ts
│   │   ├── tag.entity.ts
│   │   └── tag.module.ts
│   ├── shared/             # Shared utilities
│   │   └── pipes/
│   ├── migrations/         # Database migrations
│   ├── seeders/            # Database seeders
│   ├── app.controller.ts   # Root controller
│   ├── app.module.ts       # Root module
│   ├── config.ts           # Configuration
│   └── main.ts             # Application entry point
├── mikro-orm.config.ts     # MikroORM configuration
├── nest-cli.json           # NestJS CLI configuration
└── tsconfig.json           # TypeScript configuration
```

## 2. Module Architecture

### 2.1 Module Structure Pattern
Each feature follows NestJS module pattern:

```typescript
// article/article.module.ts
import { Module } from '@nestjs/common';
import { MikroOrmModule } from '@mikro-orm/nestjs';
import { ArticleController } from './article.controller';
import { ArticleService } from './article.service';
import { Article } from './article.entity';
import { Comment } from './comment.entity';
import { UserModule } from '../user/user.module';

@Module({
  imports: [
    MikroOrmModule.forFeature([Article, Comment]),
    UserModule,
  ],
  controllers: [ArticleController],
  providers: [ArticleService],
  exports: [ArticleService],
})
export class ArticleModule {}
```

### 2.2 Controller Pattern
Controllers handle HTTP requests and use decorators:

```typescript
// article/article.controller.ts
import { Body, Controller, Delete, Get, Param, Post, Put, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { User } from '../user/user.decorator';
import { IArticleRO, IArticlesRO } from './article.interface';
import { ArticleService } from './article.service';
import { CreateArticleDto, UpdateArticleDto } from './dto';

@ApiBearerAuth()
@ApiTags('articles')
@Controller('articles')
export class ArticleController {
  constructor(private readonly articleService: ArticleService) {}

  @ApiOperation({ summary: 'Get all articles' })
  @ApiResponse({ status: 200, description: 'Return all articles.' })
  @Get()
  async findAll(
    @User('id') userId: number,
    @Query() query: Record<string, string>
  ): Promise<IArticlesRO> {
    return this.articleService.findAll(+userId, query);
  }

  @ApiOperation({ summary: 'Create article' })
  @ApiResponse({ status: 201, description: 'The article has been successfully created.' })
  @Post()
  async create(
    @User('id') userId: number,
    @Body('article') articleData: CreateArticleDto
  ) {
    return this.articleService.create(userId, articleData);
  }

  @Put(':slug')
  async update(
    @User('id') userId: number,
    @Param('slug') slug: string,
    @Body('article') articleData: UpdateArticleDto
  ) {
    return this.articleService.update(userId, slug, articleData);
  }

  @Delete(':slug')
  async delete(@User('id') userId: number, @Param('slug') slug: string) {
    return this.articleService.delete(userId, slug);
  }
}
```

### 2.3 Service Pattern
Services contain business logic and database interactions:

```typescript
// article/article.service.ts
import { EntityManager, QueryOrder, wrap } from '@mikro-orm/core';
import { EntityRepository } from '@mikro-orm/mysql';
import { InjectRepository } from '@mikro-orm/nestjs';
import { Injectable } from '@nestjs/common';
import { User } from '../user/user.entity';
import { Article } from './article.entity';
import { IArticleRO, IArticlesRO } from './article.interface';

@Injectable()
export class ArticleService {
  constructor(
    private readonly em: EntityManager,
    @InjectRepository(Article)
    private readonly articleRepository: EntityRepository<Article>,
    @InjectRepository(User)
    private readonly userRepository: EntityRepository<User>,
  ) {}

  async findAll(userId: number, query: Record<string, string>): Promise<IArticlesRO> {
    const user = userId
      ? await this.userRepository.findOne(userId, { populate: ['followers', 'favorites'] })
      : undefined;
      
    const qb = this.articleRepository
      .createQueryBuilder('a')
      .select('a.*')
      .leftJoin('a.author', 'u');

    // Apply filters
    if ('tag' in query) {
      qb.andWhere({ tagList: new RegExp(query.tag) });
    }

    if ('author' in query) {
      const author = await this.userRepository.findOne({ username: query.author });
      qb.andWhere({ author: author.id });
    }

    // Pagination
    const res = await qb
      .orderBy({ createdAt: QueryOrder.DESC })
      .limit(+query.limit || 20)
      .offset(+query.offset || 0)
      .getResultAndCount();

    return { articles: res[0], articlesCount: res[1] };
  }

  async create(userId: number, dto: CreateArticleDto) {
    const user = await this.userRepository.findOne(userId);
    const article = new Article(user, dto.title, dto.description, dto.body);
    article.tagList = dto.tagList || [];
    
    await this.em.persistAndFlush(article);
    
    return { article: article.toJSON(user) };
  }
}
```

## 3. Database Layer (MikroORM)

### 3.1 Entity Definition
Entities use MikroORM decorators:

```typescript
// article/article.entity.ts
import {
  ArrayType,
  Collection,
  Entity,
  ManyToOne,
  OneToMany,
  PrimaryKey,
  Property,
  wrap,
} from '@mikro-orm/core';
import slug from 'slug';
import { User } from '../user/user.entity';
import { Comment } from './comment.entity';

@Entity()
export class Article {
  @PrimaryKey({ type: 'number' })
  id: number;

  @Property({ fieldName: 'slug' })
  slug: string;

  @Property({ fieldName: 'title' })
  title: string;

  @Property({ fieldName: 'description' })
  description = '';

  @Property({ fieldName: 'body' })
  body = '';

  @Property({ type: 'date', fieldName: 'created_at' })
  createdAt = new Date();

  @Property({ type: 'date', onUpdate: () => new Date(), fieldName: 'updated_at' })
  updatedAt = new Date();

  @Property({ type: ArrayType, fieldName: 'tag_list' })
  tagList: string[] = [];

  @ManyToOne(() => User, { fieldName: 'author_id' })
  author: User;

  @OneToMany(() => Comment, (comment) => comment.article, { eager: true, orphanRemoval: true })
  comments = new Collection<Comment>(this);

  @Property({ type: 'number', fieldName: 'favorites_count' })
  favoritesCount = 0;

  constructor(author: User, title: string, description: string, body: string) {
    this.author = author;
    this.title = title;
    this.description = description;
    this.body = body;
    this.slug = slug(title, { lower: true }) + '-' + ((Math.random() * Math.pow(36, 6)) | 0).toString(36);
  }

  toJSON(user?: User) {
    const o = wrap(this).toObject();
    o.favorited = user && user.favorites.isInitialized() ? user.favorites.contains(this) : false;
    o.author = this.author.toJSON(user);

    return o;
  }
}
```

### 3.2 MikroORM Configuration
```typescript
// mikro-orm.config.ts
import { MikroOrmModuleOptions } from '@mikro-orm/nestjs';
import { SqlHighlighter } from '@mikro-orm/sql-highlighter';

const config: MikroOrmModuleOptions = {
  type: 'mysql',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  dbName: process.env.DB_NAME || 'conduit',
  entities: ['dist/**/*.entity.js'],
  entitiesTs: ['src/**/*.entity.ts'],
  debug: true,
  highlighter: new SqlHighlighter(),
  migrations: {
    path: 'dist/migrations',
    pathTs: 'src/migrations',
  },
};

export default config;
```

### 3.3 Repository Pattern
Use MikroORM's EntityRepository:

```typescript
@Injectable()
export class ArticleService {
  constructor(
    @InjectRepository(Article)
    private readonly articleRepository: EntityRepository<Article>,
  ) {}

  async findBySlug(slug: string): Promise<Article> {
    return this.articleRepository.findOne({ slug });
  }

  async findWithAuthor(id: number): Promise<Article> {
    return this.articleRepository.findOne(id, { populate: ['author'] });
  }
}
```

## 4. Authentication & Authorization

### 4.1 JWT Strategy
JWT authentication using Passport:

```typescript
// user/jwt.strategy.ts
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { SECRET } from '../config';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderWithScheme('Token'),
      secretOrKey: SECRET,
    });
  }

  async validate(payload: any) {
    return {
      id: payload.id,
      username: payload.username,
      email: payload.email,
    };
  }
}
```

### 4.2 User Decorator
Custom decorator to extract user from request:

```typescript
// user/user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const User = createParamDecorator((data: string, ctx: ExecutionContext) => {
  const req = ctx.switchToHttp().getRequest();
  
  if (data) {
    return req.user && req.user[data];
  }

  return req.user;
});
```

### 4.3 Auth Middleware
Optional authentication middleware:

```typescript
// shared/auth.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import * as jwt from 'jsonwebtoken';
import { SECRET } from '../config';
import { UserService } from '../user/user.service';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(private readonly userService: UserService) {}

  async use(req: any, res: any, next: () => void) {
    const token = req.headers.authorization?.replace('Token ', '');
    
    if (token) {
      try {
        const decoded = jwt.verify(token, SECRET) as any;
        const user = await this.userService.findById(decoded.id);
        req.user = user;
      } catch (err) {
        // Invalid token, continue without user
      }
    }
    
    next();
  }
}
```

## 5. DTOs and Validation

### 5.1 DTO Pattern
Use class-validator for validation:

```typescript
// article/dto/create-article.dto.ts
import { IsNotEmpty, IsOptional, IsArray } from 'class-validator';

export class CreateArticleDto {
  @IsNotEmpty()
  readonly title: string;

  @IsNotEmpty()
  readonly description: string;

  @IsNotEmpty()
  readonly body: string;

  @IsOptional()
  @IsArray()
  readonly tagList?: string[];
}
```

### 5.2 Update DTOs
Partial DTOs for updates:

```typescript
// article/dto/update-article.dto.ts
import { IsOptional } from 'class-validator';

export class UpdateArticleDto {
  @IsOptional()
  readonly title?: string;

  @IsOptional()
  readonly description?: string;

  @IsOptional()
  readonly body?: string;
}
```

## 6. Response Interfaces

### 6.1 Standard Response Format
Define interfaces for API responses:

```typescript
// article/article.interface.ts
export interface IArticleData {
  slug: string;
  title: string;
  description: string;
  body: string;
  tagList: string[];
  createdAt: Date;
  updatedAt: Date;
  favorited: boolean;
  favoritesCount: number;
  author: IProfileData;
}

export interface IArticleRO {
  article: IArticleData;
}

export interface IArticlesRO {
  articles: IArticleData[];
  articlesCount: number;
}
```

## 7. API Documentation (Swagger)

### 7.1 Swagger Setup
Configure in main.ts:

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Swagger configuration
  const config = new DocumentBuilder()
    .setTitle('RealWorld API')
    .setDescription('The RealWorld API description')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
    
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);
  
  app.setGlobalPrefix('api');
  app.enableCors();
  
  await app.listen(3000);
}
```

### 7.2 Decorator Usage
Use Swagger decorators for documentation:

```typescript
@ApiBearerAuth()
@ApiTags('articles')
@Controller('articles')
export class ArticleController {
  @ApiOperation({ summary: 'Get all articles' })
  @ApiResponse({ status: 200, description: 'Return all articles.' })
  @Get()
  async findAll() { }
}
```

## 8. Database Migrations

### 8.1 Creating Migrations
```bash
npx mikro-orm migration:create
```

### 8.2 Migration Pattern
```typescript
// migrations/Migration20240101000000.ts
import { Migration } from '@mikro-orm/migrations';

export class Migration20240101000000 extends Migration {
  async up(): Promise<void> {
    this.addSql('CREATE TABLE `article` (...)');
  }

  async down(): Promise<void> {
    this.addSql('DROP TABLE `article`');
  }
}
```

### 8.3 Running Migrations
Migrations run automatically on app start:

```typescript
// app.module.ts
export class AppModule implements OnModuleInit {
  constructor(private readonly orm: MikroORM) {}

  async onModuleInit(): Promise<void> {
    await this.orm.getMigrator().up();
  }
}
```

## 9. Seeders

### 9.1 Seeder Configuration
```typescript
// seeders/DatabaseSeeder.ts
import { EntityManager } from '@mikro-orm/core';
import { Seeder } from '@mikro-orm/seeder';
import { User } from '../user/user.entity';
import { Article } from '../article/article.entity';

export class DatabaseSeeder extends Seeder {
  async run(em: EntityManager): Promise<void> {
    const user = em.create(User, {
      username: 'john',
      email: 'john@example.com',
      password: 'password',
    });

    const article = em.create(Article, {
      title: 'Sample Article',
      author: user,
      // ...
    });

    await em.flush();
  }
}
```

## 10. Error Handling

### 10.1 HTTP Exceptions
Use NestJS built-in exceptions:

```typescript
import { 
  BadRequestException,
  UnauthorizedException,
  NotFoundException,
  ForbiddenException,
  ConflictException 
} from '@nestjs/common';

// In service methods
async findOne(slug: string) {
  const article = await this.articleRepository.findOne({ slug });
  
  if (!article) {
    throw new NotFoundException('Article not found');
  }
  
  return article;
}

async create(userId: number, dto: CreateArticleDto) {
  const existing = await this.articleRepository.findOne({ title: dto.title });
  
  if (existing) {
    throw new ConflictException('Article with this title already exists');
  }
  
  // Create article...
}
```

### 10.2 Custom Exception Filters
```typescript
// shared/http-exception.filter.ts
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    const error = 
      typeof exceptionResponse === 'string'
        ? { message: exceptionResponse }
        : exceptionResponse;

    response.status(status).json({
      ...error,
      timestamp: new Date().toISOString(),
    });
  }
}
```

## 11. Development Workflow

### 11.1 Available Scripts
```bash
# Start development server with hot reload
npm run start

# Run database seeders
npm run seed

# Create new migration
npx mikro-orm migration:create

# Run migrations
npx mikro-orm migration:up
```

### 11.2 Environment Variables
```bash
# .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=conduit
JWT_SECRET=supersecret
```

## 12. Testing

### 12.1 Unit Testing Services
```typescript
// article/article.service.spec.ts
describe('ArticleService', () => {
  let service: ArticleService;
  let repository: EntityRepository<Article>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        ArticleService,
        {
          provide: getRepositoryToken(Article),
          useClass: Repository,
        },
      ],
    }).compile();

    service = module.get<ArticleService>(ArticleService);
    repository = module.get<EntityRepository<Article>>(getRepositoryToken(Article));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
```

### 12.2 E2E Testing
```typescript
// test/article.e2e-spec.ts
describe('ArticleController (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/articles (GET)', () => {
    return request(app.getHttpServer())
      .get('/articles')
      .expect(200)
      .expect((res) => {
        expect(res.body).toHaveProperty('articles');
        expect(res.body).toHaveProperty('articlesCount');
      });
  });
});
```

## Project-Specific Rules

1. **Always use MikroORM EntityManager** for database operations
2. **Follow NestJS module structure** - each feature is a module
3. **Use DTOs for all request/response validation**
4. **Implement proper error handling** with NestJS exceptions
5. **Use the custom User decorator** to get authenticated user
6. **All entities must have toJSON method** for response formatting
7. **Run migrations automatically** on application start
8. **Use QueryBuilder** for complex database queries
9. **Follow RealWorld API specification** exactly
10. **Maintain backward compatibility** with the RealWorld frontend

## Checklist for New Features

- [ ] Module created with proper imports/exports
- [ ] Entity defined with MikroORM decorators
- [ ] DTOs created with class-validator decorators
- [ ] Interface defined for response objects
- [ ] Service implements business logic
- [ ] Controller handles HTTP requests
- [ ] Swagger decorators added for documentation
- [ ] Error handling implemented
- [ ] Authentication/authorization configured
- [ ] Unit tests written for service
- [ ] E2E tests written for controller
- [ ] Migration created if database schema changed
- [ ] Module registered in AppModule

---

Remember: This is a RealWorld specification implementation. The API must be compatible with any RealWorld frontend and pass the RealWorld API test suite.
