# Repository governance and branch protection

`main` is the protected integration branch. Contributions should arrive through pull requests.

## Required repository ruleset for `main`

Configure a GitHub repository ruleset targeting the default branch with these requirements:

- block force pushes;
- block branch deletion;
- require pull requests before merging;
- require at least 1 approving review;
- require Code Owner review;
- dismiss stale approvals when new commits are pushed;
- require conversation resolution before merge;
- require status checks to pass before merge;
- required checks: CI jobs for Python 3.10, 3.11 and 3.12;
- require branches to be up to date before merge when GitHub can evaluate the required checks consistently;
- do not allow bypass for external collaborators;
- restrict bypass to repository administrators/maintainers only for genuine recovery work;
- keep linear history optional; squash merge is preferred for external contributions.

The repository-wide code owner is declared in `.github/CODEOWNERS`.

## External contributions

External contributors should never need direct write access to `main`. The normal path is:

1. fork or create a feature branch;
2. open a pull request;
3. pass CI and review;
4. merge through GitHub.

Do not request API keys, brokerage credentials, private datasets or proprietary strategy material in issues or pull requests.

## Emergency recovery

If an administrator must bypass normal protections to recover the repository, document the reason in the commit or pull request and restore the normal protected workflow immediately afterward.
