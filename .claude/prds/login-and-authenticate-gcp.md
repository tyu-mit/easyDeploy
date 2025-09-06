---
name: login-and-authenticate-gcp
description: Explicit GCP authentication via easydeploy gcp login command with OAuth2 browser flow
status: backlog
created: 2025-09-06T20:11:06Z
---

# PRD: login-and-authenticate-gcp

## Executive Summary

The `login-and-authenticate-gcp` feature provides explicit Google Cloud Platform authentication through the `easydeploy gcp login` command. Other GCP commands validate authentication status and fail with clear error messages when authentication is required, ensuring users have explicit control over the authentication process.

## Problem Statement

**What problem are we solving?**
Robotics AI developers need secure, controlled GCP authentication for cloud deployments. Users should have explicit control over when authentication occurs, with clear feedback when authentication is required.

**Why is this important now?**
- Explicit authentication gives users control and transparency
- Clear error messages reduce confusion when commands fail due to missing authentication
- Secure OAuth2 flow protects user credentials
- easyDeploy GCP functionality requires authenticated access to cloud resources

## User Stories

**Primary Persona: Robotics AI Developer**
- Experience level: Intermediate to advanced in robotics/AI, beginner to intermediate in cloud deployment
- Goal: Authenticate to GCP when needed and execute deployment commands successfully

**User Journey:**

1. **First-time User Experience**
   ```bash
   $ easydeploy gcp deploy-vm
   ❌ Error: Not authenticated with GCP
   💡 Please run: easydeploy gcp login

   $ easydeploy gcp login
   🌐 Opening browser for GCP authentication...
   ✅ Successfully authenticated with GCP

   $ easydeploy gcp deploy-vm
   ✅ Deploying VM to GCP...
   ```

2. **Authenticated User Experience**
   ```bash
   $ easydeploy gcp status
   ✅ Authenticated as: user@example.com
   📋 Project: my-robotics-project

   $ easydeploy gcp deploy-vm
   ✅ Deploying VM to GCP...
   ```

3. **Token Expiration Experience**
   ```bash
   $ easydeploy gcp deploy-vm
   ❌ Error: GCP authentication expired
   💡 Please run: easydeploy gcp login

   $ easydeploy gcp login
   🔄 Refreshing GCP authentication...
   ✅ Authentication renewed
   ```

## Requirements

### Functional Requirements

**FR-1: Explicit Login Command**
- Implement `easydeploy gcp login` command
- Launch browser-based OAuth2 authentication flow
- Store authentication tokens securely after successful login
- Provide clear success/failure feedback

**FR-2: Authentication Status Validation**
- All `easydeploy gcp [command]` (except login) must check authentication status
- Commands fail immediately with clear error message if not authenticated
- Error message includes instruction to run `easydeploy gcp login`
- No automatic authentication triggers

**FR-3: Browser-Based OAuth2 Flow**
- Launch system default browser for GCP OAuth consent
- Handle OAuth2 authorization code flow with PKCE security
- Support localhost callback server (port 8080, fallback to available ports)
- Handle user consent for required GCP permissions

**FR-4: Token Management**
- Store access and refresh tokens in `~/.easydeploy/gcp-credentials.json` (encrypted)
- Automatically refresh tokens before expiration when possible
- Detect and handle expired/invalid tokens
- Support explicit logout functionality

**FR-5: Authentication Status Commands**
- `easydeploy gcp status` - Show current authentication status
- `easydeploy gcp logout` - Clear stored authentication tokens
- Display authenticated user email and GCP project information

**FR-6: Required Permission Validation**
- Validate user has necessary GCP permissions:
  - Compute Engine: VM management, network configuration
  - Cloud Storage: Bucket and object management
  - Basic project access for resource management
- Provide specific error messages for insufficient permissions

### Non-Functional Requirements

**NFR-1: User Experience**
- Clear, actionable error messages for authentication failures
- Consistent command behavior across all GCP subcommands
- Login process completes in under 90 seconds
- Intuitive command structure and help text

