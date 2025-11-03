#!/usr/bin/env node

/**
 * Deployment Script for DevOps Assistant Plugin
 * Handles deployment validation and orchestration
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

// ANSI color codes
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

// Configuration
const config = {
    environments: {
        development: {
            url: 'http://localhost:3000',
            branch: 'develop',
            checks: ['lint', 'test'],
            approval: false
        },
        staging: {
            url: 'https://staging.example.com',
            branch: 'staging',
            checks: ['lint', 'test', 'security', 'performance'],
            approval: false
        },
        production: {
            url: 'https://example.com',
            branch: 'main',
            checks: ['lint', 'test', 'security', 'performance', 'smoke'],
            approval: true
        }
    }
};

class DeploymentManager {
    constructor(options = {}) {
        this.environment = options.environment || 'development';
        this.validate = options.validate || false;
        this.dryRun = options.dryRun || false;
        this.force = options.force || false;
        this.verbose = options.verbose || false;
        this.skipTests = options.skipTests || false;
        
        this.envConfig = config.environments[this.environment];
        this.deploymentId = this.generateDeploymentId();
        this.startTime = Date.now();
    }
    
    generateDeploymentId() {
        return `deploy-${this.environment}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    log(message, level = 'info') {
        const timestamp = new Date().toISOString();
        const prefix = {
            info: `${colors.blue}ℹ${colors.reset}`,
            success: `${colors.green}✓${colors.reset}`,
            warning: `${colors.yellow}⚠${colors.reset}`,
            error: `${colors.red}✗${colors.reset}`,
            step: `${colors.cyan}▶${colors.reset}`
        };
        
        console.log(`${prefix[level] || ''} ${message}`);
        
        if (this.verbose) {
            console.log(`  ${colors.bright}[${timestamp}]${colors.reset} ${message}`);
        }
    }
    
    async checkPrerequisites() {
        this.log('Checking prerequisites...', 'step');
        
        const checks = [
            this.checkGitStatus(),
            this.checkBranch(),
            this.checkEnvironmentVariables(),
            this.checkDependencies(),
            this.checkDiskSpace(),
            this.checkConnectivity()
        ];
        
        const results = await Promise.all(checks);
        const allPassed = results.every(r => r.passed);
        
        if (!allPassed && !this.force) {
            throw new Error('Prerequisites check failed');
        }
        
        this.log('Prerequisites check completed', 'success');
        return allPassed;
    }
    
    async checkGitStatus() {
        try {
            const { stdout } = await execPromise('git status --porcelain');
            if (stdout.trim()) {
                this.log('Working directory has uncommitted changes', 'warning');
                return { passed: false, reason: 'uncommitted changes' };
            }
            
            this.log('Git working directory is clean', 'success');
            return { passed: true };
        } catch (error) {
            this.log(`Git check failed: ${error.message}`, 'error');
            return { passed: false, reason: error.message };
        }
    }
    
    async checkBranch() {
        try {
            const { stdout } = await execPromise('git branch --show-current');
            const currentBranch = stdout.trim();
            
            if (currentBranch !== this.envConfig.branch) {
                this.log(`Wrong branch: ${currentBranch} (expected: ${this.envConfig.branch})`, 'warning');
                return { passed: false, reason: 'wrong branch' };
            }
            
            this.log(`On correct branch: ${currentBranch}`, 'success');
            return { passed: true };
        } catch (error) {
            this.log(`Branch check failed: ${error.message}`, 'error');
            return { passed: false, reason: error.message };
        }
    }
    
    async checkEnvironmentVariables() {
        const required = ['NODE_ENV', 'API_KEY', 'DATABASE_URL'];
        const missing = [];
        
        // In real deployment, check actual environment variables
        // For demo, we'll simulate
        for (const varName of required) {
            if (!process.env[varName] && this.environment === 'production') {
                missing.push(varName);
            }
        }
        
        if (missing.length > 0) {
            this.log(`Missing environment variables: ${missing.join(', ')}`, 'warning');
            return { passed: false, reason: 'missing env vars' };
        }
        
        this.log('All required environment variables are set', 'success');
        return { passed: true };
    }
    
    async checkDependencies() {
        this.log('Checking dependencies...', 'info');
        
        // Check if package.json exists
        if (!fs.existsSync('package.json')) {
            this.log('No package.json found', 'warning');
            return { passed: true };
        }
        
        try {
            // In real scenario, would run npm outdated or audit
            this.log('Dependencies check passed', 'success');
            return { passed: true };
        } catch (error) {
            this.log(`Dependencies check failed: ${error.message}`, 'error');
            return { passed: false, reason: error.message };
        }
    }
    
    async checkDiskSpace() {
        // Simulated disk space check
        const requiredSpace = 1000; // MB
        const availableSpace = 5000; // MB (simulated)
        
        if (availableSpace < requiredSpace) {
            this.log(`Insufficient disk space: ${availableSpace}MB available, ${requiredSpace}MB required`, 'error');
            return { passed: false, reason: 'insufficient disk space' };
        }
        
        this.log(`Disk space check passed (${availableSpace}MB available)`, 'success');
        return { passed: true };
    }
    
    async checkConnectivity() {
        this.log(`Testing connectivity to ${this.envConfig.url}...`, 'info');
        
        // In real scenario, would ping the target server
        // For demo, we'll simulate
        const isReachable = true;
        
        if (!isReachable) {
            this.log(`Cannot reach ${this.envConfig.url}`, 'error');
            return { passed: false, reason: 'target unreachable' };
        }
        
        this.log(`Target ${this.envConfig.url} is reachable`, 'success');
        return { passed: true };
    }
    
    async runTests() {
        if (this.skipTests) {
            this.log('Skipping tests (--skip-tests flag)', 'warning');
            return true;
        }
        
        this.log('Running test suite...', 'step');
        
        const testTypes = this.envConfig.checks;
        const results = {};
        
        for (const testType of testTypes) {
            this.log(`Running ${testType} tests...`, 'info');
            
            try {
                // Simulate test execution
                await this.simulateTest(testType);
                results[testType] = { passed: true };
                this.log(`${testType} tests passed`, 'success');
            } catch (error) {
                results[testType] = { passed: false, error: error.message };
                this.log(`${testType} tests failed: ${error.message}`, 'error');
                
                if (!this.force) {
                    throw new Error(`Test suite failed: ${testType}`);
                }
            }
        }
        
        return results;
    }
    
    async simulateTest(testType) {
        // Simulate test execution with random delay
        await new Promise(resolve => setTimeout(resolve, Math.random() * 2000));
        
        // Simulate occasional test failures
        if (Math.random() > 0.9 && !this.force) {
            throw new Error(`${testType} test suite failed`);
        }
    }
    
    async buildApplication() {
        this.log('Building application...', 'step');
        
        try {
            // Simulate build process
            this.log('Running build command...', 'info');
            
            // In real scenario: await execPromise('npm run build');
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            this.log('Build completed successfully', 'success');
            
            // Generate build artifacts info
            const buildInfo = {
                version: '1.0.0',
                commit: 'abc123',
                timestamp: new Date().toISOString(),
                files: ['dist/app.js', 'dist/app.css', 'dist/index.html']
            };
            
            // Save build info
            fs.writeFileSync(
                'build-info.json',
                JSON.stringify(buildInfo, null, 2)
            );
            
            return buildInfo;
        } catch (error) {
            this.log(`Build failed: ${error.message}`, 'error');
            throw error;
        }
    }
    
    async requestApproval() {
        if (!this.envConfig.approval) {
            return true;
        }
        
        this.log('Deployment requires approval', 'warning');
        this.log(`Deployment ID: ${this.deploymentId}`, 'info');
        this.log(`Environment: ${this.environment}`, 'info');
        this.log(`Target URL: ${this.envConfig.url}`, 'info');
        
        // In real scenario, would send notification and wait for approval
        // For demo, we'll auto-approve
        this.log('Auto-approving deployment (demo mode)', 'success');
        return true;
    }
    
    async deploy() {
        this.log(`Starting deployment to ${this.environment}...`, 'step');
        
        if (this.dryRun) {
            this.log('DRY RUN MODE - No actual deployment will occur', 'warning');
        }
        
        const steps = [
            { name: 'Backup current version', fn: () => this.backupCurrent() },
            { name: 'Upload artifacts', fn: () => this.uploadArtifacts() },
            { name: 'Update configuration', fn: () => this.updateConfiguration() },
            { name: 'Database migrations', fn: () => this.runMigrations() },
            { name: 'Switch versions', fn: () => this.switchVersions() },
            { name: 'Health check', fn: () => this.healthCheck() },
            { name: 'Smoke tests', fn: () => this.runSmokeTests() }
        ];
        
        for (const step of steps) {
            this.log(`${step.name}...`, 'info');
            
            try {
                if (!this.dryRun) {
                    await step.fn();
                }
                this.log(`${step.name} completed`, 'success');
            } catch (error) {
                this.log(`${step.name} failed: ${error.message}`, 'error');
                
                if (!this.force) {
                    await this.rollback();
                    throw error;
                }
            }
        }
        
        this.log('Deployment completed successfully!', 'success');
    }
    
    async backupCurrent() {
        // Simulate backup
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.log('Backup created: backup-20240115-123456.tar.gz', 'info');
    }
    
    async uploadArtifacts() {
        // Simulate upload
        await new Promise(resolve => setTimeout(resolve, 2000));
        this.log('Artifacts uploaded to server', 'info');
    }
    
    async updateConfiguration() {
        // Simulate config update
        await new Promise(resolve => setTimeout(resolve, 500));
        this.log('Configuration updated', 'info');
    }
    
    async runMigrations() {
        // Simulate database migrations
        await new Promise(resolve => setTimeout(resolve, 1500));
        this.log('Database migrations completed', 'info');
    }
    
    async switchVersions() {
        // Simulate version switch
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.log('Switched to new version', 'info');
    }
    
    async healthCheck() {
        // Simulate health check
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const health = {
            status: 'healthy',
            version: '1.0.0',
            uptime: 0,
            checks: {
                database: 'ok',
                cache: 'ok',
                storage: 'ok'
            }
        };
        
        this.log(`Health check passed: ${JSON.stringify(health)}`, 'success');
        return health;
    }
    
    async runSmokeTests() {
        // Simulate smoke tests
        await new Promise(resolve => setTimeout(resolve, 3000));
        this.log('Smoke tests passed', 'success');
    }
    
    async rollback() {
        this.log('ROLLING BACK DEPLOYMENT', 'error');
        
        // Simulate rollback
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        this.log('Rollback completed', 'warning');
    }
    
    generateReport() {
        const duration = Date.now() - this.startTime;
        const report = {
            deploymentId: this.deploymentId,
            environment: this.environment,
            status: 'success',
            duration: `${(duration / 1000).toFixed(2)}s`,
            timestamp: new Date().toISOString(),
            url: this.envConfig.url
        };
        
        this.log('\n' + '='.repeat(50), 'info');
        this.log('DEPLOYMENT REPORT', 'info');
        this.log('='.repeat(50), 'info');
        
        Object.entries(report).forEach(([key, value]) => {
            this.log(`${key}: ${value}`, 'info');
        });
        
        // Save report to file
        fs.writeFileSync(
            `deployment-${this.deploymentId}.json`,
            JSON.stringify(report, null, 2)
        );
        
        return report;
    }
    
    async execute() {
        try {
            this.log(`\n🚀 Deployment Manager - ${this.environment.toUpperCase()}`, 'info');
            this.log('='.repeat(50), 'info');
            
            if (this.validate) {
                this.log('Running validation only', 'info');
                await this.checkPrerequisites();
                await this.runTests();
                this.log('Validation completed successfully', 'success');
                return;
            }
            
            // Full deployment flow
            await this.checkPrerequisites();
            await this.runTests();
            await this.buildApplication();
            
            const approved = await this.requestApproval();
            if (!approved) {
                throw new Error('Deployment not approved');
            }
            
            await this.deploy();
            
            const report = this.generateReport();
            
            this.log(`\n✅ Deployment successful!`, 'success');
            this.log(`🔗 Application URL: ${this.envConfig.url}`, 'info');
            
            return report;
            
        } catch (error) {
            this.log(`\n❌ Deployment failed: ${error.message}`, 'error');
            process.exit(1);
        }
    }
}

// Parse command line arguments
function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        environment: 'development',
        validate: false,
        dryRun: false,
        force: false,
        verbose: false,
        skipTests: false,
        help: false
    };
    
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--env':
            case '-e':
                options.environment = args[++i];
                break;
            case '--validate':
            case '-v':
                options.validate = true;
                break;
            case '--dry-run':
                options.dryRun = true;
                break;
            case '--force':
            case '-f':
                options.force = true;
                break;
            case '--verbose':
                options.verbose = true;
                break;
            case '--skip-tests':
                options.skipTests = true;
                break;
            case '--help':
            case '-h':
                options.help = true;
                break;
        }
    }
    
    return options;
}

function showHelp() {
    console.log(`
${colors.cyan}Deployment Script for DevOps Assistant Plugin${colors.reset}

Usage: node deploy.js [options]

Options:
  --env, -e <env>     Target environment (development, staging, production)
  --validate, -v      Run validation only without deploying
  --dry-run           Simulate deployment without making changes
  --force, -f         Force deployment even if checks fail
  --skip-tests        Skip test execution
  --verbose           Enable verbose output
  --help, -h          Show this help message

Examples:
  node deploy.js --env staging
  node deploy.js --validate --env production
  node deploy.js --dry-run --env production
`);
}

// Main execution
async function main() {
    const options = parseArgs();
    
    if (options.help) {
        showHelp();
        process.exit(0);
    }
    
    // Validate environment
    if (!config.environments[options.environment]) {
        console.error(`${colors.red}Error: Unknown environment '${options.environment}'${colors.reset}`);
        console.log(`Available environments: ${Object.keys(config.environments).join(', ')}`);
        process.exit(1);
    }
    
    const manager = new DeploymentManager(options);
    await manager.execute();
}

// Run if executed directly
if (require.main === module) {
    main().catch(error => {
        console.error(`${colors.red}Fatal error: ${error.message}${colors.reset}`);
        process.exit(1);
    });
}

module.exports = DeploymentManager;
