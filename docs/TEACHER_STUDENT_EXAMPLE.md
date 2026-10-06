# Teacher-to-student workflow example

This example shows how a contributor can use a capable multimodal model as a teacher and then train a smaller task-specific student.

## 1. Build causal examples

Each example should be frozen at one decision timestamp and contain only information available at that moment:

```text
RID
symbol
base timestamp
base timeframe history
higher-timeframe closed history
optional rendered images
optional deterministic numerical context
```

No future price path or outcome belongs in the teacher input.

## 2. Query the teacher

Ask for a compact, machine-readable structure rather than a long essay.

Example target schema:

```json
{
  "regime": "trend|range|transition|uncertain",
  "structure": "continuation|pullback|breakout|reversal|unclear",
  "alignment": "strong|partial|conflict",
  "direction": "long|short|neutral",
  "ambiguity": 0.0
}
```

Preserve:

- teacher model name and revision;
- image/render version;
- prompt/schema version;
- decoding settings;
- raw output;
- parsed output;
- timestamp and RID.

## 3. Review / normalize

Teacher outputs may be inconsistent. A production dataset should normalize labels and preserve invalid/ambiguous cases rather than silently rewriting them.

Possible workflows:

- automatic schema validation;
- majority consensus between multiple teachers;
- deterministic sanity checks;
- human review of disagreements;
- discard only under explicit documented rules.

## 4. Train a smaller student

The student does not need to generate prose.

Possible student inputs:

- numerical state only;
- numerical state + compact sequence;
- image embeddings;
- chart images;
- typed state fields;
- combinations of the above.

Possible student outputs are the teacher's compact labels.

Students can range from gradient boosting and MLPs to compact VLMs or small language models.

## 5. Compare teacher and student

Use a validation split that was not used for student training.

Report at minimum:

- overall and per-class accuracy/F1;
- confusion matrix;
- teacher/student disagreement count;
- inference time;
- RAM/VRAM;
- model size;
- batch size;
- hardware.

Do not promote a student only because it is faster.

## 6. Keep the teacher as fallback

A practical hybrid system can use the Mini AI for common cases and call the larger teacher only when the student reports uncertainty or an out-of-distribution state.

```text
new market state
      |
      v
Mini AI
  |        |
confident  uncertain
  |        |
  v        v
result   large teacher
            |
            v
       richer review
```

This architecture can reduce compute cost while retaining access to a more capable model on difficult cases.

## 7. Feed hard cases back into training

Disagreements are valuable data.

A later training round can focus on:

- student errors;
- low-confidence examples;
- teacher disagreement;
- new instruments/timeframes;
- new market regimes.

This creates an iterative loop where the small model becomes more capable without requiring the large teacher on every runtime decision.