**NFR-2: Security**
- OAuth2 with PKCE for secure public client authentication
- Encrypted local credential storage
- Secure localhost-only redirect URIs
- No credential exposure in logs or error messages

**NFR-3: Reliability**
- Robust error handling for network failures and browser issues
- Automatic token refresh where possible
- Clear recovery instructions for authentication failures
- Consistent behavior across Linux, macOS, Windows

**NFR-4: Performance**
- Authentication status check completes in < 1 second
- Token validation doesn't significantly delay command startup
- Efficient local credential storage and retrieval

## Success Criteria

**Primary Metrics:**
- Login command success rate > 95%
- Authentication status validation accuracy 100%
- Average login completion time < 60 seconds
- User error resolution rate > 80% (users successfully authenticate after error)

**User Experience Goals:**
- Users understand when and why authentication is required
- Error messages lead to successful problem resolution
- No surprise authentication prompts or automatic browser launches
- Clear feedback on authentication status and required actions

## Constraints & Assumptions

**Technical Constraints:**
- Must integrate with easydeploy CLI framework
- Requires system browser for OAuth flow
- Depends on internet connectivity for authentication
- Subject to GCP OAuth2 service quotas and limitations

**Design Constraints:**
- Authentication must be explicit user action (no automatic triggers)
- All GCP commands must validate authentication before execution
- Error messages must be clear and actionable
- Commands must fail fast when authentication is invalid

**Assumptions:**
- Users have Google accounts with GCP project access
- System has default browser configured and accessible
- Network allows HTTPS connections to Google OAuth services
- Users are comfortable with browser-based authentication flows

## Out of Scope

**Explicitly NOT Building:**
- Automatic authentication triggers from other commands
- Service account key file authentication
- Multi-project authentication management
- Shared authentication across multiple users
- Offline authentication modes
- Custom OAuth consent screens
- Integration with enterprise SSO systems
- Authentication for `easydeploy azure` or `easydeploy local`

## Dependencies

**External Dependencies:**
- Google Cloud Platform OAuth2 services
- System default browser functionality
- GCP APIs for permission validation
- Internet connectivity for authentication flows

**Internal Dependencies:**
- easydeploy CLI framework and command structure
- Python Google Auth libraries (google-auth, google-auth-oauthlib)
- Secure local storage implementation
- HTTP server for OAuth callback handling
- Cross-platform browser launching utilities

**Future Integration:**
- All future `easydeploy gcp` subcommands must implement authentication validation
- Authenticated GCP client objects provided to command implementations
- Consistent error handling patterns across GCP command family

## Technical Implementation Notes

**Command Structure:**
```bash
easydeploy gcp login          # Explicit authentication
easydeploy gcp logout         # Clear authentication
easydeploy gcp status         # Show auth status
easydeploy gcp [other-cmd]    # Requires authentication
```

**Required GCP OAuth Scopes:**
```
https://www.googleapis.com/auth/compute
https://www.googleapis.com/auth/devstorage.full_control
https://www.googleapis.com/auth/cloud-platform.read-only
```

**Authentication Flow (easydeploy gcp login):**
1. Check for existing valid tokens
2. If valid, confirm renewal or exit
3. Start local HTTP callback server
4. Generate PKCE challenge and state
5. Construct GCP OAuth authorization URL
6. Launch browser to authorization URL
7. Wait for authorization code callback
8. Exchange authorization code for tokens
9. Validate token permissions
10. Store encrypted tokens locally
11. Display success message with user info

**Validation Flow (other commands):**
1. Check for stored authentication tokens
2. Validate token expiration and scopes
3. If invalid/missing: fail with clear error message
4. If valid: provide authenticated GCP clients to command
5. Handle token refresh if needed

**Error Scenarios:**
- No stored credentials: "Not authenticated with GCP. Please run: easydeploy gcp login"
- Expired credentials: "GCP authentication expired. Please run: easydeploy gcp login"
- Insufficient permissions: "Missing required GCP permissions: [specific permissions]"
- Network issues: "Unable to connect to GCP. Please check internet connection."
- Browser launch failure: "Unable to open browser. Please visit: [manual URL]"
