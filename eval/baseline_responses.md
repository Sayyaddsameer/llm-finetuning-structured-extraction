# Baseline Evaluation Responses

Raw verbatim model outputs from **Llama-3.2-3B-Instruct (base, no fine-tuning)** on 20 held-out documents. Prompt used for all 20 evaluations:

```
You are a data extraction assistant. Extract all fields from the document below and return ONLY a valid JSON object. Do not include markdown code fences, explanations, or any text other than the JSON object itself.

Document:
{document_text}
```

---

## Doc-01 (Invoice / USD / multi-item)

**Input:**
```
INVOICE
Vendor:       Ironbridge Engineering Ltd
Invoice No:   IB-2024-0501
Date:         15/09/2024
Due Date:     15/10/2024
Currency:     USD
Line Items:
  Structural Steel Beam 200x100x6m    Qty:  50  @   420.00
  Concrete Anchor Bolt M20 Box/50     Qty: 100  @    48.00
  Site Labour 8hr Day                 Qty:  20  @ 480.00
Subtotal:     USD 39400.00
Tax:          USD 3152.00
Total Due:    USD 42552.00
```

**Raw Model Output:**
```
Here is the extracted data from the invoice:

```json
{
  "vendor": "Ironbridge Engineering Ltd",
  "invoice_number": "IB-2024-0501",
  "date": "15/09/2024",
  "due_date": "15/10/2024",
  "currency": "USD",
  "subtotal": "39400.00",
  "tax": "3152.00",
  "total": "42552.00",
  "line_items": [
    {"description": "Structural Steel Beam 200x100x6m", "quantity": 50, "unit_price": "420.00"},
    {"description": "Concrete Anchor Bolt M20 Box/50", "quantity": 100, "unit_price": "48.00"},
    {"description": "Site Labour 8hr Day", "quantity": 20, "unit_price": "480.00"}
  ]
}
```
```

---

## Doc-02 (Invoice / EUR / null tax)

**Input:**
```
INVOICE
Vendor:       Versailles Garden Design
Invoice No:   VGD-2024-0088
Date:         03-10-2024
Due Date:     Not specified
Currency:     EUR
Line Items:
  Garden Design Consultation         Qty:   1  @  3500.00
  Planting Scheme Full Layout        Qty:   1  @  2800.00
Subtotal:     EUR 6300.00
Tax:          N/A
Total Due:    EUR 6300.00
```

**Raw Model Output:**
```
{
  "vendor": "Versailles Garden Design",
  "invoice_number": "VGD-2024-0088",
  "date": "03-10-2024",
  "due_date": null,
  "currency": "EUR",
  "subtotal": 6300.00,
  "tax": null,
  "total": 6300.00,
  "line_items": [
    {"description": "Garden Design Consultation", "quantity": 1, "unit_price": 3500.00},
    {"description": "Planting Scheme Full Layout", "quantity": 1, "unit_price": 2800.00}
  ]
}
```

---

## Doc-03 (PO / USD / delivery present)

**Input:**
```
PURCHASE ORDER
Buyer:        Redwood Supermarkets Corp
Supplier:     FreshFields Wholesale
PO Number:    RSC-PO-2024-0812
Date:         2024-07-01
Requested Delivery: 2024-07-18
Currency:     USD
Ordered Items:
  Organic Whole Milk 2L              Qty: 1000  @     1.80
  Free Range Eggs 12-pack            Qty:  500  @     3.60
  Sourdough Bread 800g               Qty:  400  @     2.80
Order Total:  USD 5420.00
```

**Raw Model Output:**
```
I've extracted the purchase order details:

{
  "buyer": "Redwood Supermarkets Corp",
  "supplier": "FreshFields Wholesale",
  "po_number": "RSC-PO-2024-0812",
  "date": "2024-07-01",
  "delivery_date": "2024-07-18",
  "currency": "USD",
  "total": 5420.0,
  "items": [
    {"item_name": "Organic Whole Milk 2L", "quantity": 1000, "unit_price": 1.80},
    {"item_name": "Free Range Eggs 12-pack", "quantity": 500, "unit_price": 3.60},
    {"item_name": "Sourdough Bread 800g", "quantity": 400, "unit_price": 2.80}
  ]
}
```

---

