# Failure Analysis: failure_02

## Source Document

```
INVOICE
Vendor:       Blue Ridge Photography Studio
Invoice No:   BR-2024-07-C
Date:         July 14, 2024
Due Date:     Not stated
Currency:     USD
Services Rendered:
  Product Photography Session         Qty:   1  @  2200.00
  Image Retouching per image          Qty:  30  @    45.00
  Rush Delivery Surcharge             Qty:   1  @   300.00
Sub-Total Before Tax:  USD 3850.00
No Applicable Tax
Total Payable:         USD 3850.00
```

## Expected JSON Output

```json
{"vendor":"Blue Ridge Photography Studio","invoice_number":"BR-2024-07-C","date":"2024-07-14","due_date":null,"currency":"USD","subtotal":3850.00,"tax":null,"total":3850.00,"line_items":[{"description":"Product Photography Session","quantity":1,"unit_price":2200.00},{"description":"Image Retouching per image","quantity":30,"unit_price":45.00},{"description":"Rush Delivery Surcharge","quantity":1,"unit_price":300.00}]}
```

## Model Actual Output

```json
{"vendor":"Blue Ridge Photography Studio","invoice_number":"BR-2024-07-C","date":"2024-07-14","due_date":null,"currency":"USD","subtotal":3850.00,"tax":0.0,"total":3850.00,"line_items":[{"description":"Product Photography Session","quantity":1,"unit_price":2200.00},{"description":"Image Retouching per image","quantity":30,"unit_price":45.00},{"description":"Rush Delivery Surcharge","quantity":1,"unit_price":300.00}]}
```

## What Went Wrong

Value type mismatch on `tax` field. The model outputs `"tax": 0.0` instead of `"tax": null`. The document says "No Applicable Tax" which semantically means tax is not applicable -- the correct schema representation is `null`, not `0.0`. The JSON is parseable and all keys are present, but `value_accuracy` drops because this is a hallucinated value (`0.0` implies tax was computed and equals zero, which is meaningfully different from "not applicable").

## Why It Likely Failed

The training data distinction between `tax: null` (field not applicable) and `tax: 0.0` (explicitly zero-rated) is subtle. The phrase "No Applicable Tax" is slightly different from "N/A" or "Not stated" -- the model defaulted to a numeric zero rather than recognizing this as an absent-field case. There are likely insufficient examples with the exact phrasing "No Applicable Tax" in the training set.

## Training Data Fix That Would Help

Add 5 invoice examples where "No Applicable Tax", "Tax Exempt", "Zero Rated", and "Tax: -" all map to `"tax": null` in the output. The model needs to learn that any of these phrasings signals absence, not zero value. Expanding the linguistic variation of the "no tax" signal in training data directly targets this failure mode.
