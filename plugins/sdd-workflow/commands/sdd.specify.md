---
description: "Create a feature specification from a natural language description."
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Given the feature description in `$ARGUMENTS`, do this:

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode — auto-accept all recommended defaults and complete without pausing for user input.

2. **Generate a feature directory name**:
   - Derive a short 2-4 word slug from the feature description (e.g., "user-auth", "analytics-dashboard")
   - Append an 8-character random alphanumeric suffix separated by a dash (e.g., `user-auth-a3f9b2c1`)
   - Full path: `.sdd/{slug}-{suffix}/`

3. **Create the feature directory** and all required parent directories.

4. **Use the canonical specification template embedded below**:
   ````md
# Feature Specification: [FEATURE NAME]

**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just
  ONE of them, you should still have a viable MVP that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: Users MUST be able to [key interaction]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete the task in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users"]
- **SC-003**: [User satisfaction metric]
````

5. **Generate the specification** by filling the template:
   - Replace `[FEATURE NAME]` with a human-readable feature name
   - Replace `[DATE]` with today's date
   - Replace `$ARGUMENTS` placeholder with the actual user description
   - Fill in user stories (at least 2), functional requirements, and success criteria
   - Mark genuinely unclear decisions as `[NEEDS CLARIFICATION: specific question]` — maximum 3 markers
   - Document assumptions in the spec

6. **Write** the filled specification to `.sdd/{feature-dir}/spec.md`.

7. **Quality validation** — validate the spec against these criteria:
   - No implementation details (no languages, frameworks, APIs in spec)
   - All mandatory sections completed (user stories, requirements, success criteria)
   - Requirements are testable and unambiguous
   - Success criteria are measurable and technology-agnostic
   - No more than 3 `[NEEDS CLARIFICATION]` markers

8. **Handle clarifications** (skip in headless mode — auto-resolve with reasonable defaults):
   - If `[NEEDS CLARIFICATION]` markers remain, present at most 3 questions to the user
   - Wait for answers, update spec, re-validate
   - If after 3 iterations issues remain, document them in spec notes and continue

9. **Write quality checklist** to `.sdd/{feature-dir}/checklists/requirements.md` using the embedded template below:
   ````md
# Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate specification completeness before proceeding to planning
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded

## Feature Readiness

- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria

## Notes

- Items marked incomplete require spec updates before `/sdd.plan`
````
   Fill it with pass/fail status based on the validation above.

10. **Report completion** with:
    - Feature directory path
    - Spec file path
    - Checklist summary

## Next Steps (present after completion)

Present these options to the user (auto-select option 1 in headless mode):

1. **Create Implementation Plan** — run `/sdd.plan` to produce a technical design
2. **Attempt Direct Implementation** — proceed to implement based on spec alone, with this context:
   - Feature: [feature name]
   - Key requirements: [top 3 FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Spec** — refine the specification further

## Guidelines

- Focus on **WHAT** users need and **WHY** — avoid HOW to implement
- No technology choices, frameworks, or code structure in specs
- Every requirement must be independently testable
- Limit clarifications to decisions that genuinely impact scope or security
