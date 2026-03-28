# Evaluation Summary

## Baseline Parse Success Rate

**Parse Success Rate (base model, no fine-tuning): 7 / 20 = 35%**

A response counts as a "parse success" if and only if:
1. `json.loads()` succeeds without error, AND
2. All required schema keys are present in the parsed object.

---

## Baseline Metric Breakdown

| Metric | Value |
|--------|-------|
| Total evaluation documents | 20 |
| Valid JSON responses | 10 |
| Has all required keys (of valid JSON) | 7 |
| **Parse success rate** | **35%** |
| Avg key_accuracy (all 20 docs) | 0.478 |
| Avg value_accuracy (all 20 docs) | 0.362 |
| Responses with markdown code fences | 4 |
| Responses with prose preamble | 7 |
| Responses with wrong key names | 3 |
| Responses with non-ISO date format | 8 |
| Responses with string floats instead of numbers | 3 |

---

## Key Failure Modes Observed

1. **Prose preamble (7/20)**: The model prefixes JSON with sentences like "Here is the extracted data..." or "Based on the invoice provided...". This makes `json.loads()` fail on the full response string.
2. **Markdown code fences (4/20)**: Output wrapped in ` ```json ` and ` ``` ` blocks. Parseable only after stripping fences.
3. **Wrong key names (3/20)**: Model uses keys like `invoice_no`, `desc`, `qty`, `price`, `Line Items` instead of schema-required names.
4. **Non-ISO date format (8/20)**: Model copies dates as-printed (`15/09/2024`, `01-10-2024`, `Nov 30, 2024`) rather than normalizing to `YYYY-MM-DD`.
5. **String floats (3/20)**: Monetary values quoted as strings (`"subtotal": "39400.00"`) instead of JSON numbers.

---

## Post Fine-Tuning Parse Success Rate

**Parse Success Rate (fine-tuned model): 18 / 20 = 90%**

See `before_vs_after.md` for full comparison table.
