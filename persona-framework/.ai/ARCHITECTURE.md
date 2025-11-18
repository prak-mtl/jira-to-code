# Persona-Driven AI Framework Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         JIRA TICKET                             │
│                         (e.g., AEC-456)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              PLANNING & DOCUMENTATION                           │
│         persona-framework/.ai/workflow/AEC-456/                 │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ REQUIREMENTS.md  │  │ SYSTEM_DESIGN.md │  │    PLAN.md   │ │
│  │                  │  │                  │  │              │ │
│  │ • User flows     │  │ • Architecture   │  │ • Tasks      │ │
│  │ • Acceptance     │  │ • API contracts  │  │ • Timeline   │ │
│  │   criteria       │  │ • Data models    │  │ • Risks      │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      README.md                           │  │
│  │  Links to implementation code in demo-app/               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION                               │
│                      demo-app/                                  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   Backend    │  │   Frontend   │  │   Infrastructure     │ │
│  │              │  │              │  │                      │ │
│  │ • API code   │  │ • Components │  │ • Terraform          │ │
│  │ • Services   │  │ • Styles     │  │ • CloudFormation     │ │
│  │ • Models     │  │ • Tests      │  │ • Serverless         │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      tests/                              │  │
│  │  Unit, Integration, E2E tests                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT                                 │
│                   (AWS, GCP, Azure, etc.)                       │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
project-root/
│
├── persona-framework/.ai/          # 📋 PLANNING & DOCUMENTATION
│   ├── README.md                   # Framework overview
│   ├── USAGE_GUIDE.md             # How to use the framework
│   ├── FRAMEWORK_SETUP_COMPLETE.md # Setup completion guide
│   │
│   ├── templates/                  # 📝 Templates for new workflows
│   │   ├── REQUIREMENTS_TEMPLATE.md
│   │   ├── DESIGN_TEMPLATE.md
│   │   ├── PLAN_TEMPLATE.md
│   │   └── WORKFLOW_README_TEMPLATE.md
│   │
│   └── workflow/                   # 🗂️ Individual workflow directories
│       ├── JIRA-123/              # Example: Jira ticket
│       │   ├── README.md
│       │   ├── FEATURE_REQUIREMENTS.md
│       │   ├── SYSTEM_DESIGN.md
│       │   ├── IMPLEMENTATION_PLAN.md
│       │   ├── COMPLETION_SUMMARY.md
│       │   └── INDEX.md
│       │
│       ├── DASHBOARD-001/         # Example: Complete workflow
│       │   └── [same structure]
│       │
│       └── FEATURE-XYZ/           # Example: Feature workflow
│           └── [same structure]
│
└── demo-app/                       # 💻 IMPLEMENTATION CODE
    ├── README.md                   # Quick start guide
    │
    ├── backend/                    # Backend implementation
    │   ├── app/
    │   │   ├── api/
    │   │   ├── auth/
    │   │   ├── services/
    │   │   └── models/
    │   └── tests/
    │
    ├── frontend/                   # Frontend implementation
    │   ├── src/
    │   │   ├── components/
    │   │   ├── services/
    │   │   ├── types/
    │   │   └── utils/
    │   └── tests/
    │
    ├── infrastructure/             # Infrastructure as Code
    │   ├── terraform/
    │   ├── cloudformation/
    │   └── serverless.yml
    │
    └── demo_data/                  # Sample/test data
        ├── mock_data.json
        └── generate_demo_data.py
```

## Information Flow

### 1. Planning Phase

```
Jira Ticket Created
        ↓
AI Generates Requirements
        ↓
Stakeholders Review
        ↓
AI Generates Design
        ↓
Tech Lead Reviews
        ↓
AI Generates Implementation Plan
        ↓
Team Approves
```

**Output**: Complete workflow in `persona-framework/.ai/workflow/JIRA-123/`

### 2. Implementation Phase

```
Developer Creates Feature Branch
        ↓