## Doc-04 (Invoice / GBP / single item / null due_date)

**Input:**
```
INVOICE
Vendor:       Camden Photography Studio
Invoice No:   CPS-0044
Date:         22/08/2024
Due Date:     Not stated
Currency:     GBP
Line Items:
  Corporate Headshots Session Full Day   Qty:   1  @  1800.00
Subtotal:     GBP 1800.00
Tax:          N/A
Total Due:    GBP 1800.00
```

**Raw Model Output:**
```
{"vendor":"Camden Photography Studio","invoice_no":"CPS-0044","date":"22/08/2024","currency":"GBP","subtotal":1800.00,"tax":null,"total":1800.00,"items":[{"desc":"Corporate Headshots Session Full Day","qty":1,"price":1800.00}]}
```

---

## Doc-05 (Invoice / INR / multi-item / tax present)

**Input:**
```
INVOICE
Vendor:       Sunrise Auto Components
Invoice No:   SAC/2024/0441
Date:         10-11-2024
Due Date:     10-12-2024
Currency:     INR
Line Items:
  Brake Disc Rotor Front 280mm  Qty: 200  @  1100.00
  Disc Pad Set Ceramic          Qty: 200  @   480.00
  Shock Absorber Front Pair     Qty: 100  @  1850.00
Subtotal:     INR 558000.00
Tax:          INR 100440.00
Total Due:    INR 658440.00
```

**Raw Model Output:**
```
Here is the data extracted from the invoice in JSON format:

```json
{
  "vendor": "Sunrise Auto Components",
  "invoice_number": "SAC/2024/0441",
  "date": "10-11-2024",
  "due_date": "10-12-2024",
  "currency": "INR",
  "subtotal": 558000,
  "tax": 100440,
  "total": 658440,
  "line_items": [
    {
      "description": "Brake Disc Rotor Front 280mm",
      "quantity": 200,
      "unit_price": 1100
    },
    {
      "description": "Disc Pad Set Ceramic",
      "quantity": 200,
      "unit_price": 480
    },
    {
      "description": "Shock Absorber Front Pair",
      "quantity": 100,
      "unit_price": 1850
    }
  ]
}
```
```

---

## Doc-06 (PO / GBP / null delivery / single item)

**Input:**
```
PURCHASE ORDER
Buyer:        Ashford Records Label
Supplier:     Disc Manufacturing UK
PO Number:    ARL-PO-2024-0011
Date:         2024-05-30
Requested Delivery: TBD
Currency:     GBP
Ordered Items:
  Vinyl Record 180g Black 12 inch     Qty: 2000  @    4.50
Order Total:  GBP 9000.00
```

**Raw Model Output:**
```
{
  "buyer": "Ashford Records Label",
  "supplier": "Disc Manufacturing UK",
  "po_number": "ARL-PO-2024-0011",
  "date": "2024-05-30",
  "delivery_date": null,
  "currency": "GBP",
  "total": 9000.0,
  "items": [
    {
      "item_name": "Vinyl Record 180g Black 12 inch",
      "quantity": 2000,
      "unit_price": 4.50
    }
  ]
}
```

---

## Doc-07 (Invoice / EUR / many items)

**Input:**
```
INVOICE
Vendor:       Alpine Sports GmbH
Invoice No:   AS-2024-4411
Date:         2024-09-01
Due Date:     2024-10-01
Currency:     EUR
Line Items:
  Ski Boot Atomic Hawx 130   Qty:  30  @  380.00
  Ski Pole Pair Leki 120cm   Qty:  30  @   85.00
  Ski Helmet Smith Quantum   Qty:  25  @  210.00
  Ski Goggles Oakley Flight  Qty:  25  @  145.00
Subtotal:     EUR 25125.00
Tax:          EUR 4773.75
Total Due:    EUR 29898.75
```

**Raw Model Output:**
```
Sure! Here are the extracted fields:

{
  "vendor": "Alpine Sports GmbH",
  "invoice_number": "AS-2024-4411",
  "date": "2024-09-01",
  "due_date": "2024-10-01",
  "currency": "EUR",
  "subtotal": 25125.00,
  "tax": 4773.75,
  "total": 29898.75,
  "line_items": [
    {"description": "Ski Boot Atomic Hawx 130", "quantity": 30, "unit_price": 380.00},
    {"description": "Ski Pole Pair Leki 120cm", "quantity": 30, "unit_price": 85.00},
    {"description": "Ski Helmet Smith Quantum", "quantity": 25, "unit_price": 210.00},
    {"description": "Ski Goggles Oakley Flight", "quantity": 25, "unit_price": 145.00}
  ]
}
```

