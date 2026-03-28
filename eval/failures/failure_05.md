# Failure Analysis: failure_05

## Source Document

```
PURCHASE ORDER
Buyer:        Quantum Logistics Ltd
Supplier:     Atlas Freight Solutions
PO Number:    QL-2024-FRT-0088
Date:         2024-10-12
Requested Delivery: 2024-10-28
Currency:     USD

CONSOLIDATED SHIPMENT DETAILS
The following items are requested for the Q4 replenishment run as discussed in meeting ref MTG-2024-09-30. All items subject to vendor quality certification per ISO 9001.

  Industrial Packing Tape 48mm x 66m roll   Qty:  500  @    3.20
  Bubble Wrap Roll 1.5m x 50m               Qty:  100  @   18.50
  Wooden Pallet EUR Standard 1200x800mm     Qty:  200  @   14.00
  Stretch Film 20mu 500mm x 300m            Qty:  150  @    9.80

All prices are exclusive of freight surcharges. A fuel adjustment of USD 480.00 will be added to the final invoice separately.

Order Total:  USD 13945.00
```

## Expected JSON Output

```json
{"buyer":"Quantum Logistics Ltd","supplier":"Atlas Freight Solutions","po_number":"QL-2024-FRT-0088","date":"2024-10-12","delivery_date":"2024-10-28","currency":"USD","total":13945.00,"items":[{"item_name":"Industrial Packing Tape 48mm x 66m roll","quantity":500,"unit_price":3.20},{"item_name":"Bubble Wrap Roll 1.5m x 50m","quantity":100,"unit_price":18.50},{"item_name":"Wooden Pallet EUR Standard 1200x800mm","quantity":200,"unit_price":14.00},{"item_name":"Stretch Film 20mu 500mm x 300m","quantity":150,"unit_price":9.80}]}
```

## Model Actual Output

```json
{"buyer":"Quantum Logistics Ltd","supplier":"Atlas Freight Solutions","po_number":"QL-2024-FRT-0088","date":"2024-10-12","delivery_date":"2024-10-28","currency":"USD","total":14425.00,"items":[{"item_name":"Industrial Packing Tape 48mm x 66m roll","quantity":500,"unit_price":3.20},{"item_name":"Bubble Wrap Roll 1.5m x 50m","quantity":100,"unit_price":18.50},{"item_name":"Wooden Pallet EUR Standard 1200x800mm","quantity":200,"unit_price":14.00},{"item_name":"Stretch Film 20mu 500mm x 300m","quantity":150,"unit_price":9.80},{"item_name":"Fuel Adjustment Surcharge","quantity":1,"unit_price":480.00}]}
```

## What Went Wrong

**Hallucination of an additional line item.** The model adds `"Fuel Adjustment Surcharge"` as a fifth item with `unit_price: 480.00`, which does not exist in the ordered items section. It is mentioned in prose as a future addition to a separate invoice. This inflates the total from `13945.00` to `14425.00`. The JSON is parseable, all required keys are present, and structure is correct -- but the extraction is factually wrong.

## Why It Likely Failed

The training data contains no examples with embedded narrative prose that references monetary amounts which are NOT line items. Every monetary figure in the 80 training examples appears in a line items table and belongs in the output. The model has learned "if there is a monetary amount with a description, it is a line item" without learning the more nuanced distinction between ordered items and referenced future charges. This is precisely the hallucination risk in extraction contexts.

## Training Data Fix That Would Help

Add 4-5 PO or invoice examples that contain non-item monetary references in prose (e.g., "A shipping surcharge will be billed separately", "Late payment fees may apply per contract clause 4.2", "Discount of $200 reflected in total"). The correct outputs for these examples should NOT include those amounts as line items. This teaches the model that only items in the structured items table belong in the `items` array, while prose mentions are ignored.
