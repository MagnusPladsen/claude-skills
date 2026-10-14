---
name: test-run
description: Use when you want an interactive manual test run for the work in progress (a feature branch, a bug fix, review fixes or a named flow), published as a Claude artifact with tick-box steps, results, notes and screenshots that you read back afterwards.
---

<!-- magnus-pladsen-kit -->

# /test-run

Build an interactive manual test run for the work in progress and publish it as a Claude artifact: sections of tests,
each with tick-box steps, a preferred outcome, copyable checks (SQL, shell, log lines, URLs), Pass / Fail / Blocked /
Skip, notes and screenshots — all saved on the page. Then read the results back and act on them.

## Scope

Use this skill for manual testing of anything in the current repository: a feature branch before its PR, a bug fix, a
review round's fixes, or a flow the user names.

## Arguments

Optional free text: a ticket reference (`#1234`, `PROJ-123`), a PR number, a flow ("payment links", "check-in"), or an
environment ("staging", "deployed dev"). Arguments narrow the scope; they never replace grounding the tests in the code.

## Instructions

### 1. Resolve what to test

Work through these in order and stop at the first that gives a clear scope:

1. **Arguments** the user passed.
2. **The conversation**: the feature just built, review findings, fixes, known risks and things marked "not tested".
3. **The branch**:

   ```bash
   BRANCH=$(git branch --show-current)
   DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
   BASE=${DEFAULT:-main}
   for b in dev develop; do
     if [ "$BRANCH" != "$b" ] && git show-ref --quiet "refs/remotes/origin/$b"; then BASE=$b; break; fi
   done
   git fetch -q origin "$BASE"
   git log --oneline "origin/$BASE..HEAD"
   git diff --stat "origin/$BASE...HEAD"
   ```

   If the branch name carries a ticket reference, fetch its title and description when the tracker is reachable:
   - Jira-style key (`PROJ-123`): the Atlassian MCP.
   - Number on an Azure DevOps remote (`dev.azure.com/<org>/<project>/...`):
     `az boards work-item show --id "$ID" --org "https://dev.azure.com/<org>"`.
   - Number on a GitHub remote: `gh issue view "$ID"`.

   Skip this silently when the tool is missing or not logged in.
4. **Ask**: on the base or default branch with no arguments, no diff and nothing in the conversation — or when the diff is too
   broad to test in one run — ask with `AskUserQuestion`: which area, which environment (local, deployed dev), and
   whether to include regression of neighbouring flows. Offer the areas the recent commits touch as options.

State the resolved scope in one line before building.

### 2. Turn changes into tests a person can run

Read the diff of every file in scope — not only the stat. For each user-visible behaviour, cover what applies:

- **Happy path**: the everyday flow, end to end.
- **Failure paths**: declined, invalid, unauthorised, a service down.
- **Timing and edges**: back and forward, reload, two tabs, slow network (DevTools throttling), double clicks,
  retries, expiry and background jobs.
- **Data correctness**: what the database, emails, PDFs and third-party portals should show afterwards.
- **Regression**: neighbouring flows the diff touches but did not set out to change (for example the other payment
  provider when payment code changed).
- **Security**: authorization, tenant isolation, secrets in logs.

Skip what the unit and integration tests already prove, unless it only shows up in a real environment — UI, external
services, timing, emails.

Put a **setup** section first (services, tunnels, feature flags, seed data) and a **teardown** section last. Every test
that changes local configuration or data needs a matching restore step, with the original value noted first.

Priority per test:

- `must` — the change is not done until this passes.
- `should` — likely to catch a real problem.
- `nice` — worth doing when there is time.

Aim for 10–30 tests. More than that means the scope should be split into two runs.

### 3. Ground every detail in the code

A test that names a button that does not exist wastes the tester's time. Before writing a detail, confirm it:

- **UI text**: grep the exact labels, headings and toasts from the components, in the UI's own language.
- **URLs and routes**: from the frontend router (for example `app/**` in Next.js) and the backend route definitions
  (controller attributes, route files).
- **Log lines**: grep the logger call and quote a stable fragment of its message template, never a guessed sentence.
- **SQL**: table and column names from the schema: ORM models or DB context, and the migrations. Checks are `SELECT` only. Setup or
  teardown `UPDATE`s must say which value to restore. Never put secrets, tokens or real customer data in a check.
- **Test data**: test cards, accounts and slugs from the READMEs, runbooks and seed data.
- **API calls**: name the saved request (Bruno, Postman, `.http` files) when the repo has one.
- **Environment commands**: from the READMEs, `package.json` scripts, `Makefile` or compose files.

Anything you cannot confirm gets `(unverified)` in the step, and you say so when you hand the run over.

### 4. Write the plan

The page renders a JSON plan (schema below). Writing rules:

- `why`: one sentence on what would go wrong if this broke, in the user's words, not the code's.
- `steps`: imperative, one action each, at most 8. Put the concrete value in the step (the card number, the URL).
- `outcome`: observable and specific — what the screen, email, log or query shows. Several outcomes are fine; each is
  one checkable fact.
