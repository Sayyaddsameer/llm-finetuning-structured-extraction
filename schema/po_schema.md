# Purchase Order JSON Schema

This document defines the canonical JSON output schema for purchase order extraction. Every training example, evaluation sample, and model response must conform exactly to this schema.

---

## Schema Definition

```json
{
  "buyer": "string",
  "supplier": "string",
  "po_number": "string",
  "date": "YYYY-MM-DD",
  "delivery_date": "YYYY-MM-DD or null",
  "currency": "string (3-letter ISO 4217)",
  "total": "float",
  "items": [
    {
      "item_name": "string",
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
| `buyer` | string | Full legal or trade name of the company issuing the PO | Use `""` if not found |
| `supplier` | string | Full name of the company receiving the PO | Use `""` if not found |
| `po_number` | string | As printed on the document, including any prefix | Use `""` if not present |
| `date` | string | ISO 8601: `YYYY-MM-DD` (PO issuance date) | Use `""` if not found |
| `delivery_date` | string or null | ISO 8601: expected delivery date; null if not stated | `null` |
| `currency` | string | 3-letter ISO 4217 code (e.g., `USD`, `EUR`, `GBP`, `INR`) | `"USD"` if ambiguous |
| `total` | float | Sum of all item totals; final order value | Must always be present |
| `items` | array | List of ordered item objects; at minimum one element | `[]` if no items listed |

### items object

| Key | Type | Format | Absent Field Handling |
|-----|------|--------|-----------------------|
| `item_name` | string | Name or part number of the ordered item | `""` if blank |
| `quantity` | integer | Count of units ordered; round decimals to nearest integer | `1` if not stated |
| `unit_price` | float | Price per single unit in PO currency | Must always be present |

---

## Rules and Constraints

1. All float values must be true JSON numbers, never quoted strings. `"total": 5000.00` is correct; `"total": "5,000.00"` is invalid.
2. Date strings must strictly follow `YYYY-MM-DD`. Strip slashes, dots, and reformat as needed.
3. `null` (JSON null) and `""` (empty string) are distinct. Follow the table above exactly.
4. No extra keys beyond those listed above may appear in the output.
5. The output must be a single, bare JSON object. No markdown fences, no prose preamble.
6. `total` must always be a non-null float. Compute from line items if a summary is not printed.

---

## Example Compliant Output

```json
{
  "buyer": "GlobalTech Manufacturing Inc",
  "supplier": "Precision Parts Co",
  "po_number": "PO-2024-8821",
  "date": "2024-08-01",
  "delivery_date": "2024-08-22",
  "currency": "USD",
  "total": 14750.00,
  "items": [
    {"item_name": "Steel Bracket Type-A", "quantity": 500, "unit_price": 12.50},
    {"item_name": "Hex Bolt M8 x 30mm", "quantity": 2000, "unit_price": 0.85},
    {"item_name": "Rubber Gasket 50mm", "quantity": 300, "unit_price": 7.00}
  ]
}
```