---

## Doc-08 (PO / INR / multi-item / delivery present)

**Input:**
```
PURCHASE ORDER
Buyer:        Maharashtra State Road Dept
Supplier:     Tata BlueScope Steel
PO Number:    MSRD/PO/2024/0412
Date:         2024-04-01
Requested Delivery: 2024-06-01
Currency:     INR
Ordered Items:
  Guardrail W-Beam 4.3m Hot Dip Galv  Qty: 2000  @   1800.00
  Post Sigma 1.8m Hot Dip Galv        Qty: 4000  @    320.00
  End Terminal Assembly                Qty:  100  @   6500.00
Order Total:  INR 5530000.00
```

**Raw Model Output:**
```
{
  "buyer": "Maharashtra State Road Dept",
  "supplier": "Tata BlueScope Steel",
  "po_number": "MSRD/PO/2024/0412",
  "date": "2024-04-01",
  "delivery_date": "2024-06-01",
  "currency": "INR",
  "total": 5530000.0,
  "items": [
    {"item_name": "Guardrail W-Beam 4.3m Hot Dip Galv", "quantity": 2000, "unit_price": 1800.00},
    {"item_name": "Post Sigma 1.8m Hot Dip Galv", "quantity": 4000, "unit_price": 320.00},
    {"item_name": "End Terminal Assembly", "quantity": 100, "unit_price": 6500.00}
  ]
}
```

---

## Doc-09 (Invoice / USD / null tax / null due_date)

**Input:**
```
INVOICE
Vendor:       BlueSky Drone Services
Invoice No:   BSD-2024-0221
Date:         2024-07-10
Due Date:     Not specified
Currency:     USD
Line Items:
  Aerial Survey 200 Hectares      Qty:   1  @  8500.00
  Orthophoto Processing Report    Qty:   1  @  2200.00
Subtotal:     USD 10700.00
Tax:          N/A
Total Due:    USD 10700.00
```

**Raw Model Output:**
```
I'll extract the invoice fields for you:

```json
{
  "Vendor": "BlueSky Drone Services",
  "Invoice Number": "BSD-2024-0221",
  "Date": "2024-07-10",
  "Due Date": null,
  "Currency": "USD",
  "Subtotal": 10700.00,
  "Tax": null,
  "Total": 10700.00,
  "Line Items": [
    {"Item": "Aerial Survey 200 Hectares", "Quantity": 1, "Unit Price": 10700.00},
    {"Item": "Orthophoto Processing Report", "Quantity": 1, "Unit Price": 2200.00}
  ]
}
```
```

---

## Doc-10 (PO / EUR / no delivery)

**Input:**
```
PURCHASE ORDER
Buyer:        Bordeaux Winery Estate
Supplier:     Verallia Glass Packaging
PO Number:    BWE-PO-2024-0088
Date:         2024-03-10
Requested Delivery: TBD
Currency:     EUR
Ordered Items:
  Bordeaux Bottle 750ml Antique Green   Qty: 50000  @    0.48
  Cork Natural 45x24mm per 1000         Qty:  5000  @   12.00
  Capsule Tin Embossed Gold per 1000    Qty:   500  @   28.00
Order Total:  EUR 98000.00
```

**Raw Model Output:**
```
{
  "buyer": "Bordeaux Winery Estate",
  "supplier": "Verallia Glass Packaging",
  "po_number": "BWE-PO-2024-0088",
  "date": "2024-03-10",
  "delivery_date": null,
  "currency": "EUR",
  "total": 98000.0,
  "items": [
    {"item_name": "Bordeaux Bottle 750ml Antique Green", "quantity": 50000, "unit_price": 0.48},
    {"item_name": "Cork Natural 45x24mm per 1000", "quantity": 5000, "unit_price": 12.00},
    {"item_name": "Capsule Tin Embossed Gold per 1000", "quantity": 500, "unit_price": 28.00}
  ]
}
```

