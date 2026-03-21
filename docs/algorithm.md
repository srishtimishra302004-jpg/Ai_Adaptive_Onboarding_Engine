# Adaptive Learning Algorithm

## Skill Extraction Logic
- Build known skill inventory from taxonomy categories.
- Normalize incoming text:
  - lowercase
  - apply synonym replacements
- Detect skills by pattern matching against normalized text.
- Infer level by evidence phrases:
  - `advanced`: optimized, architected, scaled, led
  - `intermediate`: built, developed, implemented, deployed
  - `beginner`: familiar with, basics of

## Gap Analysis Logic
- Compute `required - user` as missing skills.
- Compute under-level skills where user level < required level.
- Compute resume score:
  - `(exact_overlap + semantic_overlap) / required_count * 100`
- Compute semantic similarity between full skill sets using embeddings.

## Adaptive Path Logic
- Represent dependencies in a lightweight directed graph.
- Topologically order missing skills so prerequisites come first.
- Attach resource bundles from dataset by skill + level.
- Add `why` reasoning per step.
- No-gap fallback:
  - generate advanced mastery track from top role-relevant skills.
