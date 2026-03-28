"""
generate_dataset.py
Generates 80 curated JSONL training examples:
  - 50 invoices (data/invoices_raw/)
  - 30 purchase orders (data/pos_raw/)
Writes to data/curated_train.jsonl
"""

import json
import os
import random

INSTRUCTION_INVOICE = (
    "Extract all invoice fields and return ONLY a valid JSON object. "
    "No explanation, no markdown, no code fences."
)
INSTRUCTION_PO = (
    "Extract all purchase order fields and return ONLY a valid JSON object. "
    "No explanation, no markdown, no code fences."
)

# ── Invoice raw text templates ────────────────────────────────────────────────

def make_invoice_text(v, inv_no, date, due, currency, subtotal, tax, total, items):
    lines = "\n".join(
        f"  {it['description']:<35} Qty:{it['quantity']:>4}  @{it['unit_price']:>9.2f}"
        for it in items
    )
    tax_str = f"Tax:          {currency} {tax:.2f}" if tax is not None else "Tax:          N/A"
    due_str = f"Due Date:  {due}" if due else "Due Date:  Not specified"
    return f"""
INVOICE

Vendor:       {v}
Invoice No:   {inv_no}
Date:         {date}
{due_str}
Currency:     {currency}

Line Items:
{lines}

Subtotal:     {currency} {subtotal:.2f}
{tax_str}
Total Due:    {currency} {total:.2f}
""".strip()

# ── PO raw text templates ─────────────────────────────────────────────────────

def make_po_text(buyer, supplier, po_no, date, del_date, currency, total, items):
    lines = "\n".join(
        f"  {it['item_name']:<35} Qty:{it['quantity']:>5}  @{it['unit_price']:>10.2f}"
        for it in items
    )
    del_str = f"Requested Delivery: {del_date}" if del_date else "Requested Delivery: TBD"
    return f"""
PURCHASE ORDER

Buyer:        {buyer}
Supplier:     {supplier}
PO Number:    {po_no}
Date:         {date}
{del_str}
Currency:     {currency}

Ordered Items:
{lines}

Order Total:  {currency} {total:.2f}
""".strip()

# ── Invoice Data ──────────────────────────────────────────────────────────────

