# Persona-Driven AI Framework - Usage Guide

## Quick Start: Creating a New Workflow

### Step 1: Create Workflow Directory

When you get a new Jira ticket (e.g., `AEC-456`), create a workflow directory:

```bash
cd persona-framework/.ai/workflow
mkdir AEC-456
cd AEC-456
```

### Step 2: Copy Templates

Copy the templates to your workflow directory:

```bash
# Copy all templates
cp ../../templates/WORKFLOW_README_TEMPLATE.md README.md
cp ../../templates/REQUIREMENTS_TEMPLATE.md FEATURE_REQUIREMENTS.md
cp ../../templates/DESIGN_TEMPLATE.md SYSTEM_DESIGN.md
cp ../../templates/PLAN_TEMPLATE.md IMPLEMENTATION_PLAN.md
```

### Step 3: Fill in the Templates

Use AI or manually fill in each template:

1. **README.md** - Overview and context
2. **FEATURE_REQUIREMENTS.md** - Detailed requirements
3. **SYSTEM_DESIGN.md** - Architecture and design
4. **IMPLEMENTATION_PLAN.md** - Task breakdown

### Step 4: Implement in Project

Write actual code in your project directory (e.g., `demo-app/`):

```bash
# Navigate to project
cd ../../../demo-app

# Create your implementation
mkdir -p backend/app/new_feature
touch backend/app/new_feature/__init__.py
touch backend/app/new_feature/service.py
```

### Step 5: Link Workflow to Code

Update your workflow's `README.md` with links to actual code:

```markdown
### Code Location
- `demo-app/backend/app/new_feature/service.py` - Main service implementation
- `demo-app/frontend/src/components/NewFeature.tsx` - UI component
- `demo-app/tests/test_new_feature.py` - Tests
```

### Step 6: Track Completion

When done, create a completion summary:

```bash
cd persona-framework/.ai/workflow/AEC-456
touch COMPLETION_SUMMARY.md
touch INDEX.md
```

## Workflow Examples

### Example 1: Simple Backend Feature

**Jira**: `API-789: Add User Profile Endpoint`

```
persona-framework/.ai/workflow/API-789/
├── README.md                    # Overview
├── FEATURE_REQUIREMENTS.md      # API spec, validation rules
├── SYSTEM_DESIGN.md            # Endpoint design, data model
└── IMPLEMENTATION_PLAN.md       # 3 tasks, 2 days

demo-app/backend/
├── app/api/v1/
│   └── profile.py              # Implementation
└── tests/
    └── test_profile.py         # Tests
```

### Example 2: Full-Stack Feature

**Jira**: `FEAT-123: Shopping Cart`

```
persona-framework/.ai/workflow/FEAT-123/
├── README.md
├── FEATURE_REQUIREMENTS.md      # User flows, cart logic
├── SYSTEM_DESIGN.md            # Frontend + backend design
├── IMPLEMENTATION_PLAN.md       # 8 tasks, 2 weeks
├── COMPLETION_SUMMARY.md        # What was built
└── INDEX.md                     # Links to code

demo-app/
├── backend/
│   ├── app/cart/
│   │   ├── models.py
│   │   ├── service.py
│   │   └── api.py
│   └── tests/test_cart.py
└── frontend/
    ├── src/components/Cart/
    │   ├── CartItem.tsx
    │   ├── CartSummary.tsx
    │   └── Checkout.tsx
    └── tests/Cart.test.tsx
```

### Example 3: Infrastructure Change

**Jira**: `INFRA-456: Migrate to PostgreSQL`

```
persona-framework/.ai/workflow/INFRA-456/
├── README.md
├── FEATURE_REQUIREMENTS.md      # Migration requirements
├── SYSTEM_DESIGN.md            # Database schema, migration plan
└── IMPLEMENTATION_PLAN.md       # 5 tasks, 1 week

demo-app/
├── infrastructure/
│   ├── database/
│   │   ├── schema.sql
│   │   └── migrations/
│   │       └── 001_initial.sql
│   └── terraform/
│       └── postgres.tf
└── backend/
    └── app/db/
        └── postgres.py
```

