---
name: login-and-authenticate-gcp
status: backlog
created: 2025-09-06T20:31:53Z
progress: 0%
prd: .claude/prds/login-and-authenticate-gcp.md
github: https://github.com/tyu-mit/easyDeploy/issues/1
---

# Epic: login-and-authenticate-gcp

## Overview
Simple GCP authentication for internal team use. Just implement `easydeploy gcp login` that opens browser, gets OAuth token, and stores it. Other GCP commands check if token exists and fail with simple error if not.

## Architecture Decisions
- **Keep it simple**: Use existing Google Auth library, store token in plain JSON file
- **No encryption**: Internal team tool, simple file storage is fine
- **Basic CLI**: Add commands to existing structure, no complex framework needed
- **Minimal error handling**: Trust internal users, basic error messages

## Technical Approach

### Just Three Commands
```bash
easydeploy gcp login   # Opens browser, saves token
easydeploy gcp logout  # Deletes token file  
easydeploy gcp status  # Shows if logged in
```

### Simple Implementation
1. **One auth file** (`src/python/gcp_auth.py`)
   - OAuth flow with google-auth-oauthlib
   - Save/load token from `~/.easydeploy/gcp-token.json`
   - Check if token is valid

2. **Add to CLI** - extend existing CLI structure
   - Three simple commands
   - Basic check function for other commands

### OAuth Flow (Minimal)
1. Open browser to Google OAuth
2. User consents, gets redirected to localhost
3. Save the token to JSON file
4. Done

## Implementation Strategy

### Single Phase: Just Build It (1 week max)
- Add google-auth-oauthlib dependency
- Create simple auth module with OAuth flow
- Add three CLI commands
- Test with team's Google accounts

## Task Breakdown Preview
High-level task categories that will be created:
- [ ] **Setup**: Add dependencies, create basic auth module
- [ ] **OAuth Implementation**: Simple browser flow, save token to file
- [ ] **CLI Commands**: Add login/logout/status to existing CLI
- [ ] **Basic Testing**: Test with real GCP accounts, verify it works

## Dependencies

### External Dependencies
- `google-auth-oauthlib` for OAuth flow
- Existing CLI framework (whatever you're using)

### Internal Dependencies  
- Basic CLI structure
- Team has GCP projects and Google accounts

## Success Criteria (Technical)

### Simple Goals
- Team members can run `easydeploy gcp login` and authenticate
- Other GCP commands check authentication and fail clearly if needed
- Basic token refresh works
- Takes < 1 week to implement

### Acceptance Criteria
- Login works with team's Google accounts
- Token persists between CLI runs
- Clear error when not authenticated

## Estimated Effort

### Timeline: 3-5 days max
- **Day 1**: Set up OAuth flow
- **Day 2**: Add CLI commands  
- **Day 3**: Test with team, fix issues

### Resource Requirements
- 1 developer
- Team's GCP project for OAuth app setup
- Test on Linux (team's main platform)

### Keep it Simple
- No complex error handling
- No cross-platform testing initially
- No encryption (internal tool)
- Basic functionality first

## Tasks Created
- [ ] #2 - Setup Dependencies and Project Structure (parallel: false)
- [ ] #3 - Implement OAuth2 Flow and Token Storage (parallel: false)
- [ ] #4 - Implement CLI Commands (parallel: false)
- [ ] #5 - Testing and Validation (parallel: false)

Total tasks: 4
Parallel tasks: 0
Sequential tasks: 4
Estimated total effort: 18-28 hours (3-5 days)
