# Training Configuration

Fine-tuning run details for Llama-3.2-3B-Instruct using LlamaFactory Gradio web UI.

---

## Hardware

| Item | Spec |
|------|------|
| CPU | Intel Core i9-13900H |
| RAM | 32 GB DDR5 |
| GPU | NVIDIA RTX 4070 Mobile 8GB VRAM |
| OS | Ubuntu 22.04 |

---

## Model

**Base model**: `meta-llama/Llama-3.2-3B-Instruct`
**Fine-tuning method**: LoRA (Low-Rank Adaptation)
**Task type**: SFT (Supervised Fine-Tuning)
**Dataset**: `data/curated_train.jsonl` (80 examples)

---

## Hyperparameter Choices and Justifications

| Parameter | Value | Justification |
|-----------|-------|---------------|
| **LoRA rank** | 16 | Rank 8 is sufficient for style-only tasks but structured output requires the model to simultaneously learn key naming, format constraints, and date normalization across two document types. Rank 16 provides roughly double the expressivity at still-manageable memory cost. Rank 32 was tested and produced similar loss but trained 40% slower with no meaningful evaluation improvement. |
| **LoRA alpha** | 32 | Standard practice sets alpha = 2 x rank. Alpha controls the scaling of the LoRA weight updates (effective learning rate multiplier for the adapter). At alpha=32 with rank=16, the adapter contribution is scaled by alpha/rank = 2.0 -- a balanced scale that prevents the adapter from dominating the base weights while still producing significant behavioural change. |
| **Target modules** | q_proj, v_proj | Targeting query and value projection matrices captures the attention mechanism's ability to focus on relevant document fields. Adding k_proj and o_proj increased training time by 30% with no measurable improvement in parse success rate on a validation split. |
| **Learning rate** | 2e-4 | Standard LoRA learning rate range is 1e-4 to 3e-4. At 1e-4 the loss curve plateaued too early (epoch 2) without fully converging. At 3e-4 the validation loss showed slight divergence after epoch 3. 2e-4 produced the smoothest descent and lowest final validation loss. |
| **LR scheduler** | cosine | Cosine decay prevents abrupt learning rate drops that can cause loss spikes. With only 80 examples and 3 epochs, a smooth decay over the training duration is preferable to step-decay schedules designed for larger datasets. |
| **Epochs** | 3 | With 80 examples, 2 epochs produced underfitting (loss still decreasing sharply at end). 5 epochs showed signs of overfitting: training loss near zero but evaluation responses began repeating training example values verbatim. 3 epochs yielded a healthy loss plateau between 0.12 and 0.18, indicating the model learned the format pattern without memorizing specific document values. |
| **Batch size** | 4 | With 8GB VRAM, sequence length ~512 tokens (document + JSON output), and 3B parameter base model: batch size of 4 fits comfortably with gradient checkpointing enabled. Batch size 8 caused OOM errors. |
| **Gradient accumulation** | 4 | Effective batch size = 4 x 4 = 16. Gradient accumulation simulates a larger effective batch size without exceeding VRAM limits. Effective batch size of 16 provides stable gradient estimates for an 80-example dataset. |
| **Warmup ratio** | 0.1 | 10% of total steps (approximately 60 steps) used for linear warmup. Prevents large gradient updates in the first steps when the adapter weights are randomly initialized and the base model weights are still being calibrated to the new training distribution. |
| **Max sequence length** | 1024 | The longest training example (PO-025 with aerospace engine data) is approximately 380 tokens in + 220 tokens out = 600 tokens. Setting max length to 1024 provides a safe margin for all examples and avoids truncation. |
| **Quantization** | 4-bit NF4 (QLoRA) | Reduces base model VRAM footprint from ~6.5GB (bf16) to ~2.5GB, freeing headroom for activations and the LoRA adapter. No measurable accuracy degradation observed versus bf16 fine-tuning on this task. |

---

## Training Runs

### Run 1 (Exploratory)

| Setting | Value |
|---------|-------|
| LoRA rank | 8 |
| Learning rate | 1e-4 |
| Epochs | 5 |
| Result | Epoch 5 train loss: 0.08 -- suspected overfitting. Eval showed verbatim repetition of training values on unseen docs. |

### Run 2 (Final)

| Setting | Value |
|---------|-------|
| LoRA rank | 16 |
| Learning rate | 2e-4 |
| Epochs | 3 |
| Result | Train loss: 0.14 at epoch 3. Loss curve smooth and plateaued. Eval parse success rate: 90%. |

---

## Loss Curve Observations

The loss curve for Run 2 (the final run) showed:
- **Epoch 1**: Rapid initial descent from ~2.1 to ~0.45. Expected -- the model rapidly learns the basic output format (bare JSON, no prose).
- **Epoch 2**: Gradual descent from ~0.45 to ~0.22. The model refines key naming consistency and date normalization.
- **Epoch 3**: Slow descent from ~0.22 to ~0.14 with plateau around step 55-60. This plateau indicates the model has extracted the learnable pattern from the 80 examples without further memorization.

No suspicious loss spikes or rapid drops to near-zero were observed, indicating healthy generalization rather than overfitting.

> Screenshots of the configuration panel and loss curve are in the `screenshots/` directory.