INVOICES = [
    # 1
    dict(vendor="Apex Office Supplies Ltd", invoice_number="INV-2024-00341", date="2024-06-12",
         due_date="2024-07-12", currency="USD", subtotal=840.00, tax=67.20, total=907.20,
         line_items=[{"description":"A4 Paper Ream 500 sheets","quantity":20,"unit_price":12.00},
                     {"description":"Ballpoint Pens Box of 50","quantity":10,"unit_price":24.00},
                     {"description":"Stapler Heavy Duty","quantity":5,"unit_price":36.00}]),
    # 2
    dict(vendor="TechVision Components GmbH", invoice_number="TV-9921-B", date="2024-03-01",
         due_date="2024-04-01", currency="EUR", subtotal=4200.00, tax=798.00, total=4998.00,
         line_items=[{"description":"Raspberry Pi 4 Model B 8GB","quantity":50,"unit_price":75.00},
                     {"description":"USB-C Power Adapter 45W","quantity":50,"unit_price":9.00}]),
    # 3
    dict(vendor="Sunrise Catering Services", invoice_number="SCS-2024-112", date="2024-07-20",
         due_date=None, currency="USD", subtotal=3200.00, tax=None, total=3200.00,
         line_items=[{"description":"Corporate Lunch Package 50 pax","quantity":2,"unit_price":1600.00}]),
    # 4
    dict(vendor="Bharat Electricals Pvt Ltd", invoice_number="BEL/24/0088", date="2024-01-15",
         due_date="2024-02-14", currency="INR", subtotal=125000.00, tax=22500.00, total=147500.00,
         line_items=[{"description":"LED Street Light 100W","quantity":100,"unit_price":950.00},
                     {"description":"Copper Cable 4mm 100m roll","quantity":25,"unit_price":1200.00}]),
    # 5
    dict(vendor="Nordic Timber AS", invoice_number="NT-20240899", date="2024-09-03",
         due_date="2024-10-03", currency="EUR", subtotal=18600.00, tax=3534.00, total=22134.00,
         line_items=[{"description":"Spruce Plank 22x100mm 4.8m","quantity":600,"unit_price":18.00},
                     {"description":"Pine Beam 50x100mm 6.0m","quantity":200,"unit_price":24.00},
                     {"description":"OSB Board 18mm 2440x1220","quantity":150,"unit_price":22.00}]),
    # 6
    dict(vendor="CleanWorks Facility Management", invoice_number="CW-0071", date="2024-05-31",
         due_date=None, currency="GBP", subtotal=1850.00, tax=370.00, total=2220.00,
         line_items=[{"description":"Office Deep Clean Service","quantity":1,"unit_price":1200.00},
                     {"description":"Window Cleaning External 3 floors","quantity":1,"unit_price":450.00},
                     {"description":"Consumables Supply","quantity":1,"unit_price":200.00}]),
    # 7
    dict(vendor="Fuji Precision Tools Co Ltd", invoice_number="FPT-2024-4412", date="2024-11-10",
         due_date="2024-12-10", currency="JPY", subtotal=840000.00, tax=84000.00, total=924000.00,
         line_items=[{"description":"CNC End Mill 6mm Carbide","quantity":200,"unit_price":2800.00},
                     {"description":"Indexable Insert APMT 1604","quantity":500,"unit_price":840.00}]),
    # 8
    dict(vendor="QuickPrint Digital", invoice_number="QPD-552", date="2024-02-28",
         due_date="2024-03-28", currency="USD", subtotal=620.00, tax=49.60, total=669.60,
         line_items=[{"description":"Business Cards 500 qty gloss","quantity":5,"unit_price":60.00},
                     {"description":"A1 Poster Print Full Colour","quantity":20,"unit_price":14.00},
                     {"description":"Lamination A4 25 sheets","quantity":4,"unit_price":15.00}]),
    # 9
    dict(vendor="Atlas Logistics BV", invoice_number="ATL-2024-3301", date="2024-08-19",
         due_date="2024-09-18", currency="EUR", subtotal=7800.00, tax=None, total=7800.00,
         line_items=[{"description":"FCL Sea Freight Rotterdam to Mumbai","quantity":1,"unit_price":6200.00},
                     {"description":"Port Handling & Documentation","quantity":1,"unit_price":1600.00}]),
    # 10
    dict(vendor="Cornerstone Real Estate LLC", invoice_number="CRE-2024-007", date="2024-10-01",
         due_date="2024-10-15", currency="USD", subtotal=12000.00, tax=None, total=12000.00,
         line_items=[{"description":"Commercial Office Lease Oct 2024","quantity":1,"unit_price":12000.00}]),
    # 11
    dict(vendor="Medline Pharmaceuticals", invoice_number="MED-44009", date="2024-04-11",
         due_date="2024-05-11", currency="USD", subtotal=9430.00, tax=0.00, total=9430.00,
         line_items=[{"description":"Paracetamol 500mg Tablets x1000","quantity":20,"unit_price":45.00},
                     {"description":"Surgical Gloves Box L x100","quantity":50,"unit_price":18.00},
                     {"description":"Disposable Syringes 5ml x50","quantity":150,"unit_price":32.00},
                     {"description":"Alcohol Swabs Box x200","quantity":10,"unit_price":8.00}]),
    # 12
    dict(vendor="Greenleaf Agricultural Supplies", invoice_number="GAS/2024/0219", date="2024-03-20",
         due_date=None, currency="INR", subtotal=87500.00, tax=None, total=87500.00,
         line_items=[{"description":"Urea Fertiliser 50kg bag","quantity":100,"unit_price":650.00},
                     {"description":"Drip Irrigation Kit 1 acre","quantity":25,"unit_price":1100.00}]),
    # 13
    dict(vendor="SkyBridge IT Solutions", invoice_number="SBS-IT-2024-0089", date="2024-06-30",
         due_date="2024-07-30", currency="USD", subtotal=22500.00, tax=None, total=22500.00,
         line_items=[{"description":"Cloud Infrastructure Setup Q2","quantity":1,"unit_price":14000.00},
                     {"description":"Managed Security Service Monthly","quantity":1,"unit_price":5500.00},
                     {"description":"24/7 NOC Support June 2024","quantity":1,"unit_price":3000.00}]),
    # 14
    dict(vendor="Castello Foods SpA", invoice_number="CF-2024-1188", date="2024-02-14",
         due_date="2024-03-14", currency="EUR", subtotal=4860.00, tax=388.80, total=5248.80,
         line_items=[{"description":"Extra Virgin Olive Oil 5L tin","quantity":120,"unit_price":18.00},
                     {"description":"Parmigiano Reggiano 1kg vacuum","quantity":80,"unit_price":22.50},
                     {"description":"San Marzano Tomatoes 400g can","quantity":240,"unit_price":2.40}]),
    # 15
    dict(vendor="Ironclad Security Systems", invoice_number="ISS-20240605", date="2024-06-05",
         due_date="2024-07-05", currency="GBP", subtotal=6700.00, tax=1340.00, total=8040.00,
         line_items=[{"description":"4K CCTV Camera Outdoor","quantity":8,"unit_price":280.00},
                     {"description":"NVR 16-Channel 4TB","quantity":1,"unit_price":650.00},
                     {"description":"Access Control Door Unit","quantity":4,"unit_price":450.00},
                     {"description":"Installation & Commissioning","quantity":1,"unit_price":1650.00}]),
    # 16 - minimal fields, no tax, no due_date
    dict(vendor="Solo Contractor Works", invoice_number="SCW-001", date="2024-01-05",
         due_date=None, currency="USD", subtotal=500.00, tax=None, total=500.00,
         line_items=[{"description":"General Repair Labour 5hrs","quantity":5,"unit_price":100.00}]),
    # 17
    dict(vendor="Bright Future Education Trust", invoice_number="BFET-2024-33", date="2024-08-01",
         due_date="2024-08-31", currency="INR", subtotal=75000.00, tax=None, total=75000.00,
         line_items=[{"description":"Annual Subscription - LMS Platform","quantity":1,"unit_price":75000.00}]),
    # 18
    dict(vendor="Pacific Rim Trading Co", invoice_number="PRT-0042", date="2024-09-25",
         due_date="2024-10-25", currency="USD", subtotal=31200.00, tax=2496.00, total=33696.00,
         line_items=[{"description":"Bamboo Flooring 1m2 natural","quantity":600,"unit_price":28.00},
                     {"description":"Underlayer Foam Roll 10m","quantity":80,"unit_price":45.00},
                     {"description":"Installation Adhesive 5L","quantity":60,"unit_price":32.00},
                     {"description":"Finishing Trim 3m lengths","quantity":200,"unit_price":8.00}]),
    # 19
    dict(vendor="CloudNine Telecom", invoice_number="CNT-INV-AUG24", date="2024-08-31",
         due_date="2024-09-30", currency="USD", subtotal=1840.00, tax=147.20, total=1987.20,
         line_items=[{"description":"Business Fibre Broadband 1Gbps Aug","quantity":1,"unit_price":299.00},
                     {"description":"SIP Trunk Bundle 10 channels","quantity":1,"unit_price":450.00},
                     {"description":"Hosted PBX System Monthly","quantity":1,"unit_price":891.00},
                     {"description":"International Minutes Bundle","quantity":1,"unit_price":200.00}]),
    # 20 - non-USD, multi-item
    dict(vendor="MediSupply Deutschland GmbH", invoice_number="MS-DE-2024-0771", date="2024-05-17",
         due_date="2024-06-17", currency="EUR", subtotal=11440.00, tax=2173.60, total=13613.60,
         line_items=[{"description":"N95 Respirator Mask box/20","quantity":400,"unit_price":12.00},
                     {"description":"Nitrile Exam Gloves M box/100","quantity":200,"unit_price":14.20},
                     {"description":"Isolation Gown Disposable L","quantity":300,"unit_price":8.80},
                     {"description":"Face Shield Anti-fog","quantity":100,"unit_price":6.00}]),
    # 21
    dict(vendor="Horizon Renewable Energy", invoice_number="HRE-2024-0015", date="2024-07-01",
         due_date="2024-08-01", currency="USD", subtotal=145000.00, tax=None, total=145000.00,
         line_items=[{"description":"Solar Panel 400W Monocrystalline","quantity":200,"unit_price":210.00},
                     {"description":"Inverter 10kW Grid-tie","quantity":10,"unit_price":1800.00},
                     {"description":"Battery Storage 10kWh","quantity":5,"unit_price":4200.00},
                     {"description":"Mounting Rack & Hardware","quantity":200,"unit_price":28.00}]),
    # 22
    dict(vendor="Premium Auto Parts Sdn Bhd", invoice_number="PAP-2024-2210", date="2024-04-18",
         due_date="2024-05-18", currency="USD", subtotal=8750.00, tax=875.00, total=9625.00,
         line_items=[{"description":"Brake Pad Set Front Axle","quantity":50,"unit_price":65.00},
                     {"description":"Alternator 120A Remanufactured","quantity":25,"unit_price":110.00},
                     {"description":"Air Filter Panel Type","quantity":75,"unit_price":22.00},
                     {"description":"Engine Oil 5W-30 4L","quantity":100,"unit_price":18.00}]),
    # 23 - only one line item
    dict(vendor="Saas Analytics Pro", invoice_number="SAP-0192", date="2024-12-01",
         due_date="2025-01-01", currency="USD", subtotal=4999.00, tax=None, total=4999.00,
         line_items=[{"description":"Enterprise Analytics License Annual","quantity":1,"unit_price":4999.00}]),
    # 24 - GBP
    dict(vendor="Albion Print & Design", invoice_number="APD-2024-554", date="2024-11-20",
         due_date="2024-12-20", currency="GBP", subtotal=2140.00, tax=428.00, total=2568.00,
         line_items=[{"description":"Brochure A4 Full Colour 500 qty","quantity":1,"unit_price":320.00},
                     {"description":"Roll-up Banner 85x200cm","quantity":5,"unit_price":85.00},
                     {"description":"Branded Tote Bag 250 qty","quantity":1,"unit_price":1395.00}]),
    # 25 - no tax, INR
    dict(vendor="Shree Builders Materials", invoice_number="SBM/2024/3381", date="2024-06-10",
         due_date="2024-07-10", currency="INR", subtotal=349500.00, tax=None, total=349500.00,
         line_items=[{"description":"OPC 53 Cement 50kg bag","quantity":500,"unit_price":380.00},
                     {"description":"TMT Steel Bar 12mm 1 tonne","quantity":5,"unit_price":62900.00},
                     {"description":"Red Brick per 1000","quantity":10,"unit_price":7200.00}]),
    # 26
    dict(vendor="Cascade Water Solutions", invoice_number="CWS-INV-0084", date="2024-02-01",
         due_date=None, currency="USD", subtotal=3600.00, tax=288.00, total=3888.00,
         line_items=[{"description":"Water Filtration System Industrial","quantity":3,"unit_price":900.00},
                     {"description":"Replacement Filter Cartridge","quantity":12,"unit_price":75.00}]),
    # 27 - JPY
    dict(vendor="Kyoto Textile Manufacturing", invoice_number="KTM-2024-0088", date="2024-07-15",
         due_date="2024-08-15", currency="JPY", subtotal=560000.00, tax=56000.00, total=616000.00,
         line_items=[{"description":"Cotton Plain Weave 110cm roll","quantity":200,"unit_price":1800.00},
                     {"description":"Polyester Blend Fabric 150cm","quantity":100,"unit_price":2000.00}]),
    # 28 - minimal, one item, EUR
    dict(vendor="Berliner Consulting Group", invoice_number="BCG-2024-0031", date="2024-10-15",
         due_date="2024-11-14", currency="EUR", subtotal=12000.00, tax=2280.00, total=14280.00,
         line_items=[{"description":"Strategy Consulting Retainer Oct 2024","quantity":1,"unit_price":12000.00}]),
    # 29 - no due_date, no tax
    dict(vendor="FreshMart Wholesale", invoice_number="FMW-0872", date="2024-01-22",
         due_date=None, currency="USD", subtotal=2340.00, tax=None, total=2340.00,
         line_items=[{"description":"Organic Apples 10kg case","quantity":30,"unit_price":22.00},
                     {"description":"Mixed Salad Leaves 2kg bag","quantity":60,"unit_price":14.00},
                     {"description":"Roma Tomatoes 5kg tray","quantity":40,"unit_price":18.00}]),
    # 30 - multi-item, USD
    dict(vendor="DeepSea Marine Engineering", invoice_number="DME-2024-0119", date="2024-09-12",
         due_date="2024-10-12", currency="USD", subtotal=87400.00, tax=None, total=87400.00,
         line_items=[{"description":"Marine Diesel Engine 250kW overhaul","quantity":1,"unit_price":48000.00},
                     {"description":"Propeller Shaft Bearing replacement","quantity":2,"unit_price":4200.00},
                     {"description":"Hull Antifouling Paint 20L","quantity":50,"unit_price":120.00},
                     {"description":"Crane Hydraulic Service","quantity":1,"unit_price":29000.00}]),
    # 31
    dict(vendor="VividColors Paints Ltd", invoice_number="VCP-2024-881", date="2024-03-05",
         due_date="2024-04-04", currency="GBP", subtotal=4850.00, tax=970.00, total=5820.00,
         line_items=[{"description":"Interior Emulsion White 10L","quantity":50,"unit_price":28.00},
                     {"description":"Exterior Gloss Cream 5L","quantity":40,"unit_price":32.00},
                     {"description":"Primer Undercoat 5L","quantity":30,"unit_price":25.00},
                     {"description":"Foam Roller Set 9 inch","quantity":60,"unit_price":8.50}]),
    # 32 - no line item qty stated -> default 1
    dict(vendor="Executive Travel Associates", invoice_number="ETA-F24-0033", date="2024-05-09",
         due_date="2024-05-23", currency="USD", subtotal=7200.00, tax=None, total=7200.00,
         line_items=[{"description":"Business Class Return Ticket NYC-LHR","quantity":1,"unit_price":4800.00},
                     {"description":"5-Star Hotel 4 nights London","quantity":1,"unit_price":2400.00}]),
    # 33 - INR, tax present
    dict(vendor="Infospark IT Services Pvt Ltd", invoice_number="IS-2024-0561", date="2024-08-20",
         due_date="2024-09-19", currency="INR", subtotal=180000.00, tax=32400.00, total=212400.00,
         line_items=[{"description":"Software Development 120 hours","quantity":120,"unit_price":1000.00},
                     {"description":"QA Testing 40 hours","quantity":40,"unit_price":700.00},
                     {"description":"Project Management 20 hours","quantity":20,"unit_price":1100.00}]),
    # 34 - EUR, many items
    dict(vendor="Ecopack Sustainable Packaging", invoice_number="EP-2024-0450", date="2024-04-01",
         due_date="2024-05-01", currency="EUR", subtotal=15200.00, tax=2888.00, total=18088.00,
         line_items=[{"description":"Cardboard Box 30x20x15cm flat pack","quantity":2000,"unit_price":0.85},
                     {"description":"Compostable Mailer Bag 35x50cm","quantity":3000,"unit_price":0.60},
                     {"description":"Kraft Paper Wrap Roll 50cm","quantity":50,"unit_price":22.00},
                     {"description":"Biodegradable Packing Peanuts 30L","quantity":100,"unit_price":8.00},
                     {"description":"Printed Tissue Paper 500 sheets","quantity":10,"unit_price":45.00}]),
    # 35
    dict(vendor="LabTech Instruments Inc", invoice_number="LTI-24-1802", date="2024-11-01",
         due_date="2024-12-01", currency="USD", subtotal=34680.00, tax=2774.40, total=37454.40,
         line_items=[{"description":"Digital Oscilloscope 4ch 200MHz","quantity":4,"unit_price":2800.00},
                     {"description":"Bench Power Supply 0-30V 5A","quantity":8,"unit_price":420.00},
                     {"description":"Function Generator 10MHz","quantity":6,"unit_price":560.00},
                     {"description":"Multimeter True RMS","quantity":20,"unit_price":89.00}]),
    # 36 - no tax, no due_date
    dict(vendor="Hartland Stables & Arena", invoice_number="HSA-INV-0004", date="2024-06-20",
         due_date=None, currency="GBP", subtotal=1200.00, tax=None, total=1200.00,
         line_items=[{"description":"Arena Hire Full Day","quantity":1,"unit_price":800.00},
                     {"description":"Stabling 5 horses weekend","quantity":1,"unit_price":400.00}]),
    # 37 - USD, multiple items
    dict(vendor="SteelCraft Fabricators Inc", invoice_number="SCF-2024-0277", date="2024-07-08",
         due_date="2024-08-07", currency="USD", subtotal=62400.00, tax=4992.00, total=67392.00,
         line_items=[{"description":"Structural Steel H-Beam 200x200 6m","quantity":80,"unit_price":380.00},
                     {"description":"Steel Plate 10mm 2400x1200","quantity":60,"unit_price":290.00},
                     {"description":"Welding Rod E7018 5kg","quantity":200,"unit_price":28.00},
                     {"description":"Cutting & Fabrication Labour","quantity":1,"unit_price":8800.00}]),
    # 38 - EUR single item
    dict(vendor="GreenEnergy Certificates BV", invoice_number="GEC-2024-0088", date="2024-10-30",
         due_date="2024-11-29", currency="EUR", subtotal=25000.00, tax=None, total=25000.00,
         line_items=[{"description":"Renewable Energy Certificate 100MWh","quantity":100,"unit_price":250.00}]),
    # 39 - INR no due_date
    dict(vendor="Sunrise Textiles Mills", invoice_number="STM/2024/8801", date="2024-09-15",
         due_date=None, currency="INR", subtotal=445000.00, tax=80100.00, total=525100.00,
         line_items=[{"description":"Cotton Yarn 30s Count 1 tonne","quantity":10,"unit_price":28000.00},
                     {"description":"Dyed Fabric Polyester 150cm roll","quantity":500,"unit_price":180.00},
                     {"description":"Zipper Nylon 30cm pcs","quantity":5000,"unit_price":5.00}]),
    # 40
    dict(vendor="UrbanChef Catering Group", invoice_number="UCG-2024-0214", date="2024-12-15",
         due_date="2024-12-31", currency="GBP", subtotal=8400.00, tax=1680.00, total=10080.00,
         line_items=[{"description":"Christmas Corporate Dinner 100 covers","quantity":1,"unit_price":5500.00},
                     {"description":"Canapes Reception 100 pax","quantity":1,"unit_price":1800.00},
                     {"description":"Bar Package 4 hours open bar","quantity":1,"unit_price":1100.00}]),
    # 41 - USD, minimal, null tax
    dict(vendor="CreativeEdge Design Studio", invoice_number="CE-2024-0082", date="2024-02-10",
         due_date="2024-03-10", currency="USD", subtotal=3500.00, tax=None, total=3500.00,
         line_items=[{"description":"Brand Identity Design Package","quantity":1,"unit_price":2200.00},
                     {"description":"Social Media Asset Pack","quantity":1,"unit_price":1300.00}]),
    # 42 - JPY, two items
    dict(vendor="Osaka Printing Works", invoice_number="OPW-2024-1041", date="2024-05-28",
         due_date="2024-06-27", currency="JPY", subtotal=380000.00, tax=38000.00, total=418000.00,
         line_items=[{"description":"Catalogue A4 Full Colour 1000 qty","quantity":1000,"unit_price":320.00},
                     {"description":"Leaflet A5 2-sided 5000 qty","quantity":5000,"unit_price":12.00}]),
    # 43 - USD, many items
    dict(vendor="HealthFirst Medical Supplies", invoice_number="HFM-2024-7712", date="2024-03-30",
         due_date="2024-04-29", currency="USD", subtotal=21350.00, tax=1708.00, total=23058.00,
         line_items=[{"description":"Blood Glucose Test Strips box/50","quantity":200,"unit_price":18.00},
                     {"description":"Insulin Syringe 1ml 29G box/100","quantity":150,"unit_price":32.00},
                     {"description":"Pulse Oximeter Desktop","quantity":10,"unit_price":145.00},
                     {"description":"Exam Table Paper Roll 21 inch","quantity":50,"unit_price":12.00},
                     {"description":"Latex Free Tourniquet 18 inch","quantity":100,"unit_price":3.50}]),
    # 44 - EUR no tax
    dict(vendor="EuroFreight Logistics GmbH", invoice_number="EFL-2024-3302", date="2024-06-01",
         due_date=None, currency="EUR", subtotal=9400.00, tax=None, total=9400.00,
         line_items=[{"description":"Truck Freight Hamburg to Warsaw","quantity":1,"unit_price":4200.00},
                     {"description":"Warehouse Storage 3 months","quantity":3,"unit_price":1400.00},
                     {"description":"Customs Clearance Service","quantity":1,"unit_price":800.00}]),
    # 45 - USD, single labour item
    dict(vendor="Praxis Legal Consulting", invoice_number="PLC-2024-0044", date="2024-10-20",
         due_date="2024-11-19", currency="USD", subtotal=8500.00, tax=None, total=8500.00,
         line_items=[{"description":"Legal Retainer October 2024","quantity":1,"unit_price":8500.00}]),
    # 46 - GBP multi-item
    dict(vendor="Highfield Garden Supplies", invoice_number="HGS-2024-0392", date="2024-04-25",
         due_date="2024-05-25", currency="GBP", subtotal=6830.00, tax=1366.00, total=8196.00,
         line_items=[{"description":"Premium Topsoil 1 tonne bag","quantity":20,"unit_price":82.00},
                     {"description":"Ornamental Bark Chippings 60L bag","quantity":100,"unit_price":8.00},
                     {"description":"Grass Seed Lawn Mix 10kg","quantity":30,"unit_price":45.00},
                     {"description":"Fertiliser Granular 25kg","quantity":25,"unit_price":28.00},
                     {"description":"Raised Bed Cedar 1.2x0.9m","quantity":15,"unit_price":110.00}]),
    # 47 - INR, no due_date
    dict(vendor="Deepak Pharma Distributors", invoice_number="DPD/2024/0312", date="2024-07-30",
         due_date=None, currency="INR", subtotal=220000.00, tax=None, total=220000.00,
         line_items=[{"description":"Azithromycin 500mg Strip/10 tablets","quantity":2000,"unit_price":65.00},
                     {"description":"Metformin 1000mg Strip/15 tablets","quantity":1500,"unit_price":48.00},
                     {"description":"Omeprazole 20mg Strip/15 capsules","quantity":1000,"unit_price":32.00}]),
    # 48 - EUR, small invoice
    dict(vendor="Boulangerie Artisanale Moreau", invoice_number="BAM-2024-001", date="2024-01-31",
         due_date="2024-02-14", currency="EUR", subtotal=480.00, tax=24.00, total=504.00,
         line_items=[{"description":"Sourdough Loaf 800g","quantity":40,"unit_price":5.50},
                     {"description":"Croissant Butter x12","quantity":20,"unit_price":7.20},
                     {"description":"Tart Citron Whole","quantity":10,"unit_price":12.00}]),
    # 49 - USD many items, null due_date
    dict(vendor="Wellspring Construction Materials", invoice_number="WCM-2024-0821", date="2024-08-05",
         due_date=None, currency="USD", subtotal=178600.00, tax=14288.00, total=192888.00,
         line_items=[{"description":"Ready Mix Concrete 30MPa m3","quantity":200,"unit_price":185.00},
                     {"description":"Rebar 16mm 12m bar","quantity":500,"unit_price":48.00},
                     {"description":"Plywood Shutter Form 18mm Sheet","quantity":300,"unit_price":38.00},
                     {"description":"Concrete Block 200mm each","quantity":3000,"unit_price":4.20},
                     {"description":"Mortar Mix 25kg bag","quantity":400,"unit_price":8.50}]),
    # 50 - GBP, null tax, null due_date
    dict(vendor="North Sea Energy Consultants", invoice_number="NSE-2024-CC001", date="2024-10-01",
         due_date=None, currency="GBP", subtotal=35000.00, tax=None, total=35000.00,
         line_items=[{"description":"Offshore Site Assessment Report","quantity":1,"unit_price":20000.00},
                     {"description":"Environmental Impact Consultation","quantity":1,"unit_price":15000.00}]),
]

