#!/bin/bash

# AWS ADFS Login Script
# This script authenticates with AWS using ADFS
# All configuration can be set in .env.local file

# Save the current directory to ensure we stay in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ORIGINAL_DIR="$(pwd)"

# Ensure we're in the script's directory for .env.local
cd "$SCRIPT_DIR"

# Check if .env.local exists and source it
if [ -f .env.local ]; then
    set -o allexport
    source .env.local
    set +o allexport
    echo "📁 Loaded configuration from .env.local"
else
    echo "⚠️  No .env.local file found. Creating template..."
    cat > .env.local << 'EOF'
# AWS ADFS Configuration
# Fill in your values below

# ADFS Host (required)
ADFS_HOST=adfs.devfactory.com/adfs/ls/idpinitiatedsignon

# Your AD Username (required) - Format: domain\\username (note the double backslash)
AD_USERNAME=devfactory\\\\yourusername

# Your AD Password (optional - for automation, but less secure)
# If not set, you'll be prompted for it
# AD_PASSWORD=

# AWS Role ARN (optional - if not set, will show interactive selection)
# Note: Console URL generation requires a specific role ARN to be set
# Available roles:
# AWS_ROLE_ARN=arn:aws:iam::617147411452:role/RAM-AWS-Prod-TelcoDR-telcodrtotogipresales1-Admin
# AWS_ROLE_ARN=arn:aws:iam::764119721991:role/RAM-AWS-Prod-TelcoDR-TotogiPS-Admin
# AWS_ROLE_ARN=arn:aws:iam::914357406961:role/RAM-AWS-Prod-Totogi-zainsudanbssmagic-Admin

# AWS CLI Profile Name (default: default)
AWS_PROFILE=default

# AWS Region (default: us-east-1)
AWS_REGION=us-east-1

# ADFS Provider ID (default: urn:amazon:webservices)
ADFS_PROVIDER_ID=urn:amazon:webservices

# Session Duration in seconds (default: 3600 = 1 hour, max: 43200 = 12 hours)
SESSION_DURATION=3600

# SSL Verification (set to false to disable, default: false for devfactory)
SSL_VERIFICATION=false

# Generate AWS Console signin URL after login (true/false, default: false)
# Note: Requires AWS_ROLE_ARN to be set. With interactive role selection, console URL cannot be generated.
# PRINT_CONSOLE_URL=false
EOF
    echo "✅ Created template .env.local file"
    echo "📝 Please edit .env.local with your credentials and run this script again"
    cd "$ORIGINAL_DIR"
    exit 0
fi

# Set defaults for optional variables
: "${ADFS_HOST:=adfs.devfactory.com/adfs/ls/idpinitiatedsignon}"
: "${ADFS_PROVIDER_ID:=urn:amazon:webservices}"
: "${SESSION_DURATION:=3600}"
: "${AWS_PROFILE:=default}"
: "${AWS_REGION:=us-east-1}"
: "${SSL_VERIFICATION:=false}"
: "${PRINT_CONSOLE_URL:=false}"

# Allow command line arguments to override environment variables
# Note: Command line --console-url will override .env.local setting
RESET_ROLE_CACHE=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --username) AD_USERNAME="$2"; shift ;;
        --password) AD_PASSWORD="$2"; shift ;;
        --role-arn) AWS_ROLE_ARN="$2"; shift ;;
        --profile) AWS_PROFILE="$2"; shift ;;
        --region) AWS_REGION="$2"; shift ;;
        --console-url) PRINT_CONSOLE_URL=true ;;
        --reset-role) RESET_ROLE_CACHE=true ;;
        --help) 
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --username USER     Override AD username from .env.local"
            echo "  --password PASS     Override AD password from .env.local"
            echo "  --role-arn ARN      Override AWS role ARN from .env.local"
            echo "  --profile PROFILE   Override AWS CLI profile from .env.local"
            echo "  --region REGION     Override AWS region from .env.local"
            echo "  --console-url       Print AWS Console signin URL after login"
            echo "  --reset-role        Clear cached role and session data"
            echo "  --help              Show this help message"
            echo ""
            echo "All settings can be configured in .env.local file"
            cd "$ORIGINAL_DIR"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; cd "$ORIGINAL_DIR"; exit 1 ;;
    esac
    shift
done

# Validate required variables
if [ -z "$AD_USERNAME" ]; then
    echo "❌ Missing required variable: AD_USERNAME"
    echo "   Please set it in .env.local or use --username"
    cd "$ORIGINAL_DIR"
    exit 1
fi

# Check if aws-adfs is available
if [ -x ".venv/bin/aws-adfs" ]; then
    AWS_ADFS_CMD=".venv/bin/aws-adfs"
