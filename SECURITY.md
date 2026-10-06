# Security and data safety

Multimodal Market AI is a research framework. Please do not publish secrets, private market data, broker credentials, account information or restricted model/data assets in issues, pull requests or example files.

## Reporting a security issue

If you believe you found a vulnerability that could expose credentials, private files, arbitrary code execution or unsafe deserialization behavior, do not include live secrets or sensitive data in a public issue.

Open a minimal public issue only if it can be described safely without exposing the vulnerability in a way that puts users at immediate risk. Otherwise contact the repository owner through GitHub before publishing exploit details.

## Data safety rules

Contributors should assume that research folders may contain:

- licensed market data;
- model weights with separate licenses;
- API keys in local environment files;
- broker/account exports;
- large generated artifacts.

These should remain outside Git unless redistribution is explicitly allowed.

## Model and checkpoint safety

Do not add opaque executable artifacts or unsafe serialized objects without a clear reason and provenance. Prefer formats that do not execute arbitrary Python during loading where practical.

Document the source and license of model weights and checkpoints. Third-party model licenses remain in force even when code around them is Apache-2.0.

## Financial safety

The repository should not contain live credentials or code that silently opens real trades by default. Examples and tests should be safe-by-default, deterministic where possible, and clearly separated from any user-specific execution layer.
