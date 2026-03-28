# Prompt Engineering Evaluation

Evaluation of 3 prompt versions on the 3 worst-performing baseline documents.

## Test Documents

- **Doc-01**: Invoice with prose preamble + markdown fence + string floats (Ironbridge Engineering)
- **Doc-09**: Invoice with prose preamble + wrong key names (BlueSky Drone Services)
- **Doc-13**: Invoice with pure prose response, no JSON (Pinnacle Event Management)

---

## Results Table

| Prompt Version | Doc | is_valid_json | has_all_required_keys | key_accuracy | value_accuracy | Notes |
|---|---|---|---|---|---|---|
| V1: Basic | Doc-01 | False | False | 0.0 | 0.0 | Still wraps in prose + fence |
| V1: Basic | Doc-09 | False | False | 0.0 | 0.0 | Prose preamble; wrong keys (Vendor, Invoice Number) |
| V1: Basic | Doc-13 | False | False | 0.0 | 0.0 | Pure prose paragraph response |
| V2: Format-Constrained | Doc-01 | True | True | 1.0 | 0.7 | No fence or prose; dates still not ISO (15/09/2024) |
| V2: Format-Constrained | Doc-09 | True | False | 0.56 | 0.4 | No prose; wrong keys persist (Vendor/Invoice Number) |
| V2: Format-Constrained | Doc-13 | True | True | 1.0 | 0.9 | Clean JSON; dates correctly parsed from DD/MM/YYYY |
| V3: Few-Shot | Doc-01 | True | True | 1.0 | 0.9 | Bare JSON; date still DD/MM not ISO |
| V3: Few-Shot | Doc-09 | True | True | 1.0 | 1.0 | Keys now correct following example; ISO date |
| V3: Few-Shot | Doc-13 | True | True | 1.0 | 1.0 | Perfect; followed example format precisely |

---

## Parse Success Rate: Prompt Engineering vs Fine-Tuning

| Approach | Parse Success Rate (3 worst docs) |
|----------|----------------------------------|
| V1 Basic prompt | 0 / 3 = 0% |
| V2 Format-constrained | 2 / 3 = 67% |
| V3 Few-shot | 3 / 3 = 100% |
| Fine-tuned model (same docs) | 3 / 3 = 100% |

---

## Key Observations

**Prompt V2 vs V3**: Explicit format rules (V2) eliminated fence and prose preamble but could not fix key naming errors. The model continued to use human-readable labels ("Invoice Number") despite being told to use schema keys. Only the few-shot example (V3) provided a concrete pattern to imitate, fixing key names.

**Prompt engineering ceiling**: V3 achieves 100% on these 3 documents, matching the fine-tuned model. However, V3 uses a long prompt (~250 tokens overhead per call) and the example only covers the invoice type. A PO document would require a separate PO example prompt, doubling overhead. At scale, this increases inference cost significantly.

**Fine-tuning advantage**: The fine-tuned model achieves equivalent accuracy with a 15-token instruction ("Extract all invoice fields...") regardless of document type, with zero per-call prompt engineering overhead and consistent performance across all 20 evaluation documents including types not demonstrated in any prompt.