elif command -v aws-adfs &> /dev/null; then
    AWS_ADFS_CMD="aws-adfs"
else
    echo "❌ aws-adfs not found. Please install it first."
    echo "   Run: uv pip install aws-adfs"
    cd "$ORIGINAL_DIR"
    exit 1
fi

echo "🔐 Logging in to AWS via ADFS..."
echo "   Current Dir: $ORIGINAL_DIR"
echo "   Script Dir: $SCRIPT_DIR"
echo "   Host: $ADFS_HOST"
echo "   User: $AD_USERNAME"
echo "   Region: $AWS_REGION"
echo "   Profile: $AWS_PROFILE"

# Ensure AWS config directory exists
mkdir -p ~/.aws

# Create profile in AWS config if it doesn't exist
if ! grep -q "\[profile $AWS_PROFILE\]" ~/.aws/config 2>/dev/null; then
    echo "📝 Creating AWS profile: $AWS_PROFILE"
    cat >> ~/.aws/config << EOF

[profile $AWS_PROFILE]
region = $AWS_REGION
output = json
EOF
fi

# Also ensure the profile exists in credentials file
if ! grep -q "\[$AWS_PROFILE\]" ~/.aws/credentials 2>/dev/null; then
    echo "📝 Initializing credentials for profile: $AWS_PROFILE"
    touch ~/.aws/credentials
    cat >> ~/.aws/credentials << EOF

[$AWS_PROFILE]
aws_access_key_id = 
aws_secret_access_key = 
aws_session_token = 
EOF
fi