- `checks`: only when they help confirm an outcome. Kinds: `sql`, `shell`, `log`, `http`, `url`, `text`.
- `needs`: test ids that must run first (setup, a shortened expiry).
- `note`: a known limitation or a way the test can legitimately go differently ("if the timing missed, mark Skip").
- Inline `` `backticks` `` render as code. No other markup.
- Test ids: an uppercase area prefix and a number (`SHOP-1`, `LINK-3`). Keep ids stable across updates — results are
  keyed by them.

### 5. Build and publish

1. Load the `artifact-design` and `artifact-capabilities` skills, as the Artifact tool requires. The template already
   follows them; do not restyle it beyond what the subject genuinely needs.
2. Copy `~/.claude/skills/test-run/template.html` into the scratchpad under a short, specific name
   (`1234-test-run.html`).
3. Replace the contents of `<script type="application/json" id="run-plan">` with the plan. Escape every `<` in the JSON
   as `\u003c`, so no string can close the script block.
4. Set `<title>` to the plan's `title`: a short name for this run ("Checkout Test Run"), not "Test plan".
5. **New run**: leave `run-state` as `{"results":{}}`.
   **Updating a run the user already started**: read the published artifact first (`Artifact` action `read` with its
   URL), copy its `run-state` JSON into the new file unchanged, bump the plan's `version`, and republish to the same
   URL. Results for test ids that still exist are kept; removed ids are ignored.
6. Publish with `capabilities: {"artifact": {}, "assets": {}}`: `artifact` saves the run to the page, `assets` stores
   screenshots. Declaring `assets` makes the page organization-internal. First publish needs an `icon` (`checklist`) and a
   one-sentence `description`.
7. Do not build a screenshot or DOM test loop around the page. Publish, and let the user report anything broken.

### 6. Hand it over

Reply with the link and at most a few points:

- How it works, in one or two lines (tick steps, pick a result, notes and screenshots save to the page).
- Tests that need you: API-only checks, sandbox calls with the user's test keys, data you have to seed.
- Tests that change configuration or data, and which teardown test undoes them.
- Anything marked `(unverified)`.

### 7. Read the results back

When the user says they are done, or asks what failed:

1. `Artifact` action `read` with the run's URL, and parse the `run-state` JSON.
2. List failed and blocked tests with their notes, then untested `must` tests.
3. For screenshots, `Artifact` action `list` with `scope: "assets"`, then `read` with `path` set to each asset id the
   failed tests reference, and look at them before diagnosing.
4. Diagnose each failure against the code, propose fixes, and ask before changing anything. Problems outside the
   current ticket become new tickets in the project's tracker, not quiet fixes on this branch.

The page saves by republishing itself, so each save arrives as an "artifact changed" notification. That is the user
saving progress: acknowledge it in one short line at most, and do not re-read or republish unless asked.

## Plan schema

```json
{
  "version": "1",
  "title": "Checkout Test Run",
  "eyebrow": "#1234 · local test run · shop",
  "intro": "Work through the tests in order. Tick each step, then mark the test Pass, Fail, Blocked or Skip.",
  "meta": { "branch": "1234", "commit": "e1b74a354", "generated": "2026-09-15" },
  "facts": [
    { "label": "Good card", "value": "4268 2700 8737 4847", "mono": true },
    { "label": "Declined card", "value": "4925 0000 0000 0087", "mono": true }
  ],
  "groups": [
    {
      "id": "shop",
      "title": "Buying in the shop",
      "intro": "The everyday path: a guest buys tickets and pays inside the page.",
      "tests": [
        {
          "id": "SHOP-1",
          "title": "Buy a ticket with the good test card",
          "priority": "must",
          "minutes": 5,
          "needs": ["SETUP-1"],
          "why": "The receipt should only say the order is confirmed once the payment is recorded.",
          "steps": ["Open the shop and add a ticket.", "Pay with `4268 2700 8737 4847`."],
          "outcome": ["The receipt shows “Order confirmed” with the QR code."],
          "checks": [
            { "kind": "sql", "label": "Newest orders", "code": "SELECT TOP 5 OrderNumber, OrderStatus FROM [Order] ORDER BY OrderId DESC;" },
            { "kind": "log", "label": "API log contains", "code": "Payment captured" },
            { "kind": "url", "label": "Shop", "code": "http://localhost:3000/order/tickets" }
          ],
          "note": "Optional."
        }
      ]
    }
  ]
}
```

Required per test: `id`, `title`, `why`, `steps`, `outcome`. Everything else is optional; `priority` defaults to
`should`.

## Notes

- The run is the user's record; never publish results they did not enter.
- Keep secrets out of the plan: reference `.env` keys by name, never by value.
- One run per scope. For a second environment (deployed dev after local), publish a separate run, so both sets of
  results survive.
