# Failure Analysis: failure_01

## Source Document

```
INVOICE
Vendor:       Summit Software Consultants
Invoice No:   SSC-2024-ALPHA
Date:         Nov 30, 2024
Due Date:     Dec 30, 2024
Currency:     USD
Line Items:
  Discovery Workshop 2 days          Qty:   2  @  8000.00
  Technical Architecture Design      Qty:   1  @  12000.00
  API Development 80 hours           Qty:  80  @   175.00
Total Due:    USD 34000.00
```

## Expected JSON Output

```json
{"vendor":"Summit Software Consultants","invoice_number":"SSC-2024-ALPHA","date":"2024-11-30","due_date":"2024-12-30","currency":"USD","subtotal":34000.00,"tax":null,"total":34000.00,"line_items":[{"description":"Discovery Workshop 2 days","quantity":2,"unit_price":8000.00},{"description":"Technical Architecture Design","quantity":1,"unit_price":12000.00},{"description":"API Development 80 hours","quantity":80,"unit_price":175.00}]}
```

## Model Actual Output

```json
{"vendor":"Summit Software Consultants","invoice_number":"SSC-2024-ALPHA","date":"2024-11-30","due_date":"2024-12-30","currency":"USD","subtotal":34000.00,"tax":null,"total":34000.00,"line_items":[{"description":"Discovery Workshop 2 days","quantity":2,"unit_price":8000.00},{"description":"Technical Architecture Design","quantity":1,"unit_price":12000.00},{"description":"API Development 80 hours","quantity":80,"unit_price":175.00}]}
```

> Note: After fine-tuning, this doc now passes. Original base model failure was pure prose response.

## What Went Wrong (Baseline)

The base model returned a multi-sentence prose explanation instead of JSON. It described the invoice in natural language without producing a parseable object.

## Why It Likely Failed

The document uses unconventional date formatting ("Nov 30, 2024") and has no explicit "Subtotal" line. The base model, lacking fine-tuning on structured output, fell back to its default conversational behavior when faced with an ambiguous format.

## Training Data Fix That Would Help

Add 5-10 examples where dates appear in long-form English ("November 30, 2024", "30 Nov 2024") and the model must normalize to YYYY-MM-DD. Also add examples where subtotal is absent and must be inferred from line item arithmetic.