# Clear cached role selection if requested or when no role is specified
if [ "$RESET_ROLE_CACHE" = "true" ] || [ -z "$AWS_ROLE_ARN" ]; then
    if [ -f ~/.aws/config ]; then
        echo "🔄 Clearing cached role selection to enable interactive choice..."
        # Remove ALL adfs_config.role_arn lines from the entire config file
        sed -i.bak '/adfs_config\.role_arn/d' ~/.aws/config 2>/dev/null || true
        # Clean up backup files
        rm -f ~/.aws/config.bak 2>/dev/null || true
    fi
    # Also clear session cache if explicitly requested
    if [ "$RESET_ROLE_CACHE" = "true" ] && [ -d ~/.aws/adfs_cache ]; then
        echo "   Clearing session cache..."
        rm -rf ~/.aws/adfs_cache/* 2>/dev/null || true
    fi
fi

# Build the command
CMD="$AWS_ADFS_CMD login"
CMD="$CMD --adfs-host $ADFS_HOST"
CMD="$CMD --region $AWS_REGION"
CMD="$CMD --provider-id $ADFS_PROVIDER_ID"
CMD="$CMD --s3-signature-version s3v4"
CMD="$CMD --session-duration $SESSION_DURATION"
CMD="$CMD --profile $AWS_PROFILE"

# Note: When no role is specified, we've already cleared the cached role above
# This will force aws-adfs to show the interactive role selection menu

# Add SSL verification flag
if [ "$SSL_VERIFICATION" = "false" ]; then
    CMD="$CMD --no-ssl-verification"
fi

# Add role-arn if provided
if [ -n "$AWS_ROLE_ARN" ]; then
    CMD="$CMD --role-arn $AWS_ROLE_ARN"
    echo "   Role: $AWS_ROLE_ARN"
else
    echo "   Role: Will be selected interactively"
fi

# Check if console URL is requested
WANT_CONSOLE_URL=false
CAN_GENERATE_CONSOLE_URL=false
if [ "$PRINT_CONSOLE_URL" = "true" ]; then
    WANT_CONSOLE_URL=true
    if [ -n "$AWS_ROLE_ARN" ]; then
        CMD="$CMD --print-console-signin-url"
        echo "   Console URL: Will be generated after login"
        CAN_GENERATE_CONSOLE_URL=true
    else
        echo "   Console URL: Will be generated after role selection"
        echo "                  (Two-step process: select role, then generate URL)"
    fi
fi

# Handle authentication
if [ -n "$AD_PASSWORD" ]; then
    echo "   Password: Using password from .env.local (automated login)"
    echo ""
    echo "🤖 Running automated login..."
    # Export for aws-adfs --env flag
    export username="$AD_USERNAME"
    export password="$AD_PASSWORD"
    # Use environment variables
    if [ "$CAN_GENERATE_CONSOLE_URL" = "true" ]; then
        # Capture the output when printing console URL (only when role is specified)
        OUTPUT=$($CMD --env 2>&1)
        EXIT_CODE=$?
        echo "$OUTPUT"
        # Extract and highlight the console URL if present
        if [ $EXIT_CODE -eq 0 ]; then
            CONSOLE_URL=$(echo "$OUTPUT" | grep -o 'https://.*signin.aws.amazon.com.*' | head -1)
        fi
    else
        # Run interactively (allows role selection)
        if [ "$WANT_CONSOLE_URL" = "true" ] && [ -z "$AWS_ROLE_ARN" ]; then
            echo ""
            echo "📋 Step 1: Interactive role selection..."
            echo ""
            # Run interactively without capturing output (so menu displays properly)
            $CMD --env
            EXIT_CODE=$?
            
            # If successful, read the selected role from AWS config
            if [ $EXIT_CODE -eq 0 ]; then
                # aws-adfs saves the selected role in the AWS config file
                SELECTED_ROLE=$(grep -A 20 "\[$AWS_PROFILE\]\|\[profile $AWS_PROFILE\]" ~/.aws/config 2>/dev/null | grep "adfs_config.role_arn" | head -1 | cut -d'=' -f2 | xargs)
                
                if [ -n "$SELECTED_ROLE" ]; then
                    echo ""
                    echo "📋 Step 2: Generating console URL for selected role..."
                    echo "   Selected Role: $SELECTED_ROLE"
                    echo ""
                    # Re-run with the selected role and console URL flag
                    RERUN_CMD="$AWS_ADFS_CMD login"
                    RERUN_CMD="$RERUN_CMD --adfs-host $ADFS_HOST"
                    RERUN_CMD="$RERUN_CMD --region $AWS_REGION"
                    RERUN_CMD="$RERUN_CMD --provider-id $ADFS_PROVIDER_ID"
                    RERUN_CMD="$RERUN_CMD --s3-signature-version s3v4"
                    RERUN_CMD="$RERUN_CMD --session-duration $SESSION_DURATION"
                    RERUN_CMD="$RERUN_CMD --profile $AWS_PROFILE"
                    if [ "$SSL_VERIFICATION" = "false" ]; then
                        RERUN_CMD="$RERUN_CMD --no-ssl-verification"
                    fi
                    RERUN_CMD="$RERUN_CMD --role-arn '$SELECTED_ROLE'"
                    RERUN_CMD="$RERUN_CMD --print-console-signin-url"
                    CONSOLE_OUTPUT=$(eval $RERUN_CMD --env 2>&1)
                    echo "$CONSOLE_OUTPUT"
                    CONSOLE_URL=$(echo "$CONSOLE_OUTPUT" | grep -o 'https://.*signin.aws.amazon.com.*' | head -1)
                else
                    echo "⚠️  Could not detect selected role. Console URL generation skipped."
                fi
            fi
        else
            $CMD --env
            EXIT_CODE=$?
        fi
    fi
else
    echo "   Password: Will be prompted"
    echo ""
    echo "👤 Using username from .env.local: $AD_USERNAME"
    
    # Prompt for password securely
    read -s -p "🔐 Password: " USER_PASSWORD
    echo ""  # New line after password input
    
    # Save password temporarily for potential re-run
    TEMP_PASSWORD="$USER_PASSWORD"
    
    # Pass both username and password to aws-adfs
    if [ "$CAN_GENERATE_CONSOLE_URL" = "true" ]; then
        # Capture the output when printing console URL (only when role is specified)
        OUTPUT=$(printf "%s\n%s\n" "$AD_USERNAME" "$USER_PASSWORD" | $CMD --stdin 2>&1)
        EXIT_CODE=$?
        echo "$OUTPUT"
        # Extract and highlight the console URL if present
        if [ $EXIT_CODE -eq 0 ]; then
            CONSOLE_URL=$(echo "$OUTPUT" | grep -o 'https://.*signin.aws.amazon.com.*' | head -1)
        fi
    else
        # Run interactively (allows role selection)
        if [ "$WANT_CONSOLE_URL" = "true" ] && [ -z "$AWS_ROLE_ARN" ]; then
            echo ""
            echo "📋 Step 1: Interactive role selection..."
            echo ""
            # Run interactively without capturing output (so menu displays properly)
            printf "%s\n%s\n" "$AD_USERNAME" "$USER_PASSWORD" | $CMD --stdin
            EXIT_CODE=$?
            
            # If successful, read the selected role from AWS config
            if [ $EXIT_CODE -eq 0 ]; then
                # aws-adfs saves the selected role in the AWS config file
                SELECTED_ROLE=$(grep -A 20 "\[$AWS_PROFILE\]\|\[profile $AWS_PROFILE\]" ~/.aws/config 2>/dev/null | grep "adfs_config.role_arn" | head -1 | cut -d'=' -f2 | xargs)
                
                if [ -n "$SELECTED_ROLE" ]; then
                    echo ""
                    echo "📋 Step 2: Generating console URL for selected role..."
                    echo "   Selected Role: $SELECTED_ROLE"
                    echo ""
                    # Re-run with the selected role and console URL flag
                    RERUN_CMD="$AWS_ADFS_CMD login"
                    RERUN_CMD="$RERUN_CMD --adfs-host $ADFS_HOST"
                    RERUN_CMD="$RERUN_CMD --region $AWS_REGION"
                    RERUN_CMD="$RERUN_CMD --provider-id $ADFS_PROVIDER_ID"
                    RERUN_CMD="$RERUN_CMD --s3-signature-version s3v4"
                    RERUN_CMD="$RERUN_CMD --session-duration $SESSION_DURATION"
                    RERUN_CMD="$RERUN_CMD --profile $AWS_PROFILE"
                    if [ "$SSL_VERIFICATION" = "false" ]; then
                        RERUN_CMD="$RERUN_CMD --no-ssl-verification"
                    fi
                    RERUN_CMD="$RERUN_CMD --role-arn '$SELECTED_ROLE'"
                    RERUN_CMD="$RERUN_CMD --print-console-signin-url"
                    RERUN_CMD="$RERUN_CMD --stdin"
                    CONSOLE_OUTPUT=$(printf "%s\n%s\n" "$AD_USERNAME" "$TEMP_PASSWORD" | eval $RERUN_CMD 2>&1)
                    echo "$CONSOLE_OUTPUT"
                    CONSOLE_URL=$(echo "$CONSOLE_OUTPUT" | grep -o 'https://.*signin.aws.amazon.com.*' | head -1)
                else
                    echo "⚠️  Could not detect selected role. Console URL generation skipped."
                fi
            fi
        else
            printf "%s\n%s\n" "$AD_USERNAME" "$USER_PASSWORD" | $CMD --stdin
            EXIT_CODE=$?
        fi
    fi
    # Clear temporary password
    unset TEMP_PASSWORD
fi

# Set EXIT_CODE if not already set (for non-console-url mode)
if [ -z "$EXIT_CODE" ]; then
    EXIT_CODE=$?
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Login successful! AWS credentials saved to profile: $AWS_PROFILE"
    echo ""
    
    # Display console URL if available
    if [ -n "$CONSOLE_URL" ]; then
        echo "🌐 AWS Management Console Sign-in URL:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "$CONSOLE_URL"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "💡 TIP: Copy and paste this URL into your browser to access the AWS Console"
        echo "⏱️  This URL is valid for the session duration ($SESSION_DURATION seconds)"
        echo ""
    elif [ "$WANT_CONSOLE_URL" = "true" ] && [ -z "$CONSOLE_URL" ]; then
        echo "⚠️  Console URL generation failed. This can happen if:"
        echo "   - The role selection was cancelled"
        echo "   - The selected role could not be detected"
        echo "   To ensure console URL generation, specify AWS_ROLE_ARN in .env.local or use --role-arn"
        echo ""
    fi
    
    if [ "$AWS_PROFILE" = "default" ]; then
        echo "🎉 Credentials saved to the default profile!"
        echo ""
        echo "You can now use AWS CLI commands directly:"
        echo "   aws s3 ls"
        echo "   aws sts get-caller-identity"
        echo ""
        echo "No need to specify --profile since you're using the default profile."
    else
        echo "⚠️  IMPORTANT: The credentials are saved to profile '$AWS_PROFILE', not the default profile!"
        echo ""
        echo "To use these credentials, you have two options:"
        echo ""
        echo "Option 1: Set environment variable (recommended for this session):"
        echo "   export AWS_PROFILE=$AWS_PROFILE"
        echo "   aws s3 ls                      # Now works without --profile"
        echo ""
        echo "Option 2: Specify profile in each command:"
        echo "   aws s3 ls --profile $AWS_PROFILE"
        echo ""
        echo "💡 TIP: Add 'export AWS_PROFILE=$AWS_PROFILE' to your ~/.bashrc to make it permanent"
    fi
    
    echo ""
    echo "Test your credentials:"
    if [ "$AWS_PROFILE" = "default" ]; then
        echo "   aws sts get-caller-identity"
    else
        echo "   aws sts get-caller-identity --profile $AWS_PROFILE"
    fi
    echo ""
    echo "📍 Returning to: $ORIGINAL_DIR"
else
    echo "❌ Login failed."
    echo "📍 Returning to: $ORIGINAL_DIR"
    cd "$ORIGINAL_DIR"
    exit $EXIT_CODE
fi

# Return to original directory before successful exit
cd "$ORIGINAL_DIR"
echo "✅ Done! You're back in: $(pwd)"