# ── Purchase Order Data ───────────────────────────────────────────────────────

PURCHASE_ORDERS = [
    # 1
    dict(buyer="GlobalTech Manufacturing Inc", supplier="Precision Parts Co",
         po_number="PO-2024-8821", date="2024-08-01", delivery_date="2024-08-22",
         currency="USD", total=14750.00,
         items=[{"item_name":"Steel Bracket Type-A","quantity":500,"unit_price":12.50},
                {"item_name":"Hex Bolt M8 x 30mm","quantity":2000,"unit_price":0.85},
                {"item_name":"Rubber Gasket 50mm","quantity":300,"unit_price":7.00}]),
    # 2
    dict(buyer="Sunrise Retail Pvt Ltd", supplier="FastTrack Logistics",
         po_number="SR-PO-2024-0041", date="2024-03-10", delivery_date=None,
         currency="INR", total=425000.00,
         items=[{"item_name":"Pallet Racking Beam 2.7m","quantity":100,"unit_price":2800.00},
                {"item_name":"Pallet Racking Upright 6m","quantity":50,"unit_price":3300.00}]),
    # 3
    dict(buyer="Northgate Hospitals NHS Trust", supplier="SterileSupply UK Ltd",
         po_number="NHS-PO-24-0081", date="2024-06-15", delivery_date="2024-07-01",
         currency="GBP", total=31200.00,
         items=[{"item_name":"Surgical Drape 120x150cm sterile","quantity":500,"unit_price":14.00},
                {"item_name":"Scalpel Handle #3","quantity":200,"unit_price":9.50},
                {"item_name":"Suture Vicryl 2-0 36 per box","quantity":100,"unit_price":88.00},
                {"item_name":"Surgical Gloves Size 7 box/50","quantity":400,"unit_price":22.50}]),
    # 4
    dict(buyer="Mittelstand Automotive GmbH", supplier="RubberTech Europe BV",
         po_number="MA-PO-2024-4401", date="2024-04-20", delivery_date="2024-05-15",
         currency="EUR", total=58200.00,
         items=[{"item_name":"EPDM Seal Strip 10mm 100m roll","quantity":300,"unit_price":48.00},
                {"item_name":"Silicone O-Ring AS568-214 box/100","quantity":500,"unit_price":28.80},
                {"item_name":"Polyurethane Bushing 40mm","quantity":1000,"unit_price":15.60}]),
    # 5
    dict(buyer="Pacific Hotels Group", supplier="Luxe Linen Trading",
         po_number="PHG-PO-2024-0119", date="2024-09-01", delivery_date="2024-09-20",
         currency="USD", total=24800.00,
         items=[{"item_name":"King Size Duvet Cover Egyptian Cotton","quantity":200,"unit_price":48.00},
                {"item_name":"Pillow Case Set King Size","quantity":400,"unit_price":18.00},
                {"item_name":"Bath Towel 700gsm White","quantity":600,"unit_price":14.00},
                {"item_name":"Hand Towel 500gsm White","quantity":600,"unit_price":8.00}]),
    # 6 - no delivery_date
    dict(buyer="Amazonas Agro SA", supplier="BASF Brazil Ltda",
         po_number="AGA-PO-2024-055", date="2024-02-28", delivery_date=None,
         currency="USD", total=310000.00,
         items=[{"item_name":"Glyphosate 480g/L SL 1000L IBC","quantity":50,"unit_price":3200.00},
                {"item_name":"Atrazine 500g/L SC 200L drum","quantity":100,"unit_price":1400.00},
                {"item_name":"Mancozeb 80% WP 25kg bag","quantity":200,"unit_price":420.00}]),
    # 7
    dict(buyer="CityGrid Power Authority", supplier="ABB Electrification",
         po_number="CGP-2024-E0042", date="2024-07-10", delivery_date="2024-09-10",
         currency="USD", total=428500.00,
         items=[{"item_name":"MV Switchgear 12kV Panel","quantity":5,"unit_price":38000.00},
                {"item_name":"Power Transformer 500kVA 11/0.4kV","quantity":3,"unit_price":52000.00},
                {"item_name":"LV Distribution Board 8-way","quantity":20,"unit_price":4200.00},
                {"item_name":"Cable Ladder 100x50mm 3m HDG","quantity":200,"unit_price":85.00}]),
    # 8 - EUR, no delivery_date
    dict(buyer="Academie Gastronomique Paris", supplier="Rungis Wholesale Food Market",
         po_number="AGP-PO-2024-018", date="2024-01-15", delivery_date=None,
         currency="EUR", total=9760.00,
         items=[{"item_name":"Wagyu Beef A5 Grade 1kg","quantity":20,"unit_price":180.00},
                {"item_name":"Black Truffle Fresh 100g","quantity":50,"unit_price":85.00},
                {"item_name":"Foie Gras Entier Bloc 500g","quantity":30,"unit_price":65.00},
                {"item_name":"Champagne Vintage Brut 750ml","quantity":60,"unit_price":48.00}]),
    # 9
    dict(buyer="BlueLine Shipping Corp", supplier="Makita Tools Distribution",
         po_number="BLS-PO-2024-3302", date="2024-10-05", delivery_date="2024-10-25",
         currency="USD", total=18720.00,
         items=[{"item_name":"Cordless Drill Driver 18V Kit","quantity":40,"unit_price":189.00},
                {"item_name":"Angle Grinder 115mm 750W","quantity":30,"unit_price":124.00},
                {"item_name":"Jigsaw Pendulum 701W","quantity":20,"unit_price":148.00},
                {"item_name":"Drilling Bit Set 19pc","quantity":60,"unit_price":38.00}]),
    # 10 - INR
    dict(buyer="Rajasthan State Electricity Board", supplier="Finolex Cables Ltd",
         po_number="RSEB/PO/2024/1108", date="2024-05-20", delivery_date="2024-06-30",
         currency="INR", total=5850000.00,
         items=[{"item_name":"XLPE Insulated Cable 240mm2 metre","quantity":10000,"unit_price":385.00},
                {"item_name":"XLPE Cable 120mm2 metre","quantity":5000,"unit_price":220.00},
                {"item_name":"PVC Copper Cable 16mm2 metre","quantity":8000,"unit_price":80.00}]),
    # 11
    dict(buyer="Northern Star Mining Ltd", supplier="Komatsu Australia Pty",
         po_number="NSM-2024-E0018", date="2024-03-01", delivery_date="2024-06-01",
         currency="USD", total=2650000.00,
         items=[{"item_name":"Mining Haul Truck HD785-7","quantity":2,"unit_price":1100000.00},
                {"item_name":"Excavator PC2000-11","quantity":1,"unit_price":450000.00}]),
    # 12 - GBP, many items
    dict(buyer="Britannia University", supplier="Scientific & Lab Supplies PLC",
         po_number="BU-PO-2024-0441", date="2024-08-25", delivery_date="2024-09-15",
         currency="GBP", total=48600.00,
         items=[{"item_name":"Analytical Balance 0.1mg","quantity":5,"unit_price":1800.00},
                {"item_name":"Centrifuge 10000RPM 24-place","quantity":3,"unit_price":4200.00},
                {"item_name":"pH Meter Benchtop","quantity":8,"unit_price":380.00},
                {"item_name":"Pipette Electronic 1000ul","quantity":20,"unit_price":290.00},
                {"item_name":"Laboratory Oven 50L Forced Air","quantity":2,"unit_price":1650.00}]),
    # 13 - no delivery date, EUR
    dict(buyer="Benelux Food Retailers Coop", supplier="Danone Fresh Dairy",
         po_number="BFR-2024-PO-0287", date="2024-11-01", delivery_date=None,
         currency="EUR", total=42000.00,
         items=[{"item_name":"Greek Yogurt Natural 1kg pot","quantity":1200,"unit_price":1.80},
                {"item_name":"Skyr Protein 500g","quantity":800,"unit_price":2.40},
                {"item_name":"Cheese Spread 200g pack","quantity":2000,"unit_price":1.50},
                {"item_name":"Probiotic Drinking Yogurt 100g","quantity":3000,"unit_price":0.80}]),
    # 14 - USD
    dict(buyer="SunTech Solar Installations", supplier="Jinko Solar Europe GmbH",
         po_number="STS-PO-2024-0091", date="2024-07-15", delivery_date="2024-08-10",
         currency="USD", total=156000.00,
         items=[{"item_name":"Bifacial Solar Module 480W","quantity":300,"unit_price":490.00},
                {"item_name":"String Inverter 20kW","quantity":10,"unit_price":2100.00}]),
    # 15 - INR no delivery_date
    dict(buyer="Tata Consultancy Services", supplier="Dell Technologies India",
         po_number="TCS-HW-2024-0442", date="2024-09-01", delivery_date=None,
         currency="INR", total=9850000.00,
         items=[{"item_name":"Dell PowerEdge R760 Server","quantity":20,"unit_price":380000.00},
                {"item_name":"Dell EMC PowerVault ME5012 Storage","quantity":5,"unit_price":250000.00},
                {"item_name":"Dell 48-Port Network Switch","quantity":10,"unit_price":85000.00}]),
    # 16 - GBP small PO
    dict(buyer="Westfield Events Ltd", supplier="EventPro Hire",
         po_number="WEL-PO-2024-0021", date="2024-05-10", delivery_date="2024-05-24",
         currency="GBP", total=4800.00,
         items=[{"item_name":"6m x 3m Marquee Structure","quantity":4,"unit_price":600.00},
                {"item_name":"Round Table Hire per day","quantity":30,"unit_price":25.00},
                {"item_name":"Banquet Chair Hire per day","quantity":240,"unit_price":4.50},
                {"item_name":"PA System Full Rig Weekend","quantity":1,"unit_price":1500.00}]),
    # 17 - EUR, multi-item
    dict(buyer="Dutch Flower Exports BV", supplier="Syngenta Seeds AG",
         po_number="DFE-PO-2024-0044", date="2024-02-01", delivery_date="2024-02-20",
         currency="EUR", total=38200.00,
         items=[{"item_name":"Tulip Bulb Red 12cm/+ per 1000","quantity":50,"unit_price":280.00},
                {"item_name":"Gerbera Plug Young Plant tray/104","quantity":200,"unit_price":58.00},
                {"item_name":"Rose Cutting 10cm per 1000","quantity":30,"unit_price":420.00},
                {"item_name":"Chrysanthemum Liner 9cm pot","quantity":500,"unit_price":35.00}]),
    # 18 - USD single item
    dict(buyer="Quantum Data Centers Inc", supplier="Vertiv UPS Solutions",
         po_number="QDC-PO-2024-0088", date="2024-06-01", delivery_date="2024-07-01",
         currency="USD", total=240000.00,
         items=[{"item_name":"Liebert EXM2 UPS 800kVA","quantity":2,"unit_price":120000.00}]),
    # 19 - no delivery date, USD
    dict(buyer="OceanBlue Fishing Cooperative", supplier="Marine Gear International",
         po_number="OBF-2024-PO-0038", date="2024-04-05", delivery_date=None,
         currency="USD", total=61500.00,
         items=[{"item_name":"Monofilament Net 400m depth 18mm mesh","quantity":10,"unit_price":2800.00},
                {"item_name":"LED Underwater Fish Light 12V","quantity":30,"unit_price":380.00},
                {"item_name":"EPIRB Distress Beacon 406MHz","quantity":5,"unit_price":1500.00},
                {"item_name":"Life Raft 12-person SOLAS","quantity":3,"unit_price":4800.00},
                {"item_name":"Hydraulic Winch 5T Pull","quantity":2,"unit_price":5250.00}]),
    # 20 - INR, delivery date present
    dict(buyer="Indian Railways Procurement Div", supplier="BHEL Power Sector",
         po_number="IR-PO-2024-ELECT-0091", date="2024-01-20", delivery_date="2024-06-30",
         currency="INR", total=85000000.00,
         items=[{"item_name":"25kV AC Traction Transformer 10MVA","quantity":10,"unit_price":7500000.00},
                {"item_name":"Overhead Equipment Copper Wire 1km","quantity":200,"unit_price":50000.00}]),
    # 21 - EUR
    dict(buyer="EuroConstruct AG", supplier="Hilti Deutschland GmbH",
         po_number="EC-PO-2024-0334", date="2024-10-20", delivery_date="2024-11-05",
         currency="EUR", total=21840.00,
         items=[{"item_name":"Rotary Hammer Drill TE 70 ATC","quantity":12,"unit_price":780.00},
                {"item_name":"Diamond Core Bit 82mm 450mm","quantity":30,"unit_price":220.00},
                {"item_name":"Chemical Anchor HIT-RE 500 V3 500ml","quantity":60,"unit_price":68.00},
                {"item_name":"Safety Anchor Eye Bolt M12","quantity":200,"unit_price":18.00}]),
    # 22 - GBP no delivery_date
    dict(buyer="Harrods Ltd", supplier="Fine Spirits Imports Ltd",
         po_number="HAR-PO-2024-0201", date="2024-12-01", delivery_date=None,
         currency="GBP", total=43200.00,
         items=[{"item_name":"Single Malt Scotch 18yr 700ml","quantity":120,"unit_price":145.00},
                {"item_name":"Champagne Grand Cru Brut 750ml","quantity":200,"unit_price":88.00},
                {"item_name":"Cognac XO 700ml","quantity":80,"unit_price":165.00}]),
    # 23 - USD small PO
    dict(buyer="Creative Agency Network", supplier="Adobe Systems Inc",
         po_number="CAN-PO-2024-SW-009", date="2024-11-15", delivery_date=None,
         currency="USD", total=14988.00,
         items=[{"item_name":"Adobe Creative Cloud All Apps Annual","quantity":12,"unit_price":1249.00}]),
    # 24 - INR three items
    dict(buyer="Varun Beverages Ltd", supplier="Crown Holdings India",
         po_number="VBL/PO/2024/5512", date="2024-06-01", delivery_date="2024-06-30",
         currency="INR", total=28750000.00,
         items=[{"item_name":"Aluminum Can 250ml Sleek per 1000","quantity":5000,"unit_price":3800.00},
                {"item_name":"Aluminum Can 330ml per 1000","quantity":3000,"unit_price":4200.00},
                {"item_name":"Lid B64 per 1000","quantity":8000,"unit_price":650.00}]),
    # 25 - EUR single item
    dict(buyer="Airbus SAS", supplier="Safran Aircraft Engines",
         po_number="AIR-2024-ENG-0044", date="2024-05-01", delivery_date="2025-01-31",
         currency="EUR", total=80000000.00,
         items=[{"item_name":"CFM LEAP-1A Engine Unit","quantity":20,"unit_price":4000000.00}]),
    # 26 - USD
    dict(buyer="Metro City Council", supplier="Caterpillar Financial Products",
         po_number="MCC-PO-2024-INFRA-011", date="2024-08-01", delivery_date="2024-09-01",
         currency="USD", total=892000.00,
         items=[{"item_name":"Caterpillar 320 Excavator","quantity":2,"unit_price":245000.00},
                {"item_name":"Cat 140 Motor Grader","quantity":1,"unit_price":280000.00},
                {"item_name":"Vibratory Compactor CS56","quantity":2,"unit_price":61000.00}]),
    # 27 - GBP multi item
    dict(buyer="Aldgate Print Media Group", supplier="Verso Paper Corp",
         po_number="APM-PO-2024-0088", date="2024-03-15", delivery_date="2024-04-10",
         currency="GBP", total=67500.00,
         items=[{"item_name":"Coated Offset Paper 90gsm A4 500sht","quantity":500,"unit_price":28.00},
                {"item_name":"Newsprint Roll 42gsm 1200mm","quantity":50,"unit_price":420.00},
                {"item_name":"Gloss Art Paper 170gsm SRA3","quantity":200,"unit_price":95.00},
                {"item_name":"Cardboard Board 300gsm A3","quantity":300,"unit_price":42.00}]),
    # 28 - EUR no delivery date
    dict(buyer="Parisian Patisserie Group", supplier="Valrhona SA",
         po_number="PPG-PO-2024-003", date="2024-01-08", delivery_date=None,
         currency="EUR", total=31500.00,
         items=[{"item_name":"Valrhona Guanaja 70% Dark 3kg","quantity":150,"unit_price":95.00},
                {"item_name":"Valrhona Ivoire White Chocolate 3kg","quantity":100,"unit_price":78.00},
                {"item_name":"Cocoa Powder Extra Brute 1kg","quantity":200,"unit_price":18.00}]),
    # 29 - USD large multi-item
    dict(buyer="HorizonFarm Cooperative", supplier="John Deere Financial",
         po_number="HFC-PO-2024-AGRI-007", date="2024-02-15", delivery_date="2024-04-01",
         currency="USD", total=482000.00,
         items=[{"item_name":"John Deere 6R 155 Tractor","quantity":3,"unit_price":112000.00},
                {"item_name":"8-Row Corn Planter Precision","quantity":2,"unit_price":48000.00},
                {"item_name":"Grain Cart 1100bu","quantity":1,"unit_price":58000.00}]),
    # 30
    dict(buyer="Singapore Airlines Engineering", supplier="Honeywell Aerospace",
         po_number="SIAEC-PO-2024-0071", date="2024-09-10", delivery_date="2024-12-01",
         currency="USD", total=3240000.00,
         items=[{"item_name":"APU GTCP131-9B Overhaul","quantity":6,"unit_price":220000.00},
                {"item_name":"Avionics LRU Replacement Kit","quantity":12,"unit_price":145000.00},
                {"item_name":"Cabin Air Recirculation Fan","quantity":30,"unit_price":8800.00}]),
]

