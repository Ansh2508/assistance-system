---
name: velth-e2e-live-verify
description: How to actually get and use a real authenticated Playwright session against VELTH production, AND how to do real live UI/UX visual inspection (screenshot + actually look), so a fix touching login-gated behavior (Begehung senden, the guided review, anything behind Zitadel) or a visual/layout claim can be verified against real production instead of code-level inference alone. Load whenever a task needs to prove something works or looks right in production beyond health checks and unauthenticated route probes — and load velth-prod-verify alongside it for the deploy-status half of the same problem.
---

# VELTH E2E live-verify — closing the "I couldn't log in" gap

## Why this exists

Every deploy-verification pass this project has run so far (see `velth-prod-verify`)
stops at the same wall: health checks, unauthenticated route probes, and
Playwright's own public-page suite all pass, and then the report has to say
"the actual authenticated click-through was not verified" — because there was
no way to log in. That gap got hit repeatedly in one real session:

- Pulling `zitadel-backend-pat-prod` and calling `POST /management/v1/users/human/_import`
  hit a Zitadel-side gateway bug (`dial tcp 127.0.0.1:8080: connect: connection refused`)
  — a real infra fault on that specific write endpoint, not a credential problem.
- The same PAT, called correctly with `x-zitadel-orgid`, returned `401 Errors.Token.Invalid`
  against `GET /management/v1/orgs/me` — the token itself had gone stale.
- Rotating that PAT requires `zitadel_device_flow.py`, an interactive OAuth
  device-code grant a human has to approve in a browser — correctly refused as a
  "don't touch prod credentials without asking" action.
- No Playwright/Puppeteer/computer-use MCP tool was available to click through
  the UI manually even with working credentials.

