# Invoice JSON Schema

This document defines the canonical JSON output schema that all invoice extraction models must produce. Every training example, evaluation sample, and model response must conform exactly to this schema.

---

## Schema Definition

```json
{
  "vendor": "string",
  "invoice_number": "string",
  "date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD or null",
  "currency": "string (3-letter ISO 4217)",
  "subtotal": "float",
  "tax": "float or null",
  "total": "float",
  "line_items": [
    {
      "description": "string",
      "quantity": "integer",
      "unit_price": "float"
    }
  ]
}
```

---

## Field Specifications

| Key | Type | Format | Absent Field Handling |
|-----|------|--------|-----------------------|
| `vendor` | string | Full legal or trade name of the issuing company | Use `""` (empty string) if completely illegible |
| `invoice_number` | string | As printed on the document, including any prefix letters | Use `""` if not present |
| `date` | string | ISO 8601: `YYYY-MM-DD` | Use `""` if not found |
| `due_date` | string or null | ISO 8601: `YYYY-MM-DD`; null if no due date is stated | `null` |
| `currency` | string | 3-letter ISO 4217 code (e.g., `USD`, `GBP`, `EUR`, `INR`, `JPY`) | `"USD"` if ambiguous |
| `subtotal` | float | Amount before tax, as a decimal number | `0.0` if not itemised |
| `tax` | float or null | Tax amount in the document currency; null if not stated | `null` |
| `total` | float | Final payable amount inclusive of tax and fees | Must always be present |
| `line_items` | array | List of item objects; at minimum one element | `[]` if no items listed |

### line_items object

| Key | Type | Format | Absent Field Handling |
|-----|------|--------|-----------------------|
| `description` | string | Free text description of the item or service | `""` if blank |
| `quantity` | integer | Whole number count; round to nearest integer if given as decimal | `1` if not stated |
| `unit_price` | float | Price per single unit in the invoice currency | Must always be present |

---

## Rules and Constraints

1. All float values must be true JSON numbers, never quoted strings. `"total": 1500.00` is correct; `"total": "1500.00"` is invalid.
2. Date strings must strictly follow `YYYY-MM-DD`. Never use `DD/MM/YYYY` or `MM-DD-YYYY` in the output.
3. `null` (JSON null) and `""` (empty string) are distinct. Follow the table above exactly.
4. No extra keys beyond those listed above may appear in the output.
5. The output must be a single, bare JSON object. No markdown fences, no prose, no comments.
6. `total` must always be a non-null float. If the document is ambiguous, use the largest monetary amount visible.

---

## Example Compliant Output

```json
{
  "vendor": "Apex Office Supplies Ltd",
  "invoice_number": "INV-2024-00341",
  "date": "2024-06-12",
  "due_date": "2024-07-12",
  "currency": "USD",
  "subtotal": 840.00,
  "tax": 67.20,
  "total": 907.20,
  "line_items": [
    {"description": "A4 Paper Ream 500 sheets", "quantity": 20, "unit_price": 12.00},
    {"description": "Ballpoint Pens Box of 50", "quantity": 10, "unit_price": 24.00},
    {"description": "Stapler Heavy Duty", "quantity": 5, "unit_price": 36.00}
  ]
}
```