---

## Doc-11 (Invoice / JPY / tax present)

**Input:**
```
INVOICE
Vendor:       Yokohama Electronics Ltd
Invoice No:   YEL-2024-3311
Date:         20/10/2024
Due Date:     20/11/2024
Currency:     JPY
Line Items:
  Power Supply Unit 650W 80+ Gold  Qty: 100  @  12000.00
  CPU Cooler Tower 120mm Fan       Qty:  80  @   8500.00
Subtotal:     JPY 1880000.00
Tax:          JPY 188000.00
Total Due:    JPY 2068000.00
```

**Raw Model Output:**
```
Here's the extracted invoice data:
{
  "vendor": "Yokohama Electronics Ltd",
  "invoice_number": "YEL-2024-3311",
  "date": "20/10/2024",
  "due_date": "20/11/2024",
  "currency": "JPY",
  "subtotal": 1880000,
  "tax": 188000,
  "total": 2068000,
  "line_items": [{"description": "Power Supply Unit 650W 80+ Gold", "quantity": 100, "unit_price": 12000}, {"description": "CPU Cooler Tower 120mm Fan", "quantity": 80, "unit_price": 8500}]
}
```

---

## Doc-12 (PO / USD / 5 items)

**Input:**
```
PURCHASE ORDER
Buyer:        Valley Farm Supply
Supplier:     Agri Pro Chemicals
PO Number:    VFS-PO-2024-1102
Date:         2024-02-20
Requested Delivery: 2024-03-05
Currency:     USD
Ordered Items:
  Roundup Pro 5L can             Qty: 200  @    42.00
  Maxim XL Seed Treatment 5L     Qty: 100  @    68.00
  Urea 46% N 50lb bag            Qty: 500  @    28.00
  Potassium Chloride 50lb bag    Qty: 300  @    22.00
  Irrigation Drip Tape 1000m roll Qty: 20  @   185.00
Order Total:  USD 40500.00
```

**Raw Model Output:**
```
{
  "buyer": "Valley Farm Supply",
  "supplier": "Agri Pro Chemicals",
  "po_number": "VFS-PO-2024-1102",
  "date": "2024-02-20",
  "delivery_date": "2024-03-05",
  "currency": "USD",
  "total": 40500.00,
  "items": [
    {"item_name": "Roundup Pro 5L can", "quantity": 200, "unit_price": 42.00},
    {"item_name": "Maxim XL Seed Treatment 5L", "quantity": 100, "unit_price": 68.00},
    {"item_name": "Urea 46% N 50lb bag", "quantity": 500, "unit_price": 28.00},
    {"item_name": "Potassium Chloride 50lb bag", "quantity": 300, "unit_price": 22.00},
    {"item_name": "Irrigation Drip Tape 1000m roll", "quantity": 20, "unit_price": 185.00}
  ]
}
```

---

## Doc-13 (Invoice / USD / prose-wrapped)

**Input:**
```
INVOICE
Vendor:       Pinnacle Event Management
Invoice No:   PEM-2024-0631
Date:         30/11/2024
Due Date:     30/12/2024
Currency:     USD
Line Items:
  Conference Room Hire Full Day    Qty:   2  @  3200.00
  AV Equipment Package             Qty:   1  @  1800.00
  Catering Lunch 80 pax            Qty:   1  @  4800.00
Subtotal:     USD 13000.00
Tax:          USD 1040.00
Total Due:    USD 14040.00
```

**Raw Model Output:**
```
Based on the invoice provided, here are the extracted fields:

The vendor is Pinnacle Event Management and the invoice number is PEM-2024-0631. The invoice is dated 30/11/2024 with payment due by 30/12/2024. The currency is USD. There are three line items: Conference Room Hire (2 days at $3,200 each), AV Equipment Package (1 unit at $1,800), and Catering Lunch for 80 people (1 event at $4,800). The subtotal comes to $13,000.00. Tax of $1,040.00 is applied. The total amount due is $14,040.00.
```

---

## Doc-14 (PO / GBP / delivery present)

