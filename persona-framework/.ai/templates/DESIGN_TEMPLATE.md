# SYSTEM_DESIGN.md: [Feature Name]

## 1. Executive Summary

[Brief overview of the system design approach, key architectural decisions, and high-level technical strategy]

## 2. Requirements Analysis Summary

### Key Requirements Identified
*   **[Requirement Category 1]**: [Summary of requirements]
*   **[Requirement Category 2]**: [Summary of requirements]
*   **[Requirement Category 3]**: [Summary of requirements]

### Technical Scope
*   **[Technology 1]**: [Purpose and usage]
*   **[Technology 2]**: [Purpose and usage]
*   **[Technology 3]**: [Purpose and usage]

### Complexity Assessment
*   **High Complexity**: [Areas of high complexity and why]
*   **Medium Complexity**: [Areas of medium complexity]
*   **Low Complexity**: [Areas of low complexity]

## 3. High-Level Design (HLD)

### Component Architecture Overview

```mermaid
[Insert architecture diagram - C4 Context, Component, or similar]
```

### Data Flow Architecture

```mermaid
[Insert data flow diagram - sequence diagram, flow chart, etc.]
```

### Integration Points
*   **[External System 1]**:
    *   **Mechanism**: [How integration works - API, webhook, etc.]
    *   **Data**: [What data is exchanged]
*   **[External System 2]**:
    *   **Mechanism**: [How integration works]
    *   **Data**: [What data is exchanged]

## 4. Low-Level Design (LLD)

### Component Structure Details

*   **[Component 1]**
    *   `[directory/]`
        *   `[file1.ext]`: [Purpose]
        *   `[file2.ext]`: [Purpose]
        *   `[subdirectory/]`
            *   `[file3.ext]`: [Purpose]

### File/Module Organization

```
[project-root]/
├── [directory1]/
│   ├── [file1.ext]
│   └── [file2.ext]
├── [directory2]/
│   ├── [subdirectory]/
│   │   └── [file3.ext]
│   └── [file4.ext]
└── [file5.ext]
```

### API Contracts

**[API Endpoint 1]**

```[language]
[Code example showing API contract - request/response]
```

**[API Endpoint 2]**

```[language]
[Code example showing API contract]
```

### Data Models

**[Model 1]**

```[language]
[Code example showing data model structure]
```

**[Model 2]**

```[language]
[Code example showing data model structure]
```

### Database Schema

**[Table/Collection 1]**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| [field1] | [type] | [constraints] | [description] |
| [field2] | [type] | [constraints] | [description] |

**Indexes**:
- [Index description]

**[Table/Collection 2]**

[Similar structure]

## 5. Technical Decisions

### Decision 1: [Decision Title]
*   **Context**: [Why this decision was needed]
*   **Options Considered**:
    1. [Option 1]: [Pros/Cons]
    2. [Option 2]: [Pros/Cons]
*   **Decision**: [Chosen option]
*   **Rationale**: [Why this option was chosen]

### Decision 2: [Decision Title]
[Similar structure]

## 6. Security Design

### Authentication & Authorization
*   **Authentication**: [How users are authenticated]
*   **Authorization**: [How access control is enforced]
*   **Session Management**: [How sessions are managed]

### Data Security
*   **Encryption at Rest**: [What and how]
*   **Encryption in Transit**: [What and how]
*   **PII Handling**: [How sensitive data is protected]

### Security Controls
*   **Input Validation**: [Validation strategy]
*   **Output Encoding**: [Encoding strategy]
*   **CSRF Protection**: [Protection mechanism]
*   **Rate Limiting**: [Rate limiting strategy]

## 7. Performance & Scalability

### Performance Targets
*   **Response Time**: [Target for key operations]
*   **Throughput**: [Requests per second]
*   **Concurrent Users**: [Expected concurrent load]

### Scalability Strategy
*   **Horizontal Scaling**: [How components scale horizontally]
*   **Vertical Scaling**: [When vertical scaling is used]
*   **Caching**: [Caching strategy and layers]
*   **Database Optimization**: [Indexing, partitioning, etc.]

### Performance Optimizations
*   **[Optimization 1]**: [Description]
*   **[Optimization 2]**: [Description]

## 8. Error Handling & Monitoring

### Error Handling Strategy
*   **Client Errors (4xx)**: [How handled]
*   **Server Errors (5xx)**: [How handled]
*   **Retry Logic**: [Retry strategy]
*   **Fallback Mechanisms**: [Fallback approach]

### Logging & Monitoring
*   **Logging**: [What's logged and where]
*   **Metrics**: [Key metrics to track]
*   **Alerts**: [Alert conditions and notifications]
*   **Tracing**: [Distributed tracing approach]

## 9. Testing Strategy

### Unit Testing
*   **Coverage Target**: [Percentage]
*   **Key Areas**: [What to focus on]

### Integration Testing
*   **Scope**: [What's tested]
*   **Approach**: [Testing approach]

### End-to-End Testing
*   **Critical Paths**: [User flows to test]
*   **Tools**: [Testing tools]

## 10. Deployment & Operations

### Deployment Strategy
*   **Environment**: [Dev, staging, production setup]
*   **CI/CD**: [Pipeline description]
*   **Rollback Plan**: [How to rollback]

### Operational Considerations
*   **Backup & Recovery**: [Backup strategy]
*   **Disaster Recovery**: [DR plan]
*   **Maintenance Windows**: [Planned maintenance]

---

## AI Generation Footprint

**Generated By**: Architect AI

**Framework Version**: v1.0.0

**Generation Date**: [ISO 8601 timestamp]

**Architecture Design Status**: ✅ COMPLETE

---

Co-authored by Architect AI using Persona-Driven AI Framework v1.0.0

