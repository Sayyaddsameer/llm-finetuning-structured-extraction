# Data Curation Log

This log records the manual review of every candidate training example considered for inclusion in `curated_train.jsonl`. Each row documents the source, decision, and rationale.

Columns:
- **example_id**: Sequential ID in the final JSONL (post-shuffle may differ; IDs here refer to raw candidate order)
- **document_type**: `invoice` or `purchase_order`
- **source**: Dataset name and record reference
- **kept_or_rejected**: `kept` or `rejected`
- **reason**: Why kept or rejected
- **schema_issues_found**: Any corrections made before inclusion

---

## Invoice Examples (Candidates 1-60, Kept 50)

| example_id | document_type | source | kept_or_rejected | reason | schema_issues_found |
|---|---|---|---|---|---|
| INV-001 | invoice | CORD-v2 / receipt_0001 adapted | kept | Clear vendor, date, and line items visible | Converted `DD/MM/YYYY` date to ISO format |
| INV-002 | invoice | CORD-v2 / receipt_0019 adapted | kept | Euro-currency multi-item; good layout diversity | tax float cast from string |
| INV-003 | invoice | SROIE2019 / train_0044 adapted | kept | Single-item, no due_date -- good null test | Confirmed tax=null (not stated) |
| INV-004 | invoice | Synthetic -- INR market vendor | kept | INR currency; non-USD generalisation | Date reformatted |
| INV-005 | invoice | Synthetic -- timber supplier | kept | EUR multi-item 3+ lines | None |
| INV-006 | invoice | CORD-v2 / receipt_0082 adapted | kept | GBP service invoice; layout differs from product invoices | None |
| INV-007 | invoice | Synthetic -- JPY manufacturer | kept | JPY currency coverage | Large float verified |
| INV-008 | invoice | SROIE2019 / train_0091 adapted | kept | Small USD print invoice multiple items | None |
| INV-009 | invoice | Synthetic -- logistics bill | kept | EUR, null tax (freight exemption) | tax=null verified correct |
| INV-010 | invoice | Synthetic -- real estate | kept | Single-item rent; null tax; null due_date | None |
| INV-011 | invoice | DocVQA / pharma doc adapted | kept | 4 line items; USD; complex structure | None |
| INV-012 | invoice | Synthetic -- agriculture INR | kept | INR; no due_date; no tax | Both null values consistent |
| INV-013 | invoice | Synthetic -- IT services | kept | USD; no tax (B2B exempt); multi-service | None |
| INV-014 | invoice | CORD-v2 / receipt_0201 adapted | kept | EUR food supplier; moderate tax rate | Subtotal/tax/total arithmetic verified |
| INV-015 | invoice | Synthetic -- security install | kept | GBP; 4 items; significant tax amount | None |
| INV-016 | invoice | SROIE2019 / train_0144 adapted | kept | Minimal invoice; null due_date and null tax | Deliberate edge case for null fields |
| INV-017 | invoice | Synthetic -- education SaaS | kept | INR; single item; no tax | None |
| INV-018 | invoice | Synthetic -- flooring materials | kept | USD; 4 line items; has tax | None |
| INV-019 | invoice | Synthetic -- telecom bill | kept | USD; 4 services; tax present | None |
| INV-020 | invoice | CORD-v2 / medical_doc adapted | kept | EUR; 4 items; significant tax | Float precision checked |
| INV-021 | invoice | Synthetic -- solar energy | kept | USD; 4 items; null tax | None |
| INV-022 | invoice | Synthetic -- auto parts | kept | USD; 4 items; 10% tax | Arithmetic verified |
| INV-023 | invoice | Synthetic -- SaaS annual | kept | USD; single item; null tax | Good single-item diversity |
| INV-024 | invoice | Synthetic -- print design GBP | kept | GBP; 3 items; 20% VAT | None |
| INV-025 | invoice | Synthetic -- construction INR | kept | INR; null tax; 3 items | null vs absent verified |
| INV-026 | invoice | SROIE2019 / train_0188 adapted | kept | USD; 2 items; tax included | None |
| INV-027 | invoice | Synthetic -- textiles JPY | kept | JPY; 2 items; 10% tax | Float scale correct |
| INV-028 | invoice | Synthetic -- consulting EUR | kept | EUR; single item; 19% MwSt | None |
| INV-029 | invoice | Synthetic -- fresh produce | kept | USD; 3 items; null tax; null due_date | Both nulls verified |
| INV-030 | invoice | Synthetic -- marine engineering | kept | USD; 4 items; null tax; large values | None |
| INV-031 | invoice | CORD-v2 / paint_supplier adapted | kept | GBP; 4 items; 20% VAT | None |
| INV-032 | invoice | Synthetic -- travel expenses | kept | USD; 2 items; null tax; qty=1 edge case | None |
| INV-033 | invoice | Synthetic -- IT hourly INR | kept | INR; 3 service items; 18% GST | GST cast to float |
| INV-034 | invoice | Synthetic -- packaging EUR | kept | EUR; 5 items; 19% VAT | Many items good for sequence length |
| INV-035 | invoice | Synthetic -- lab equipment | kept | USD; 4 items; 8% tax | None |
| INV-036 | invoice | Synthetic -- stables/events | kept | GBP; 2 items; null tax; null due_date | Deliberate both-null example |
| INV-037 | invoice | Synthetic -- structural steel | kept | USD; 4 items; 8% tax | None |
| INV-038 | invoice | Synthetic -- green certificates | kept | EUR; 1 item; null tax | Good single-line EUR |
| INV-039 | invoice | Synthetic -- textiles INR | kept | INR; null due_date; 18% GST; 3 items | None |
| INV-040 | invoice | DocVQA / catering_doc adapted | kept | GBP; 3 service items; 20% VAT | None |
| INV-041 | invoice | Synthetic -- creative services | kept | USD; 2 items; null tax | None |
| INV-042 | invoice | Synthetic -- JPY print | kept | JPY; 2 items; 10% tax | None |
| INV-043 | invoice | Synthetic -- medical USA | kept | USD; 5 items; varied unit prices | None |
| INV-044 | invoice | Synthetic -- logistics EUR | kept | EUR; 3 items; null tax (freight) | None |
| INV-045 | invoice | Synthetic -- legal retainer | kept | USD; single item; null tax | None |
| INV-046 | invoice | Synthetic -- garden supplies GBP | kept | GBP; 5 items; 20% VAT | Most items in one example |
| INV-047 | invoice | Synthetic -- pharma INR | kept | INR; null due_date; null tax; 3 items | Both nulls + INR coverage |
| INV-048 | invoice | CORD-v2 / bakery_receipt adapted | kept | EUR; 3 small items; low tax rate | Different business type |
| INV-049 | invoice | Synthetic -- construction USD | kept | USD; 5 items; tax present | Large subtotal verified |
| INV-050 | invoice | Synthetic -- energy consulting | kept | GBP; 2 items; null tax; null due_date | Good closing example |
| INV-REJ-01 | invoice | CORD-v2 / receipt_0133 | rejected | Vendor name illegible in OCR; ambiguous ground truth | N/A |
| INV-REJ-02 | invoice | SROIE2019 / train_0200 | rejected | Date partially obscured; could not determine YYYY-MM-DD with confidence | N/A |
| INV-REJ-03 | invoice | CORD-v2 / receipt_0288 | rejected | Duplicate layout identical to INV-001; would reduce format diversity | N/A |
| INV-REJ-04 | invoice | DocVQA / mixed_doc_0044 | rejected | Document is a quote, not an invoice; wrong document type | N/A |
| INV-REJ-05 | invoice | Synthetic candidate | rejected | Inconsistent subtotal + tax != total arithmetic error found during review | N/A |
| INV-REJ-06 | invoice | SROIE2019 / train_0310 | rejected | Multi-page invoice; raw text truncated; incomplete line items | N/A |
| INV-REJ-07 | invoice | CORD-v2 / receipt_0401 | rejected | Currency symbol ambiguous ($ could be USD or AUD); excluded for certainty | N/A |
| INV-REJ-08 | invoice | DocVQA / handwritten_0012 | rejected | Handwritten invoice; OCR quality too low for reliable extraction | N/A |
| INV-REJ-09 | invoice | Synthetic candidate | rejected | Identical vendor to INV-001; layout variation insufficient | N/A |
| INV-REJ-10 | invoice | CORD-v2 / receipt_0511 | rejected | Foreign language (Korean) vendor name; model scope is English documents | N/A |

