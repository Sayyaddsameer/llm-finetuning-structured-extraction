# Prompting vs Fine-Tuning Analysis

## Structured Output Reliability for Enterprise Document Extraction

This section analyzes when prompt engineering versus fine-tuning is the appropriate tool for improving structured output reliability in a production document extraction pipeline.

The experiment compared three progressively more engineered prompts against a LoRA fine-tuned model on the same set of difficult evaluation documents. The results reveal a clear pattern.

**Prompt engineering wins when**: the task is new, well-defined but narrow, and the stakes of occasional failure are low. Version 3, the few-shot prompt, achieved 100% parse success on the 3 test documents and required no training infrastructure, no data pipeline, and no GPU time. For a small internal team prototyping an invoice parser that runs a few times a day, a carefully engineered prompt can be entirely sufficient. The cost to iterate is low -- a new prompt version takes minutes, not hours. Prompt engineering also handles schema changes gracefully: update the example in the prompt, deploy immediately.

**Fine-tuning wins when**: reliability must hold across high document volume, diverse formats, and two or more document types simultaneously. The fine-tuned model achieved 90% parse success across all 20 evaluation documents using a 15-token instruction, compared to 100% for V3 on only the 3 documents it was designed for. When V3 is tested on German-locale documents or PO formats without a matching few-shot example, its performance degrades sharply -- the same failure modes return. Fine-tuning, by contrast, bakes the behaviour into the model weights, making it robust to phrasing variation, layout differences, and format diversity without per-call overhead.

**The production decision framework**: If your parsing volume exceeds 50,000 documents per month, the token overhead of a few-shot prompt (200-300 tokens per call vs. 15 tokens post-fine-tuning) translates to material inference cost at scale. If your pipeline processes two or more document types -- as this task does with invoices and purchase orders -- a single few-shot prompt becomes impractical: you need type-specific prompts, adding routing logic and maintenance burden. Fine-tuning consolidates this into a single model endpoint. The correct decision is: prototype fast with prompt engineering, validate the business case, then fine-tune once the schema is stable and volume justifies the training investment. The two approaches are not mutually exclusive -- fine-tuned models still benefit from clear, concise system instructions.