None of those were the actual best path. **Zitadel has a documented,
officially-supported flow specifically for this** — GitHub discussion
[zitadel/zitadel#7530](https://github.com/zitadel/zitadel/discussions/7530),
"Human user programmatic login for end2end testing scenarios" — that logs in a
REAL, EXISTING human test user without ever opening a browser or doing the
`_import` write call that hit the broken gateway. This skill is that flow,
adapted to this codebase, plus the Playwright `storageState` pattern
(industry-standard for exactly this — see Sources) that means you only ever
have to do the login dance ONCE, not on every test run.

## The standing precondition: one real test account, created once, by a human

This skill does NOT create a test account — `import_human_user` already exists
in `core/auth/zitadel_management.py` for that, and creating one is a real,
one-time production-identity-provider write that should go through the normal
"ask before touching prod credentials" gate, not be automated inside a test
skill. Once such an account exists (email + password, e.g.
`e2e-test@velth.io`), everything below is repeatable and read-mostly.

If no such account exists yet: stop here, tell the user exactly this, and ask
either (a) for them to create one via the real `/registrieren` signup flow and
hand you the credentials, or (b) for explicit go-ahead to use
`import_human_user` once, since that's a real production write worth a
confirmation, not a silent default.

## The login flow — no browser, no `_import`, uses the PAT that already exists

This is DIFFERENT from the `_import` call that hit the gateway bug. It logs in
an EXISTING user via the Session API + `x-zitadel-login-client` header, which
is Zitadel's own documented pattern for exactly this:

```
1. GET https://auth.velth.io/oauth/v2/authorization?<real OIDC params: client_id,
   redirect_uri, response_type=code, scope, code_challenge, ...>
   Headers: Authorization: Bearer <ZITADEL_SERVICE_TOKEN>
            x-zitadel-login-client: <the SERVICE USER's own Zitadel id, not the
            test user's — confirm this via zitadel_management.find_user_id_by_username
            on the service account's own userName, e.g. "velth-backend">
   Do NOT follow the redirect. Read the auth request id out of the `Location`
   header's query string (param name varies — inspect the actual redirect,
   don't assume).

2. POST https://auth.velth.io/v2/sessions
   Headers: Authorization: Bearer <ZITADEL_SERVICE_TOKEN>
   Body: {"checks": {"user": {"loginName": "e2e-test@velth.io"}}}
   -> returns sessionId + sessionToken (a user check, alone, is enough to start;
      confirm current API shape against the live OpenAPI/console before trusting
      this body verbatim — Zitadel's own docs page for this exact call did not
      give a fully worked example when checked 2026-09-22)

3. POST https://auth.velth.io/v2/sessions/<sessionId>
   Headers: Authorization: Bearer <ZITADEL_SERVICE_TOKEN>
   Body: {"checks": {"password": {"password": "<test account's real password>"}}}
   -> a password check requires the user check from step 2 to have already
      happened in this same session; do these as two calls, not one

4. POST https://auth.velth.io/oidc/v2/authorizations/<auth-request-id>/callback (or the
   equivalent OIDC Session API callback path — confirm exact path against the
   live console before trusting this verbatim)
   Body: {"session": {"sessionId": "...", "sessionToken": "..."}}
   -> returns a callback URL containing a real authorization `code`

5. POST https://auth.velth.io/oauth/v2/token
   Body: grant_type=authorization_code, code=<from step 4>, code_verifier=<from
   step 1's PKCE challenge>, redirect_uri=..., client_id=...
   -> returns a real access_token / id_token for the TEST USER, not the service
      account — this is what the frontend's own session would hold after a
      real login
```

**This has not yet been run end-to-end against this codebase's real Zitadel
instance.** Treat every exact path/param above as a strong, sourced starting
point, not a verified fact — confirm each one against the live
`https://auth.velth.io/.well-known/openid-configuration` and, ideally, a
Zitadel console session inspecting a real login's network calls, before
trusting it blind. The FIRST time this flow is run for real, expect to spend
one real debugging pass on it, and encode whatever the actual working shape
turns out to be back into this skill afterward — a skill that's never been
proven against the real system is a hypothesis, not a procedure (see
`velth-truth-gate`'s RELAYED-vs-EXECUTED distinction: everything above is
RELAYED from Zitadel's own docs/discussion until someone runs it here and it's
promoted to EXECUTED).

## Turning the resulting tokens into a Playwright session (do this ONCE)

Once step 5 above returns real tokens, don't re-derive them on every test run —
that's the whole point of `storageState`. Set the cookies/local-storage values
the frontend's own Zitadel client (`apps/frontend/lib/zitadelClient.ts`)
actually expects (read that file to confirm the exact storage key/shape it
reads on load — don't guess it), save via
`await context.storageState({ path: 'e2e-auth.json' })`, and reuse that file:

```ts
// playwright.config.ts — add a second project that reuses the saved state
{
  name: 'authenticated',
  use: { ...devices['Desktop Chrome'], storageState: 'e2e-auth.json' },
  dependencies: ['setup'], // a one-time project that runs the login flow above
}
```

`e2e-auth.json` is a real credential artifact — treat it exactly like a
secret: never commit it, store it only in the session's scratch directory, and
regenerate it (re-run the login flow) rather than assuming an old one is still
valid, since Zitadel tokens expire on their own schedule.

## UI/UX live inspection — the other half of "verify it works in prod"

A passing functional assertion (button click -> expected network call ->
expected route) proves the CODE path works. It says nothing about whether the
page is actually legible, correctly laid out, or free of a regression a user
would immediately notice. Both halves are needed; neither substitutes for the
other. This part does NOT require the login flow above for public pages, and
DOES for anything behind Zitadel — use whichever applies.

**The actual, proven pattern** (used successfully this session against real
production, unauthenticated pages — `https://www.velth.io/`, `/registrieren`,
`/begehung`'s pre-login gate):

```ts
// A throwaway spec file, deleted after use — this is inspection, not a
// permanent regression test (write a real one separately if the finding
// warrants a standing check).
import { test } from '@playwright/test';
import path from 'node:path';

const DIR = path.join(__dirname, '_ui_shots'); // scratch dir, never committed

test('screenshot <page>', async ({ page }) => {
  // For an authenticated page: load storageState per the section above first
  // (pass it via test.use({ storageState: '...' }) in this file, or run this
  // spec under the 'authenticated' Playwright project).
  await page.goto('/<route>');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1500); // let client-side rendering/animations settle
  await page.screenshot({ path: path.join(DIR, '<name>.png'), fullPage: true });
});
```

Run it against production directly: `BASE_URL=https://www.velth.io npx
playwright test <file> --project=chromium`. Cover at minimum: desktop AND a
real mobile viewport (`page.setViewportSize({ width: 390, height: 844 })` —
don't rely on the `mobile` project's default device alone if the fix is
layout-specific), and the specific screen the fix touches.

**Then actually look at the screenshots** — `Read` the PNG file and inspect it
visually, the same as reading any other tool output. Do not just confirm the
file was written; a screenshot nobody looked at proves nothing. Real, cheap
findings from doing this here: a cookie-consent banner overlapping a headline
on both desktop and mobile (cosmetic, pre-existing, not a regression — still
worth naming); confirming `/pricing` rendering identically to `/` was an
intentional `redirect('/')` by reading the route's source, not a broken page,
BEFORE reporting it as a finding — a screenshot alone can't distinguish
"looks the same" from "is the same page," only the code can.

**Clean up after**: delete the throwaway spec file and the screenshot
directory once inspected — this is a scratch tool, not a permanent test
artifact, and leaving `.png` files or ad-hoc spec files in the tree is exactly
the kind of stray output `git status` should never show after this skill runs.

## What this actually buys, honestly

- **Does** let a real Playwright test click "Analyse senden," submit a form, or
  navigate a guided review, and assert on the real resulting DOM/network calls
  — this is a genuine authenticated click-through, not a proxy for one.
- **Does** let a human (via the screenshots above) actually see what shipped,
  on real production, at real viewport sizes — not infer it from reading JSX.
- **Does not** mean every future task needs this — most fixes are provable at
  the code/deploy/unauthenticated-route level (see `velth-prod-verify`), and
  spinning up this whole flow for a change that doesn't touch login-gated
  behavior is real overhead for no real gain. Reach for this specifically when
  the thing that needs proving is behind a login and nothing else will do, or
  when a visual claim ("renders correctly," "no layout regression") needs an
  actual look rather than an assertion about it.

## Mechanical checklist

1. Confirm a real E2E test account exists; if not, stop and get one created by
   a human, or get explicit go-ahead to create it yourself once via
   `import_human_user`.
2. Pull `ZITADEL_SERVICE_TOKEN` from Secret Manager exactly as described in
   `velth-prod-verify` (scoped, one-time, delete-and-verify-deleted after).
3. Run the 5-step login flow above. Expect to debug the exact request/response
   shapes against the real system on the first attempt — budget for that, and
   update this skill with what actually worked once it does.
4. Save the resulting session as `storageState`, in the scratch directory only.
5. Add the `authenticated` Playwright project, write the test against the real
   authenticated flow, run it, and read the actual output/screenshots — don't
   trust a green exit code alone (see `build-test-verify`'s "if a test won't
   fail, it isn't a test" rule: prove this test can fail by breaking the flow
   on purpose once, same as was done for the Begehung regression test earlier
   this session).
6. Delete the pulled service token immediately after, verify deletion.

## Sources

- [zitadel/zitadel discussion #7530](https://github.com/zitadel/zitadel/discussions/7530)
  — "Human user programmatic login for end2end testing scenarios," the exact
  Session-API + `x-zitadel-login-client` flow this skill is built on. Read via
  a summarizing fetch, not the raw page — re-fetch and confirm directly before
  the first real run.
- Zitadel's own OpenID Connect grant-types doc — confirms Resource Owner
  Password Grant is explicitly NOT supported ("due to growing security
  concerns"), which is why the Session-API flow above exists as the
  documented alternative, not a workaround.
- Multiple 2026 Playwright authentication guides (getautonoma.com, currents.dev,
  checklyhq.com, testdino.com) — converge on the same `storageState`
  login-once-reuse-everywhere pattern, one explicitly warning "don't automate
  the live third-party OAuth login" and naming captured-session reuse as the
  correct alternative — which is exactly why this skill logs in via API, not
  via scripting the browser through Zitadel's hosted login page.
- `velth-prod-verify` (this project) — the credential-handling discipline
  (pull scoped, delete after, verify deletion) this skill reuses verbatim.