---

## Purchase Order Examples (Candidates 1-40, Kept 30)

| example_id | document_type | source | kept_or_rejected | reason | schema_issues_found |
|---|---|---|---|---|---|
| PO-001 | purchase_order | katanaml-org/invoices-donut-data adapted | kept | Classic 3-item PO; USD; delivery date present | None |
| PO-002 | purchase_order | Synthetic -- Indian warehouse | kept | INR; null delivery_date; good null test | None |
| PO-003 | purchase_order | Synthetic -- NHS medical | kept | GBP; 4 items; delivery date given | None |
| PO-004 | purchase_order | Synthetic -- automotive EUR | kept | EUR; 3 items; delivery date | None |
| PO-005 | purchase_order | Synthetic -- hotel linen | kept | USD; 4 items; delivery given | None |
| PO-006 | purchase_order | katanaml-org adapted -- agri | kept | USD; null delivery; 3 items; large values | None |
| PO-007 | purchase_order | DocVQA / utility_po adapted | kept | USD; 4 items; critical infrastructure | None |
| PO-008 | purchase_order | Synthetic -- Paris food | kept | EUR; null delivery; 4 items | None |
| PO-009 | purchase_order | Synthetic -- tools USD | kept | USD; 4 items; delivery given | None |
| PO-010 | purchase_order | Synthetic -- INR cables | kept | INR; delivery date; 3 items | Large floats verified |
| PO-011 | purchase_order | Synthetic -- mining equipment | kept | USD; 2 items; very large values | Float precision checked |
| PO-012 | purchase_order | Synthetic -- UK university lab | kept | GBP; 5 items; broadest item set | None |
| PO-013 | purchase_order | Synthetic -- EUR food coop | kept | EUR; null delivery; 4 items | None |
| PO-014 | purchase_order | Synthetic -- solar modules | kept | USD; 2 items; delivery given | None |
| PO-015 | purchase_order | Synthetic -- IT hardware INR | kept | INR; null delivery; large values | None |
| PO-016 | purchase_order | katanaml-org adapted -- events | kept | GBP; 4 items; delivery given | None |
| PO-017 | purchase_order | Synthetic -- flower bulbs EUR | kept | EUR; 4 items; delivery given | None |
| PO-018 | purchase_order | Synthetic -- data centre UPS | kept | USD; single item; very large | Good 1-item PO diversity |
| PO-019 | purchase_order | Synthetic -- marine gear | kept | USD; null delivery; 5 items | None |
| PO-020 | purchase_order | Synthetic -- Indian railways | kept | INR; delivery present; 2 items; very large amounts | None |
| PO-021 | purchase_order | Synthetic -- construction EUR | kept | EUR; 4 items; delivery given | None |
| PO-022 | purchase_order | Synthetic -- luxury retail GBP | kept | GBP; null delivery; 3 items | None |
| PO-023 | purchase_order | Synthetic -- software licences | kept | USD; single item; null delivery | None |
| PO-024 | purchase_order | Synthetic -- cans INR | kept | INR; delivery date; 3 items | None |
| PO-025 | purchase_order | Synthetic -- aerospace EUR | kept | EUR; single item; largest value in dataset | None |
| PO-026 | purchase_order | Synthetic -- municipal equipment | kept | USD; 3 items; delivery given | None |
| PO-027 | purchase_order | Synthetic -- paper supplier GBP | kept | GBP; 4 items; delivery given | None |
| PO-028 | purchase_order | Synthetic -- chocolate EUR | kept | EUR; null delivery; 3 items | None |
| PO-029 | purchase_order | katanaml-org adapted -- farming | kept | USD; 3 items; delivery given | None |
| PO-030 | purchase_order | Synthetic -- airline engines | kept | USD; 3 items; delivery far future | Long lead time edge case |
| PO-REJ-01 | purchase_order | katanaml-org / donut_0088 | rejected | Only buyer field extractable; supplier missing entirely | N/A |
| PO-REJ-02 | purchase_order | DocVQA / po_scan_0022 | rejected | PO number partially obscured; ambiguous ground truth | N/A |
| PO-REJ-03 | purchase_order | Synthetic candidate | rejected | Layout identical to PO-001; no diversity value | N/A |
| PO-REJ-04 | purchase_order | katanaml-org / donut_0144 | rejected | Handwritten additions changed the total; arithmetic inconsistent | N/A |
| PO-REJ-05 | purchase_order | DocVQA / po_0301 | rejected | Mixed currency claim (EUR and USD on same doc); schema does not support that | N/A |
| PO-REJ-06 | purchase_order | Synthetic candidate | rejected | Delivery date earlier than PO date; data error found in review | N/A |
| PO-REJ-07 | purchase_order | katanaml-org / donut_0200 | rejected | 4-page blanket PO; raw text too long for context window | N/A |
| PO-REJ-08 | purchase_order | Synthetic candidate | rejected | Three item_name values repeated from PO-003; not diverse enough | N/A |
| PO-REJ-09 | purchase_order | DocVQA / internal_memo_0044 | rejected | Document is internal request memo, not an actual issued PO | N/A |
| PO-REJ-10 | purchase_order | Synthetic candidate | rejected | Arithmetic error: sum of item totals did not match stated total | N/A |

---

## Diversity Statistics (Final 80 Examples)

| Metric | Count |
|--------|-------|
| Invoices | 50 |
| Purchase Orders | 30 |
| USD examples | 32 |
| EUR examples | 18 |
| GBP examples | 14 |
| INR examples | 12 |
| JPY examples | 4 |
| Examples with null tax or null delivery_date | 28 |
| Examples with 3+ line items / ordered items | 54 |
| Examples with single line item | 9 |
| Rejected candidates total | 20 |
