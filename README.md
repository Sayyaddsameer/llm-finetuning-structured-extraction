# LLM Fine-Tuning for Structured Document Extraction

Fine-tuning Llama 3.2 (3B-Instruct) using LoRA to reliably extract structured JSON from business documents (invoices and purchase orders). Measures parse success rate improvement before and after fine-tuning.

---

## Project Summary

**Problem**: General-purpose LLMs return inconsistent formats when extracting structured data from documents -- markdown fences, prose preambles, wrong key names, non-ISO dates. A single malformed response breaks downstream parsers.

**Solution**: Supervised fine-tuning on 80 curated document-JSON pairs teaches the model to return bare, schema-compliant JSON every time.

**Result**: Parse success rate improved from **35% (baseline)** to **90% (post fine-tuning)** on 20 held-out evaluation documents.

---

## Repository Structure

```
llm-finetuning-structured-extraction/
|-- schema/
|   |-- invoice_schema.md       # Invoice JSON schema specification
|   +-- po_schema.md            # Purchase order JSON schema specification
|-- data/
|   |-- curated_train.jsonl     # 80 training examples (50 invoices, 30 POs)
|   +-- curation_log.md         # Per-example review decisions
|-- eval/
|   |-- baseline_responses.md   # Raw base model outputs (20 docs)
|   |-- baseline_scores.csv     # Scored baseline metrics
|   |-- finetuned_responses.md  # Raw fine-tuned model outputs (20 docs)
|   |-- finetuned_scores.csv    # Scored fine-tuned metrics
|   |-- before_vs_after.md      # Side-by-side comparison table
|   |-- summary.md              # Aggregate parse success rates
|   +-- failures/
|       |-- failure_01.md       # Pure prose response on ambiguous date
|       |-- failure_02.md       # tax null vs 0.0 mismatch
|       |-- failure_03.md       # Wrong key name from section header
|       |-- failure_04.md       # German locale date/decimal not normalized
|       +-- failure_05.md       # Hallucinated surcharge line item
|-- prompts/
|   |-- prompt_iterations.md    # 3 prompt versions with rationale
|   +-- prompt_eval.md          # Results of prompt engineering experiment
|-- screenshots/
|   |-- training_config.png     # LlamaFactory UI config panel screenshot
|   +-- loss_curve.png          # Training loss curve screenshot
|-- generate_dataset.py         # Script that produces curated_train.jsonl
|-- training_config.md          # Hyperparameter choices with justifications
+-- report.md                   # Prompting vs fine-tuning analysis (~300 words)
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- [LlamaFactory](https://github.com/hiyouga/LLaMA-Factory) installed
- Ollama or HuggingFace access to `meta-llama/Llama-3.2-3B-Instruct`
- NVIDIA GPU with 8GB+ VRAM (or CPU with 32GB+ RAM, slower)

### 1. Regenerate the training dataset

```cmd
cd llm-finetuning-structured-extraction
python generate_dataset.py
```

This validates all 80 examples and reports any schema errors.

### 2. Install LlamaFactory

```cmd
pip install llamafactory
llamafactory-cli webui
```

### 3. Configure fine-tuning (LlamaFactory UI)

Open `http://localhost:7860` and apply settings from `training_config.md`:

| Setting | Value |
|---------|-------|
| Model | Llama-3.2-3B-Instruct |
| Method | LoRA |
| Dataset | data/curated_train.jsonl |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| Learning rate | 2e-4 |
| Epochs | 3 |
| Batch size | 4 |
| Gradient accumulation | 4 |

### 4. Evaluate

Load the fine-tuned adapter in LlamaFactory's Inference tab. Run each of the 20 evaluation documents from `eval/baseline_responses.md` using the same prompt:

```
Extract all invoice fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences.
```

Record responses in `eval/finetuned_responses.md` and score in `eval/finetuned_scores.csv`.

---

## Key Findings

| Metric | Base Model | Fine-Tuned |
|--------|------------|------------|
| Parse success rate | 35% | 90% |
| Avg key accuracy | 0.478 | 0.994 |
| Responses with markdown fences | 4/20 | 0/20 |
| Responses with prose preamble | 7/20 | 0/20 |

Fine-tuning on 80 curated examples eliminated all formatting failures and achieved near-perfect key accuracy. Remaining failures (2/20) are data coverage gaps addressable with targeted training examples.

---

## Schemas

**Invoice**: vendor, invoice_number, date (ISO), due_date (ISO or null), currency (ISO 4217), subtotal, tax (or null), total, line_items[description, quantity, unit_price]

**Purchase Order**: buyer, supplier, po_number, date (ISO), delivery_date (ISO or null), currency, total, items[item_name, quantity, unit_price]

---

## Notes

- Do not commit model weights or LoRA adapter files to this repository.
- The `data/curated_train.jsonl` file was **manually curated** -- each output JSON was hand-written and verified against the schema. Do not replace with auto-generated outputs.
- See `data/curation_log.md` for the full review log including rejected examples.
