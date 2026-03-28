# Failure Analysis: failure_04

## Source Document

```
INVOICE
Vendor:       Hanover Precision GmbH
Rechnungsnummer: HP-2024-DE-1188
Rechnungsdatum:  15.11.2024
Faelligkeitsdatum: 15.12.2024
Waehrung: EUR
Positionen:
  Praezisionsdrehteile M6 x 20mm  Menge: 5000  Einzelpreis:  0,85
  Gewindeschneidwerkzeug M6 HSS   Menge:   40  Einzelpreis: 42,00
  CNC Fraeser 6mm VHM             Menge:   80  Einzelpreis: 28,50
Nettobetrag: EUR 4850,00
Mehrwertsteuer 19%: EUR 921,50
Bruttobetrag: EUR 5771,50
```

## Expected JSON Output

```json
{"vendor":"Hanover Precision GmbH","invoice_number":"HP-2024-DE-1188","date":"2024-11-15","due_date":"2024-12-15","currency":"EUR","subtotal":4850.00,"tax":921.50,"total":5771.50,"line_items":[{"description":"Praezisionsdrehteile M6 x 20mm","quantity":5000,"unit_price":0.85},{"description":"Gewindeschneidwerkzeug M6 HSS","quantity":40,"unit_price":42.00},{"description":"CNC Fraeser 6mm VHM","quantity":80,"unit_price":28.50}]}
```

## Model Actual Output

```json
{"vendor":"Hanover Precision GmbH","invoice_number":"HP-2024-DE-1188","date":"15.11.2024","due_date":"15.12.2024","currency":"EUR","subtotal":"4850,00","tax":"921,50","total":"5771,50","line_items":[{"description":"Praezisionsdrehteile M6 x 20mm","quantity":5000,"unit_price":"0,85"},{"description":"Gewindeschneidwerkzeug M6 HSS","quantity":40,"unit_price":"42,00"},{"description":"CNC Fraeser 6mm VHM","quantity":80,"unit_price":"28,50"}]}
```

## What Went Wrong

Two distinct failures:
1. **Date format not normalized**: Model copies European dot-separated dates (`15.11.2024`) rather than converting to ISO `2024-11-15`.
2. **Decimal comma not converted to decimal point**: German locale uses comma as decimal separator (`4850,00`). The model copies these as strings (`"4850,00"`) instead of converting to JSON floats (`4850.00`). This makes `json.loads()` succeed (they are valid strings) but downstream `float()` conversion will fail.

## Why It Likely Failed

The training data contains no German-locale documents. All 80 training examples use English-format numbers (decimal point) and ISO or slash/dash date formats. The model has never seen `DD.MM.YYYY` or European decimal comma in training examples, so it lacks the pattern to normalize them. This is a genuine data coverage gap.

## Training Data Fix That Would Help

Add 5-8 invoice examples explicitly sourced from or modelled on German/European documents: dates as `DD.MM.YYYY` normalized to `YYYY-MM-DD`, amounts with decimal commas converted to decimal points, field labels in German (Rechnungsnummer, Nettobetrag, etc.) mapped to the English schema keys. This is the most impactful targeted addition: one training batch covering European locale formatting would fix both failure modes simultaneously.
