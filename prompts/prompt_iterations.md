# Prompt Engineering Iterations

Three prompt versions tested on the 3 worst-performing baseline documents: Doc-01 (prose + fence), Doc-09 (prose + wrong keys), Doc-13 (pure prose).

---

## Version 1: Basic Instruction Prompt

```
You are a data extraction assistant. Extract all fields from the document below and return only valid JSON.

Document:
{document_text}
```

**Rationale**: Minimal prompt. Tests the base model's default behaviour with minimal guidance.

**Results**: See prompt_eval.md

---

## Version 2: Format-Constrained Prompt

```
You are a precise data extraction API. Your output must be a single valid JSON object and nothing else.

Rules:
- Do NOT include markdown code fences (no backticks).
- Do NOT include any explanation, preamble, or commentary.
- Do NOT include text before or after the JSON object.
- Use only these keys for invoices: vendor, invoice_number, date, due_date, currency, subtotal, tax, total, line_items.
- Dates must be formatted as YYYY-MM-DD.
- Monetary values must be JSON numbers (floats), not strings.
- Fields not present in the document must be set to null, not omitted.

Document:
{document_text}

JSON output:
```

**Rationale**: Explicit prohibition of each observed failure mode (fence, preamble, wrong keys, string floats, non-ISO dates). The trailing "JSON output:" cue nudges the model to continue directly with JSON.

**Results**: See prompt_eval.md

---

## Version 3: Few-Shot Constrained Prompt

```
You are a structured data extraction API. For each document, return ONLY a valid JSON object with the exact keys listed.

Example input:
INVOICE
Vendor: Apex Office Ltd
Invoice No: INV-001
Date: 15/06/2024
Due Date: 15/07/2024
Currency: USD
Line Items:
  A4 Paper Ream    Qty: 10  @  12.00
Subtotal: USD 120.00
Tax: USD 9.60
Total: USD 129.60

Example output:
{"vendor":"Apex Office Ltd","invoice_number":"INV-001","date":"2024-06-15","due_date":"2024-07-15","currency":"USD","subtotal":120.00,"tax":9.60,"total":129.60,"line_items":[{"description":"A4 Paper Ream","quantity":10,"unit_price":12.00}]}

Now extract from this document:
{document_text}
```

**Rationale**: One-shot example demonstrates the exact format expected: no fences, bare JSON, ISO dates, float values, correct key names. The example is intentionally simple so it does not crowd the context window. Provides both positive instruction and a concrete template to imitate.

**Results**: See prompt_eval.md