**Input:**
```
PURCHASE ORDER
Buyer:        Thames Water Authority
Supplier:     Grundfos Pumps Ltd
PO Number:    TWA-PO-2024-0881
Date:         2024-08-15
Requested Delivery: 2024-09-15
Currency:     GBP
Ordered Items:
  Grundfos CR 10-5 Centrifugal Pump   Qty:  6  @  4800.00
  Variable Speed Drive 11kW           Qty:  6  @  1650.00
  Pressure Transmitter 10 bar         Qty: 12  @   280.00
Order Total:  GBP 41340.00
```

**Raw Model Output:**
```
{
  "buyer": "Thames Water Authority",
  "supplier": "Grundfos Pumps Ltd",
  "po_number": "TWA-PO-2024-0881",
  "date": "2024-08-15",
  "delivery_date": "2024-09-15",
  "currency": "GBP",
  "total": 41340.0,
  "items": [
    {"item_name": "Grundfos CR 10-5 Centrifugal Pump", "quantity": 6, "unit_price": 4800.00},
    {"item_name": "Variable Speed Drive 11kW", "quantity": 6, "unit_price": 1650.00},
    {"item_name": "Pressure Transmitter 10 bar", "quantity": 12, "unit_price": 280.00}
  ]
}
```

---

## Doc-15 (Invoice / EUR / missing subtotal)

**Input:**
```
INVOICE
Vendor:       Maison du Mobilier SA
Invoice No:   MM-2024-0234
Date:         2024-10-25
Due Date:     2024-11-24
Currency:     EUR
Line Items:
  Executive Desk Walnut 180cm    Qty:   5  @  980.00
  Leather Office Chair Ergon     Qty:  10  @  540.00
  Bookcase Floor-to-Ceiling      Qty:   3  @  320.00
Total Due:    EUR 11360.00
```

**Raw Model Output:**
```
{
  "vendor": "Maison du Mobilier SA",
  "invoice_number": "MM-2024-0234",
  "date": "2024-10-25",
  "due_date": "2024-11-24",
  "currency": "EUR",
  "subtotal": 11360.00,
  "tax": null,
  "total": 11360.00,
  "line_items": [
    {"description": "Executive Desk Walnut 180cm", "quantity": 5, "unit_price": 980.00},
    {"description": "Leather Office Chair Ergon", "quantity": 10, "unit_price": 540.00},
    {"description": "Bookcase Floor-to-Ceiling", "quantity": 3, "unit_price": 320.00}
  ]
}
```

---

## Doc-16 (Invoice / USD / multi-item / markdown wrap)

**Input:**
```
INVOICE
Vendor:       Delta Pharmacare
Invoice No:   DP-2024-0910
Date:         12/12/2024
Due Date:     11/01/2025
Currency:     USD
Line Items:
  Amoxicillin Capsules 500mg x100   Qty:  80  @   12.00
  Metformin 850mg Tablets x60       Qty: 120  @   8.50
  Vitamin D3 1000IU Softgel x90    Qty:  60  @   6.00
Subtotal:     USD 2940.00
Tax:          USD 0.00
Total Due:    USD 2940.00
```

**Raw Model Output:**
```
```json
{
  "vendor": "Delta Pharmacare",
  "invoice_number": "DP-2024-0910",
  "date": "12/12/2024",
  "due_date": "11/01/2025",
  "currency": "USD",
  "subtotal": 2940.00,
  "tax": 0.00,
  "total": 2940.00,
  "line_items": [
    {"description": "Amoxicillin Capsules 500mg x100", "quantity": 80, "unit_price": 12.00},
    {"description": "Metformin 850mg Tablets x60", "quantity": 120, "unit_price": 8.50},
    {"description": "Vitamin D3 1000IU Softgel x90", "quantity": 60, "unit_price": 6.00}
  ]
}
```
```

---

## Doc-17 (PO / USD / single item)

**Input:**
```
PURCHASE ORDER
Buyer:        AlphaStream Telecom Inc
Supplier:     Nokia Networks
PO Number:    AST-PO-2024-NET-001
Date:         2024-11-01
Requested Delivery: 2025-02-28
Currency:     USD
Ordered Items:
  Nokia AirScale 5G Basestation    Qty:  20  @  85000.00
Order Total:  USD 1700000.00
```