# ── Assemble JSONL ────────────────────────────────────────────────────────────

def invoice_to_jsonl(inv):
    raw = make_invoice_text(
        inv["vendor"], inv["invoice_number"], inv["date"], inv["due_date"],
        inv["currency"], inv["subtotal"], inv["tax"], inv["total"], inv["line_items"]
    )
    out = {
        "vendor": inv["vendor"],
        "invoice_number": inv["invoice_number"],
        "date": inv["date"],
        "due_date": inv["due_date"],
        "currency": inv["currency"],
        "subtotal": inv["subtotal"],
        "tax": inv["tax"],
        "total": inv["total"],
        "line_items": inv["line_items"],
    }
    return {"instruction": INSTRUCTION_INVOICE, "input": raw, "output": json.dumps(out)}

def po_to_jsonl(po):
    raw = make_po_text(
        po["buyer"], po["supplier"], po["po_number"], po["date"], po["delivery_date"],
        po["currency"], po["total"], po["items"]
    )
    out = {
        "buyer": po["buyer"],
        "supplier": po["supplier"],
        "po_number": po["po_number"],
        "date": po["date"],
        "delivery_date": po["delivery_date"],
        "currency": po["currency"],
        "total": po["total"],
        "items": po["items"],
    }
    return {"instruction": INSTRUCTION_PO, "input": raw, "output": json.dumps(out)}

def main():
    out_path = os.path.join("data", "curated_train.jsonl")
    os.makedirs("data", exist_ok=True)
    rows = []
    for inv in INVOICES:
        rows.append(invoice_to_jsonl(inv))
    for po in PURCHASE_ORDERS:
        rows.append(po_to_jsonl(po))
    random.seed(42)
    random.shuffle(rows)
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Written {len(rows)} examples to {out_path}")
    # Verify all lines are valid JSON
    errors = 0
    with open(out_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                obj = json.loads(line)
                assert "instruction" in obj and "input" in obj and "output" in obj
                json.loads(obj["output"])  # output must itself be valid JSON
            except Exception as e:
                print(f"  ERROR line {i+1}: {e}")
                errors += 1
    print(f"Validation complete. Errors: {errors}")

if __name__ == "__main__":
    main()
