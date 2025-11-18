# Persona-Driven AI Framework - Workflow Directory

## Overview

This directory contains AI-generated requirements, design documents, and implementation plans for Jira tickets. Each workflow represents a complete analysis of a feature or task, while the actual implementation code lives in project directories (e.g., `demo-app/`).

## Purpose

The `.ai/` directory serves as a **knowledge base and planning hub** for development work:

- 📋 **Requirements Analysis** - Detailed feature requirements from Jira tickets
- 🏗️ **System Design** - Architecture and technical design documents
- 📝 **Implementation Plans** - Step-by-step implementation roadmaps
- 🎯 **Completion Tracking** - Summary of completed work

**Implementation code is NOT stored here** - it lives in project directories like `demo-app/`, `packages/`, etc.

## Directory Structure

```
.ai/
├── README.md                    # This file
├── workflow/                    # Workflow-specific directories
│   ├── DASHBOARD-001/          # Example: Developer Productivity Dashboard
│   │   ├── README.md           # Workflow overview
│   │   ├── FEATURE_REQUIREMENTS.md
│   │   ├── SYSTEM_DESIGN.md
│   │   ├── IMPLEMENTATION_PLAN.md
│   │   ├── COMPLETION_SUMMARY.md
│   │   └── INDEX.md            # File navigation
│   ├── JIRA-123/               # Example: Jira ticket ABC-123
│   │   ├── README.md
│   │   ├── REQUIREMENTS.md
│   │   ├── DESIGN.md
│   │   └── PLAN.md
│   └── FEATURE-XYZ/            # Example: Feature XYZ
│       └── ...
└── templates/                   # Templates for new workflows
    ├── REQUIREMENTS_TEMPLATE.md
    ├── DESIGN_TEMPLATE.md
    └── PLAN_TEMPLATE.md
```

## Workflow Naming Convention

Use one of these naming patterns:

1. **Jira Ticket**: `JIRA-123` (e.g., `AEC-456`, `DASH-789`)
2. **Feature Name**: `FEATURE-NAME` (e.g., `USER-AUTH`, `PAYMENT-FLOW`)
3. **Epic/Initiative**: `EPIC-NAME` (e.g., `DASHBOARD-001`, `MOBILE-APP`)

## Workflow Lifecycle

### 1. Create Workflow (AI-Generated)

When starting work on a Jira ticket:

```bash
# AI generates requirements and design
persona-framework/.ai/workflow/JIRA-123/
├── README.md                    # Overview
├── FEATURE_REQUIREMENTS.md      # What needs to be built
├── SYSTEM_DESIGN.md            # How it will be built
└── IMPLEMENTATION_PLAN.md       # Step-by-step tasks
```

### 2. Implement in Project

Actual code goes in project directories:

```bash
# For demo-app project
demo-app/
├── backend/
│   └── app/
│       └── api/
│           └── new_feature.py   # Implementation for JIRA-123
├── frontend/
│   └── src/
│       └── components/
│           └── NewFeature.tsx   # Implementation for JIRA-123
└── tests/
    └── test_new_feature.py      # Tests for JIRA-123
```

### 3. Track Completion

Update workflow with completion summary:

```bash
persona-framework/.ai/workflow/JIRA-123/
├── COMPLETION_SUMMARY.md        # What was implemented
└── INDEX.md                     # Links to actual code files
```

## Standard Workflow Files

Each workflow directory should contain:

### Required Files

1. **README.md** - Overview of the workflow
   - Business objective
   - Scope
   - Links to Jira ticket
   - Links to implementation code

2. **FEATURE_REQUIREMENTS.md** - Detailed requirements
   - User stories
   - Acceptance criteria
   - Functional requirements
   - Non-functional requirements

3. **SYSTEM_DESIGN.md** - Technical design
   - Architecture diagrams
   - Component design
   - Data models
   - API contracts

4. **IMPLEMENTATION_PLAN.md** - Implementation roadmap
   - Task breakdown
   - Dependencies
   - Timeline
   - Risk assessment

### Optional Files

5. **COMPLETION_SUMMARY.md** - Work summary
   - What was implemented
   - Files created/modified
   - Testing results
   - Deployment notes