## Best Practices

### DO ✅

1. **Create workflow for every Jira ticket**
   - Even small tickets benefit from documentation
   - Helps with knowledge transfer

2. **Fill in requirements first**
   - Understand what you're building before designing
   - Get stakeholder approval on requirements

3. **Design before coding**
   - Think through architecture
   - Identify potential issues early

4. **Link workflows to code**
   - Make it easy to find implementation
   - Update links as code moves

5. **Complete the workflow**
   - Add completion summary when done
   - Document what was actually built vs. planned

### DON'T ❌

1. **Don't put code in `.ai/workflow/`**
   - This is for documentation only
   - Code goes in project directories

2. **Don't skip the design phase**
   - Jumping to code leads to rework
   - Design catches issues early

3. **Don't forget to update status**
   - Keep README.md status current
   - Update Jira ticket with workflow link

4. **Don't duplicate requirements**
   - Reference other workflows if similar
   - Link to shared design docs

5. **Don't leave workflows incomplete**
   - Finish what you start
   - Archive if cancelled

## AI-Assisted Workflow Creation

### Using AI to Generate Requirements

```bash
# Prompt for AI
"Generate detailed feature requirements for Jira ticket AEC-456: 
Add OAuth 2.0 authentication. Include user flows, functional requirements, 
and acceptance criteria. Use the template at 
persona-framework/.ai/templates/REQUIREMENTS_TEMPLATE.md"
```

### Using AI to Generate Design

```bash
# Prompt for AI
"Based on the requirements in FEATURE_REQUIREMENTS.md, generate a 
system design document. Include architecture diagrams, API contracts, 
and database schema. Use the template at 
persona-framework/.ai/templates/DESIGN_TEMPLATE.md"
```

### Using AI to Generate Plan

```bash
# Prompt for AI
"Based on the requirements and design, create an implementation plan 
with task breakdown, timeline, and risk assessment. Use the template at 
persona-framework/.ai/templates/PLAN_TEMPLATE.md"
```

## Integration with Development Workflow

### 1. Ticket Assignment
```
Developer assigned JIRA-123
↓
Create workflow: persona-framework/.ai/workflow/JIRA-123/
↓
Generate requirements, design, plan
```

### 2. Planning Review
```
Review requirements with PM/stakeholders
↓
Review design with tech lead
↓
Approve implementation plan
```

### 3. Implementation
```
Create feature branch: feature/JIRA-123
↓
Implement in demo-app/ (or other project)
↓
Link code in workflow README.md
```

### 4. Testing & Review
```
Write tests in demo-app/tests/
↓
Code review
↓
Update workflow with completion summary
```

### 5. Deployment
```
Deploy to production
↓
Update Jira ticket status
↓
Archive workflow (keep for reference)
```

## Maintenance

### Archiving Old Workflows

When a workflow is complete and deployed:

```bash
# Keep the workflow for reference
# No need to delete - it's documentation

# Optionally, mark as archived in README.md
echo "**Status**: ✅ Complete (Archived)" >> README.md
```

### Updating Templates

When you improve a template:

```bash
# Update the template
vim persona-framework/.ai/templates/REQUIREMENTS_TEMPLATE.md

# New workflows will use the updated template
# Old workflows keep their original structure
```

## Troubleshooting

### "Where should I put my code?"

**Answer**: In your project directory (e.g., `demo-app/`), NOT in `.ai/workflow/`.

### "Do I need all these documents for a small change?"

**Answer**: For very small changes (1-2 line fixes), you can skip the workflow. For anything that takes more than an hour, create a workflow.

### "Can I have multiple workflows for one Jira ticket?"

**Answer**: Generally no. One ticket = one workflow. If the ticket is too large, split it into multiple tickets.

### "What if requirements change mid-implementation?"

**Answer**: Update the FEATURE_REQUIREMENTS.md and note the change in README.md. Keep a changelog of major requirement changes.

---

**Framework Version**: v1.0.0  
**Last Updated**: 2024-11-17

