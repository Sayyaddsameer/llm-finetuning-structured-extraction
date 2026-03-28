# Failure Analysis: failure_03

## Source Document

```
PURCHASE ORDER
Issued By:    Henderson & Partners Architecture
To Supplier:  Berlin CAD Software GmbH
Reference:    H-P-2024-SW-0039
Issue Date:   2024-08-20
Expected by:  2024-09-05
Currency:     EUR
Item Details:
  AutoCAD Architecture 2025 Licence     Qty:  12  @  1299.00
  Revit BIM Subscription Annual         Qty:   8  @  1899.00
  3ds Max Subscription Annual           Qty:   4  @  1599.00
Grand Total:  EUR 33964.00
```

## Expected JSON Output

```json
{"buyer":"Henderson & Partners Architecture","supplier":"Berlin CAD Software GmbH","po_number":"H-P-2024-SW-0039","date":"2024-08-20","delivery_date":"2024-09-05","currency":"EUR","total":33964.00,"items":[{"item_name":"AutoCAD Architecture 2025 Licence","quantity":12,"unit_price":1299.00},{"item_name":"Revit BIM Subscription Annual","quantity":8,"unit_price":1899.00},{"item_name":"3ds Max Subscription Annual","quantity":4,"unit_price":1599.00}]}
```

## Model Actual Output

```json
{"buyer":"Henderson & Partners Architecture","supplier":"Berlin CAD Software GmbH","po_number":"H-P-2024-SW-0039","date":"2024-08-20","delivery_date":"2024-09-05","currency":"EUR","total":33964.00,"order_items":[{"item_name":"AutoCAD Architecture 2025 Licence","quantity":12,"unit_price":1299.00},{"item_name":"Revit BIM Subscription Annual","quantity":8,"unit_price":1899.00},{"item_name":"3ds Max Subscription Annual","quantity":4,"unit_price":1599.00}]}
```

## What Went Wrong

Key name error: the model outputs `"order_items"` instead of the schema-required `"items"`. All values are correct; only the key name is wrong. This causes `has_all_required_keys` to fail and makes the pipeline unable to extract the items array without custom remapping logic.

## Why It Likely Failed

The source document uses the header "Item Details:" rather than "Ordered Items:" -- which is the phrasing used consistently in the training data's PO raw text templates. The model associated "Item Details" with the label "order_items" (a partial hallucination of a plausible alternative). The training set's PO documents uniformly use the template label "Ordered Items" as the section header, so the model lacks examples for other section header phrasings that should still map to `"items"`.

## Training Data Fix That Would Help

Add 5-8 PO training examples with varying section header phrasings: "Item Details:", "Goods Ordered:", "Products Requested:", "Line Items:", "Procurement Details:" -- all mapping to `"items"` in the output. This teaches the model that the key name is schema-defined, not derived from the document's section header label.