**Raw Model Output:**
```
{
  "buyer": "AlphaStream Telecom Inc",
  "supplier": "Nokia Networks",
  "po_number": "AST-PO-2024-NET-001",
  "date": "2024-11-01",
  "delivery_date": "2025-02-28",
  "currency": "USD",
  "total": 1700000.0,
  "items": [
    {"item_name": "Nokia AirScale 5G Basestation", "quantity": 20, "unit_price": 85000.00}
  ]
}
```

---

## Doc-18 (Invoice / GBP / construction)

**Input:**
```
INVOICE
Vendor:       Clearwater Plumbing Services
Invoice No:   CPS-INV-2024-0055
Date:         01-10-2024
Due Date:     01-11-2024
Currency:     GBP
Line Items:
  Boiler Installation Combi 30kW   Qty:   1  @  2800.00
  Radiator 600x1200mm Double Panel Qty:   8  @   280.00
  Copper Pipe 22mm 3m length       Qty:  30  @    18.00
  Labour Plumbing 10 days          Qty:  10  @   320.00
Subtotal:     GBP 7824.00
Tax:          GBP 1564.80
Total Due:    GBP 9388.80
```

**Raw Model Output:**
```
{
  "vendor": "Clearwater Plumbing Services",
  "invoice_number": "CPS-INV-2024-0055",
  "date": "01-10-2024",
  "due_date": "01-11-2024",
  "currency": "GBP",
  "subtotal": 7824.00,
  "tax": 1564.80,
  "total": 9388.80,
  "line_items": [
    {"description": "Boiler Installation Combi 30kW", "quantity": 1, "unit_price": 2800.00},
    {"description": "Radiator 600x1200mm Double Panel", "quantity": 8, "unit_price": 280.00},
    {"description": "Copper Pipe 22mm 3m length", "quantity": 30, "unit_price": 18.00},
    {"description": "Labour Plumbing 10 days", "quantity": 10, "unit_price": 320.00}
  ]
}
```

---

## Doc-19 (PO / EUR / many items)

**Input:**
```
PURCHASE ORDER
Buyer:        Eurostore Retail NV
Supplier:     Philips Consumer Lifestyle
PO Number:    ER-PO-2024-CE-0441
Date:         2024-07-20
Requested Delivery: 2024-08-10
Currency:     EUR
Ordered Items:
  Philips Air Purifier AC3854   Qty:  50  @  299.00
  Philips Airfryer XXL HD9860   Qty:  80  @  209.00
  Philips Hue Starter Kit E27   Qty: 120  @   79.00
  Philips Sonicare DiamondClean Qty: 100  @  159.00
Order Total:  EUR 52870.00
```

**Raw Model Output:**
```
{
  "buyer": "Eurostore Retail NV",
  "supplier": "Philips Consumer Lifestyle",
  "po_number": "ER-PO-2024-CE-0441",
  "date": "2024-07-20",
  "delivery_date": "2024-08-10",
  "currency": "EUR",
  "total": 52870.0,
  "items": [
    {"item_name": "Philips Air Purifier AC3854", "quantity": 50, "unit_price": 299.00},
    {"item_name": "Philips Airfryer XXL HD9860", "quantity": 80, "unit_price": 209.00},
    {"item_name": "Philips Hue Starter Kit E27", "quantity": 120, "unit_price": 79.00},
    {"item_name": "Philips Sonicare DiamondClean", "quantity": 100, "unit_price": 159.00}
  ]
}
```

---

## Doc-20 (Invoice / USD / ambiguous format)

**Input:**
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
Subtotal:     USD 34000.00
Tax:          None
Total Due:    USD 34000.00
```

**Raw Model Output:**
```
I can extract the following information from this invoice:

{
  "vendor": "Summit Software Consultants",
  "invoice_number": "SSC-2024-ALPHA",
  "date": "Nov 30, 2024",
  "due_date": "Dec 30, 2024",
  "currency": "USD",
  "subtotal": 34000.00,
  "tax": null,
  "total": 34000.00,
  "line_items": [
    {"description": "Discovery Workshop 2 days", "quantity": 2, "unit_price": 8000.00},
    {"description": "Technical Architecture Design", "quantity": 1, "unit_price": 12000.00},
    {"description": "API Development 80 hours", "quantity": 80, "unit_price": 175.00}
  ]
}
```
