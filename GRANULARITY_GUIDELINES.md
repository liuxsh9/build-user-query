# Library Tag Granularity Guidelines

## Overview

This document defines the three-tier granularity system for Library tags in the capability taxonomy. Consistent granularity ensures tags are neither too broad (losing specificity) nor too fine (becoming unmaintainable).

## Three-Tier Granularity System

### Library-Level
**Definition:** Tags representing an entire framework or library that is commonly used as a cohesive whole.

**When to use:**
- The library is monolithic with tightly integrated components
- Developers typically learn and use the entire library together
- The library name itself represents a distinct capability
- Splitting into modules would not add meaningful distinction

**Examples:**
- `react` - Frontend framework used as a whole
- `django` - Full-stack web framework
- `pytorch` - Deep learning framework
- `express` - Node.js web framework
- `pytest` - Python testing framework

### Module-Level
**Definition:** Tags representing a major subsystem or module within a library that provides distinct, separable capabilities.

**When to use:**
- The module represents a significant, self-contained subsystem
- Developers often specialize in specific modules
- The module has its own learning curve and documentation section
- The capability is worth tracking independently for training data coverage

**Examples:**
- `django-orm` - Django's database ORM system
- `pytorch-nn` - PyTorch neural network module
- `pandas-dataframe` - Pandas DataFrame operations
- `react-router` - React routing library
- `sqlalchemy-core` - SQLAlchemy core query building

### Component-Level
**Definition:** Tags representing specific features, APIs, or patterns within a module that are frequently used independently.

**When to use:**
- The component is a distinct, frequently-used feature
- It represents a learnable skill or pattern
- Developers often search for or discuss this component specifically
- It appears commonly in Stack Overflow questions or documentation

**Examples:**
- `react-hooks` - React Hooks API
- `pandas-groupby` - Pandas groupby operations
- `django-middleware` - Django middleware system
- `pytorch-autograd` - PyTorch automatic differentiation
- `express-middleware` - Express middleware pattern

## Decision Criteria

### Library vs Module
Ask: "Do developers typically use this as a complete unit, or do they work with distinct subsystems?"

- **Library**: Used as a whole → `flask`
- **Module**: Distinct subsystems → `flask-blueprints`, `flask-extensions`

### Module vs Component
Ask: "Is this a major subsystem, or a specific feature within a subsystem?"

- **Module**: Major subsystem → `django-orm`
- **Component**: Specific feature → `django-querysets`, `django-migrations`

### Component vs Function
Ask: "Does this represent a learnable pattern/skill, or just a single function call?"

- **Component**: Learnable pattern → `react-hooks` (useState, useEffect, custom hooks)
- **Function**: Single function → ❌ `react-usestate` (too fine, don't create)

## Examples by Subcategory

### Web Subcategory

| Library-Level | Module-Level | Component-Level |
|---------------|--------------|-----------------|
| `react` | `react-router` | `react-hooks` |
| `vue` | `vue-router` | `vue-composition-api` |
| `django` | `django-orm` | `django-middleware` |
| `fastapi` | `fastapi-dependencies` | `fastapi-background-tasks` |
| `express` | `express-router` | `express-middleware` |

### Data Subcategory

| Library-Level | Module-Level | Component-Level |
|---------------|--------------|-----------------|
| `pandas` | `pandas-dataframe` | `pandas-groupby` |
| `numpy` | `numpy-array` | `numpy-broadcasting` |
| `pytorch` | `pytorch-nn` | `pytorch-autograd` |
| `tensorflow` | `tensorflow-keras` | `tensorflow-datasets` |
| `scikit-learn` | `sklearn-preprocessing` | `sklearn-pipelines` |

### Infrastructure Subcategory

| Library-Level | Module-Level | Component-Level |
|---------------|--------------|-----------------|
| `docker` | `docker-compose` | `docker-volumes` |
| `kubernetes` | `kubectl` | `k8s-deployments` |
| `terraform` | `terraform-providers` | `terraform-modules` |
| `ansible` | `ansible-playbooks` | `ansible-roles` |
| `github-actions` | `github-actions-workflows` | `github-actions-matrix` |

### Testing Subcategory

| Library-Level | Module-Level | Component-Level |
|---------------|--------------|-----------------|
| `pytest` | `pytest-fixtures` | `pytest-parametrize` |
| `jest` | `jest-matchers` | `jest-mocks` |
| `selenium` | `selenium-webdriver` | `selenium-waits` |
| `cypress` | `cypress-commands` | `cypress-intercept` |
| `junit` | `junit-assertions` | `junit-parameterized` |

### Database Subcategory

| Library-Level | Module-Level | Component-Level |
|---------------|--------------|-----------------|
| `sqlalchemy` | `sqlalchemy-orm` | `sqlalchemy-relationships` |
| `prisma` | `prisma-client` | `prisma-migrations` |
| `mongoose` | `mongoose-schemas` | `mongoose-middleware` |
| `typeorm` | `typeorm-entities` | `typeorm-decorators` |
| `sequelize` | `sequelize-models` | `sequelize-associations` |

## Edge Cases and Decision Rationale

### Edge Case 1: Standalone vs Integrated Components
**Question:** React Router is often used with React. Is it module-level or library-level?

**Decision:** **Module-level** (`react-router`)

**Rationale:** While it can be used standalone, it's primarily a subsystem of the React ecosystem. It represents a distinct capability (routing) within React applications.

### Edge Case 2: Multiple Granularities for Same Library
**Question:** Can we have both `pandas` and `pandas-dataframe`?

**Decision:** **Yes, both are valid**

**Rationale:**
- `pandas` (library-level) for general Pandas usage
- `pandas-dataframe` (module-level) for DataFrame-specific operations
- `pandas-groupby` (component-level) for groupby-specific patterns

This allows different levels of specificity for different training scenarios.

### Edge Case 3: Ambiguous Module Boundaries
**Question:** Is `django-rest-framework` a module of Django or a separate library?

**Decision:** **Library-level** (`django-rest-framework`)

**Rationale:** Despite the name, DRF is a separate package with its own versioning and can be used independently. It's not a built-in Django module.

### Edge Case 4: Very Small Libraries
**Question:** Should tiny utility libraries like `lodash` have module-level tags?

**Decision:** **Library-level only** for small libraries

**Rationale:** If the entire library can be learned in a few hours, module-level tags add unnecessary complexity. Exception: if specific utilities are extremely common (e.g., `lodash-debounce` if frequently discussed).

### Edge Case 5: Language-Specific Patterns
**Question:** Are patterns like "React Hooks" components or concepts?

**Decision:** **Component-level in Library category**

**Rationale:** Hooks are a specific API/feature of React, not a general programming concept. They belong in Library category with `language_scope: ["javascript", "typescript"]`.

## Validation Checklist

When creating or reviewing a Library tag, ask:

- [ ] Is this tag at the appropriate granularity level?
- [ ] Does it represent a distinct, learnable capability?
- [ ] Would developers search for or discuss this specifically?
- [ ] Is it neither too broad (losing specificity) nor too fine (unmaintainable)?
- [ ] Does it have clear examples and use cases?
- [ ] Is the granularity level explicitly documented in metadata?

## Metadata Field

All Library tags MUST include a `granularity` field:

```yaml
granularity: library  # or: module, component
```

This enables filtering and analysis by granularity level.
