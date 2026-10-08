# Reproducible synthetic candidates

A candidate is an observation selected for subsequent analysis. This example publishes
the source observations, selection rule, selected records, and artifact seal so anyone
can inspect and reproduce the selection.

Every value, identifier, and timestamp here is invented for this example. The daily
timestamps are an arbitrary fixture convention. No market feed or research dataset is
used. The example demonstrates the public workflow and makes no economic claim.

## Public selection rule

Select an observation when its measurement is strictly greater than the preceding
observation's measurement. Equal values are excluded. The first observation has no
predecessor and is excluded.

The selector uses only the current and previous observations. Both must be available
by the decision timestamp. The causal audit checks all eligible observations before
selection and explicitly forbids future/outcome inputs.

## Published artifacts

- observations.csv: the full invented input sequence.
- candidates.json: selected IDs, decision timestamps, feature values, declared rule,
  causal audit summary, source digest, selector revision, and selector code digest.
- candidates.json.seal.json: artifact digest, dependency fingerprint, and exact ordered IDs.

All counts in these artifacts refer exclusively to this synthetic fixture.

## Reproduce and check

From the repository root, install the package and run:

```console
python -m pip install -e ".[dev]"
python examples/candidate_workflow.py --check
python -m pytest
```

The check regenerates the observations and candidate selection in memory, compares
the published bytes, and verifies the seal. Missing, changed, or stale artifacts fail
the check. To generate an independent copy:

```console
python examples/candidate_workflow.py --output-dir work/candidate_reproduction
python examples/candidate_workflow.py --output-dir work/candidate_reproduction --check
```

Omitting both options regenerates the committed fixture directory. A change to the
selector requires regenerating its manifest and seal. Tests also mutate a later
observation to check that earlier selected records remain unchanged.

Readers can challenge the selection rule by editing an independent copy, rerunning
the selector, and comparing the resulting records. Different rules produce different
candidate sets; each experiment should preserve its own rule and provenance.
