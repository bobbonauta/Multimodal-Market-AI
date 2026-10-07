# Repository governance and branch protection

`main` is the canonical integration branch.

External contributions should arrive through pull requests. Repository owners/maintainers may also update `main` directly for verified internal synchronization and scoped maintenance work, provided the exact public diff has been reviewed and no private material is exposed.

## Required repository ruleset for `main`

The preferred ruleset should:

- block force pushes;
- block branch deletion;
- require status checks for external pull requests;
- require conversation resolution for external pull requests;
- require Code Owner review for external contributions when practical;
- keep CI for supported Python versions as required checks when code changes;
- prevent external collaborators from bypassing protections;
- allow repository owners/maintainers to perform verified direct synchronization or recovery work without creating artificial internal pull requests;
- preserve a reviewable Git history.

The repository-wide code owner is declared in `.github/CODEOWNERS`.

## Verified maintainer updates

Direct `main` updates by maintainers are reserved for already-reviewed canonical material, such as:

- synchronization of public-safe methodology from internal research;
- small repository maintenance fixes;
- documentation corrections whose content has already been validated;
- integration of verified work that should become the single source of truth.

Before writing directly to `main`:

1. verify the current `main` head;
2. inspect the exact diff;
3. remove credentials, private data, proprietary strategy logic and reverse-engineering clues;
4. run relevant tests/checks when code changes;
5. commit normally and never force-push over unrelated work.

Temporary branches used for proposals, explanations, drafts or isolated experiments are not automatically canonical. If a branch contains verified material that belongs to the project, absorb the verified content into `main`; otherwise leave it separate or close it when it has served its purpose.

## Operational changes must be versioned

Experiment-level operational decisions are not considered active merely because they appeared in chat, terminal history or an agent session.

Changes such as agent-role assignments, stop/resume decisions, split/protocol changes and other experiment-governance rules should be written and committed before the new rule is treated as canonical.

For AI-assisted work, prefer one active writer per branch/work tranche. Independent agents can audit read-only or work on separate, explicitly scoped areas until an explicit handoff occurs.

See [Experiment and AI-agent governance](EXPERIMENT_GOVERNANCE.md) for the full operational protocol.

## External contributions

External contributors should never need direct write access to `main`. The normal path is:

1. fork or create a feature branch;
2. open a pull request;
3. pass CI and review;
4. merge through GitHub.

Do not request API keys, brokerage credentials, private datasets or proprietary strategy material in issues or pull requests.

## Public/private synchronization

Internal research may feed general engineering lessons into the public repository, but the transfer must obey the public/private boundary.

Publish reusable workflow, causality rules, tests, generic schemas and sanitized evidence. Keep private the strategy itself, private data, private account/broker information and details that would materially enable reverse engineering.

See [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md).

## Emergency recovery

If an administrator must bypass normal protections to recover the repository, document the reason in the commit and restore the normal protected workflow immediately afterward.