Implements Code in demo-app/
        ↓
Writes Tests
        ↓
Links Code in Workflow README
        ↓
Code Review
        ↓
Merge to Main
```

**Output**: Working code in `demo-app/` + links in workflow

### 3. Completion Phase

```
Create COMPLETION_SUMMARY.md
        ↓
Update Workflow Status
        ↓
Deploy to Production
        ↓
Update Jira Ticket
        ↓
Archive Workflow (keep for reference)
```

**Output**: Complete documentation trail

## Workflow Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW STATES                          │
└─────────────────────────────────────────────────────────────┘

1. CREATED
   └─> Workflow directory created
       Templates copied
       
2. PLANNING
   └─> Requirements written
       Design documented
       Plan created
       
3. APPROVED
   └─> Stakeholders approved requirements
       Tech lead approved design
       Team approved plan
       
4. IN_PROGRESS
   └─> Code being written in demo-app/
       Tests being written
       Regular updates to workflow
       
5. REVIEW
   └─> Code review in progress
       Testing in progress
       Documentation review
       
6. COMPLETE
   └─> Code merged
       Tests passing
       Deployed to production
       COMPLETION_SUMMARY.md created
       
7. ARCHIVED
   └─> Workflow kept for reference
       Linked from Jira ticket
       Available for future reference
```

## Integration Points

### With Jira

```
Jira Ticket
    ↓
    ├─> Link to workflow: persona-framework/.ai/workflow/JIRA-123/
    ├─> Link to code: demo-app/backend/app/feature/
    └─> Status updates from workflow
```

### With Git

```
Git Branch: feature/JIRA-123
    ↓
    ├─> Commit messages reference JIRA-123
    ├─> PR description links to workflow
    └─> Code in demo-app/ implements workflow plan
```

### With CI/CD

```
CI/CD Pipeline
    ↓
    ├─> Runs tests from demo-app/tests/
    ├─> Deploys infrastructure from demo-app/infrastructure/
    └─> Updates workflow status on success/failure
```

## Benefits Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                    TRADITIONAL APPROACH                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Code + Requirements + Design all mixed together            │
│                                                              │
│  ❌ Hard to find documentation                              │
│  ❌ Requirements scattered across files                     │
│  ❌ Design decisions lost in code comments                  │
│  ❌ No clear separation of concerns                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘

                            ↓ ↓ ↓

┌──────────────────────────────────────────────────────────────┐
│              PERSONA-DRIVEN AI FRAMEWORK                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Planning (.ai/workflow/) ←→ Implementation (demo-app/)      │
│                                                              │
│  ✅ Clear separation of concerns                            │
│  ✅ Easy to find documentation                              │
│  ✅ Requirements in one place                               │
│  ✅ Design decisions documented                             │
│  ✅ Code stays clean and focused                            │
│  ✅ AI can help with planning                               │
│  ✅ Knowledge base grows over time                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Scalability

### Small Team (1-5 developers)

```
persona-framework/.ai/workflow/
├── JIRA-001/
├── JIRA-002/
├── JIRA-003/
└── JIRA-004/

demo-app/
└── [single project]
```

### Medium Team (5-20 developers)

```
persona-framework/.ai/workflow/
├── BACKEND-001/
├── BACKEND-002/
├── FRONTEND-001/
├── FRONTEND-002/
├── INFRA-001/
└── INFRA-002/

demo-app/
├── backend/
├── frontend/
└── infrastructure/
```

### Large Team (20+ developers)

```
persona-framework/.ai/workflow/
├── TEAM-A/
│   ├── JIRA-001/
│   └── JIRA-002/
├── TEAM-B/
│   ├── JIRA-003/
│   └── JIRA-004/
└── SHARED/
    └── EPIC-001/

project-1/
project-2/
project-3/
```

---

**Framework Version**: v1.0.0  
**Last Updated**: 2024-11-17

