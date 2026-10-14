---
name: planning-with-issues
description: Use when entering plan mode, creating implementation plans, or the user asks to plan any feature - requires GitHub issue integration and 3 iterative review rounds with user questions before finalizing
---

# Planning with GitHub Issues

## Overview

Every plan goes through 3 iterative review rounds with the user, and is cross-referenced against open GitHub issues. Plans are never finalized on the first draft.

**Core principle:** Plans improve through iteration and user dialogue. Never finalize a plan without 3 rounds of questions and GitHub issue awareness.

## The Process

### Step 0: Fetch GitHub Issues

Before writing anything:
1. Run `gh issue list --state open --limit 30` to get all open issues
2. Read each issue with `gh issue view <N>` to understand full context
3. Identify which issues are relevant to the current task
4. Note which issues could be partially or fully addressed by the plan

### Step 1: Draft Plan (Round 1)

Write the initial plan draft. Then STOP and ask the user **at least 4 questions** about:
- **Scope**: "Should we also address issue #N which overlaps with this?"
- **Priorities**: "Which of these features matters most to you?"
- **Design preferences**: Specific UI/UX/architecture choices
- **Edge cases**: Things the plan doesn't cover yet
- **Integration**: How this connects to existing features

Present relevant GitHub issues and ask if any should be incorporated or closed.

**Say:** "This is Round 1 of 3. Here are my questions before I refine the plan:"

### Step 2: Refine Plan (Round 2)

Incorporate user answers. Improve the plan. Then STOP and ask **at least 3 more questions** about:
- **Implementation details**: Specific technical choices
- **Order of operations**: What to build first
- **Verification**: How to test/verify each phase
- **Missing pieces**: Anything the user expected that isn't there

**Say:** "This is Round 2 of 3. The plan is stronger now. A few more questions:"

### Step 3: Final Review (Round 3)

Make final adjustments. Present the complete plan with:
- Summary of all changes from rounds 1-2
- GitHub issues that will be addressed/closed
- GitHub issues to create for follow-up work
- Final **2+ questions** about anything still ambiguous

**Say:** "This is Round 3 of 3 (final). Here's the complete plan and my last questions:"

### Step 4: After Approval — Update GitHub

Once the user approves:
- Comment on relevant issues noting they'll be addressed
- Move completed issues to done after implementation
- Create new issues for out-of-scope items discovered during planning

## GitHub Issue Tracking During Execution

While implementing a plan:
- When a task addresses an issue, note it
- After completing work that closes an issue, close it with a comment referencing the commit
- If new issues are discovered, create them

## Red Flags

| Thought | Reality |
|---------|---------|
| "The plan is obvious, skip to coding" | Plans always improve with iteration. Do all 3 rounds. |
| "I'll check issues later" | Issues inform the plan. Check FIRST. |
| "One round of questions is enough" | 3 rounds catches things 1 round misses. Every time. |
| "The user seems impatient" | Quick questions save hours of rework. Ask them. |
| "No relevant issues exist" | Still do 3 rounds of questions. Issues are a bonus, not the core. |

## Question Quality

**Good questions** are specific and actionable:
- "Should the toast auto-dismiss after 3s or 5s?"
- "Issue #3 mentions drag-to-reorder sessions. Include in this plan or separate?"

**Bad questions** are vague:
- "Does this look good?"
- "Anything else?"
