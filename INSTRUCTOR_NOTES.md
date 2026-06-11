# Instructor Notes

HelpDeskLite is a training repository, not production software. It is meant to give students something realistic enough to reason about with GitHub Copilot while still being small enough to understand during a workshop.

## Documented Low-Risk Defects

1. Search is case sensitive.
   - Location: `helpdesk_lite/services/issue_service.py`
   - Current behavior: searching for `vpn` does not find `VPN Access`.
   - Exercise goal: ask Copilot to explain the behavior, propose a fix, add tests, and implement case-insensitive search.

2. Dashboard performs unnecessary queries.
   - Location: `helpdesk_lite/services/dashboard_service.py`
   - Current behavior: the dashboard counts open and closed issues, then separately loads open and closed issue lists.
   - Exercise goal: ask Copilot for impact analysis and then refactor to fewer queries.

3. Issue editing allows empty descriptions.
   - Location: `helpdesk_lite/services/issue_service.py`
   - Current behavior: create validates descriptions, but edit allows an empty description.
   - Exercise goal: ask Copilot to generate a failing test, fix validation, and update route behavior.

## Suggested Copilot Exercises

### Feature Planning

- Add issue categories.
- Add due dates.
- Add a user detail page showing assigned issues.
- Add priority filtering to the issues list.

Prompt idea:

```text
Review this repository and propose a small implementation plan for adding due dates to issues. Include files likely to change, tests to add, and risks.
```

### Impact Analysis

- Ask Copilot which files are affected by changing issue statuses.
- Ask Copilot how assignment rules flow from route to service to template.
- Ask Copilot to identify what breaks if users can be deleted.

Prompt idea:

```text
Trace how an issue is assigned to a user. Identify duplicated logic, missing checks, and tests that should be added before changing it.
```

### Test Generation

- Generate tests for invalid edit payloads.
- Generate route tests for close and reopen.
- Generate tests for comments on missing issues.
- Generate tests for duplicate user creation through the web form.

Prompt idea:

```text
Write pytest tests that expose the bug where editing an issue allows an empty description. Keep the tests consistent with the existing style.
```

### Bug Fixing

- Fix case-sensitive search.
- Fix empty-description edits.
- Make dashboard queries more efficient.

Prompt idea:

```text
Explain why the issue search is case sensitive, then implement a case-insensitive fix that works with SQLite. Update or add tests.
```

### Refactoring

- Extract an issue repository.
- Move issue list formatting out of the service.
- Replace string error lists with a small result object.
- Consolidate issue create and edit validation.

Prompt idea:

```text
Refactor IssueService to reduce mixed responsibilities without changing behavior. Keep the change small and preserve the existing tests.
```

### Code Review

Ask students to review one file or one feature path at a time.

Good review targets:

- `helpdesk_lite/services/issue_service.py`
- `helpdesk_lite/routes/issues.py`
- `helpdesk_lite/services/dashboard_service.py`

Prompt idea:

```text
Review issue_service.py for maintainability, correctness, and missing tests. Prioritize actionable findings with file and line references.
```

### Prompt Engineering

Compare broad and specific prompts:

- Broad: `Fix the issue search.`
- Better: `Add a failing test showing lowercase search does not find uppercase issue titles, then make search case-insensitive for SQLite.`
- Best: `Make the smallest safe change to issue search so lowercase queries find mixed-case titles. Preserve status filtering and ordering. Add tests for both search and status together.`

### Documentation Generation

- Ask Copilot to generate a short contributor guide.
- Ask Copilot to diagram the current request flow.
- Ask Copilot to update architecture notes after a refactor.

## Intentional TODO Comments

The code includes TODO comments for:

- authorization
- pagination
- caching
- audit logging

Use these as lightweight starting points for planning and prioritization exercises.

## Testing Gaps

The tests intentionally cover only part of the application. Untested or lightly tested areas include:

- HTML details for edit, close, reopen, and assign workflows
- Invalid form submissions through routes
- Dashboard query counts
- Authorization behavior
- Pagination behavior
- Audit logging behavior
- Empty issue descriptions during edit, except as a known-defect test

## Workshop Flow

1. Run the app and create a few issues manually.
2. Run the tests and inspect coverage informally by reading test names.
3. Ask Copilot to explain one route and one service.
4. Pick one documented defect.
5. Ask Copilot for a plan before coding.
6. Ask Copilot to generate a failing test.
7. Implement the fix.
8. Ask Copilot for a code review.
9. Refactor one small area.
10. Update documentation to reflect the change.