6. **INDEX.md** - File navigation
   - Links to all workflow files
   - Links to implementation code
   - Quick reference guide

## Example: Jira Ticket Workflow

### Scenario
You have a Jira ticket `AEC-456: Add User Authentication`

### Step 1: AI Generates Requirements

```bash
persona-framework/.ai/workflow/AEC-456/
├── README.md
├── FEATURE_REQUIREMENTS.md      # OAuth 2.0, JWT, user management
├── SYSTEM_DESIGN.md            # Auth flow, database schema, API design
└── IMPLEMENTATION_PLAN.md       # 5 tasks, 2-week timeline
```

### Step 2: Implement in Project

```bash
demo-app/
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── oauth.py        # OAuth implementation
│   │   │   └── jwt.py          # JWT handling
│   │   └── api/v1/
│   │       └── auth.py         # Auth endpoints
│   └── tests/
│       └── test_auth.py        # Auth tests
└── frontend/
    └── src/
        ├── components/
        │   └── Login.tsx       # Login component
        └── services/
            └── auth.ts         # Auth service
```

### Step 3: Document Completion

```bash
persona-framework/.ai/workflow/AEC-456/
├── COMPLETION_SUMMARY.md        # Summary of implementation
└── INDEX.md                     # Links to demo-app/backend/app/auth/*
```

## Benefits of This Approach

### ✅ Separation of Concerns
- **Planning** (`.ai/workflow/`) vs. **Implementation** (`demo-app/`)
- Requirements don't clutter code directories
- Easy to find documentation for any ticket

### ✅ Reusability
- Design documents can be referenced for similar features
- Implementation patterns can be copied
- Knowledge base grows over time

### ✅ Traceability
- Clear link from Jira ticket → Requirements → Design → Code
- Easy to understand why decisions were made
- Audit trail for compliance

### ✅ Collaboration
- Designers/PMs review `.ai/workflow/` docs
- Developers implement in project directories
- Clear handoff between planning and coding

### ✅ AI-Friendly
- AI can generate comprehensive requirements
- AI can update plans without touching code
- AI can track progress across workflows

## Integration with Jira

### Linking Workflows to Jira

In your Jira ticket description, add:

```markdown
## AI-Generated Documentation
📁 Requirements & Design: `persona-framework/.ai/workflow/AEC-456/`
💻 Implementation: `demo-app/backend/app/auth/`

See [README](persona-framework/.ai/workflow/AEC-456/README.md) for details.
```

### Workflow Status in Jira

Update Jira ticket with workflow progress:

- **Requirements Complete** → `.ai/workflow/AEC-456/FEATURE_REQUIREMENTS.md` ✅
- **Design Complete** → `.ai/workflow/AEC-456/SYSTEM_DESIGN.md` ✅
- **Implementation Started** → Code in `demo-app/` 🚧
- **Implementation Complete** → `.ai/workflow/AEC-456/COMPLETION_SUMMARY.md` ✅

## Best Practices

### DO ✅

- Create a workflow directory for each Jira ticket
- Keep requirements and design in `.ai/workflow/`
- Put implementation code in project directories
- Link workflows to actual code files
- Update completion summaries when done

### DON'T ❌

- Don't put implementation code in `.ai/workflow/`
- Don't duplicate requirements across workflows
- Don't skip the design phase
- Don't forget to link Jira tickets
- Don't leave workflows incomplete

## Quick Reference

| Need | Location |
|------|----------|
| Requirements for JIRA-123 | `persona-framework/.ai/workflow/JIRA-123/FEATURE_REQUIREMENTS.md` |
| Design for JIRA-123 | `persona-framework/.ai/workflow/JIRA-123/SYSTEM_DESIGN.md` |
| Implementation plan | `persona-framework/.ai/workflow/JIRA-123/IMPLEMENTATION_PLAN.md` |
| Actual code | `demo-app/` or other project directories |
| Completion summary | `persona-framework/.ai/workflow/JIRA-123/COMPLETION_SUMMARY.md` |

---

**Framework Version**: v1.0.0  
**Last Updated**: 2024-11-17

