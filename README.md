# InsightForge AI

**An Intelligent Data Analyst Copilot Using Generative AI and Advanced Prompt Engineering**

InsightForge AI is a modular academic Streamlit application. It combines working tabular question answering, charts, a prompt playground, document retrieval, a bounded tool agent, an evaluation page, and interactive lessons in model families, sequence learning, transformers, multimodal systems, and responsible AI.

## Quick start on Windows / VS Code

1. Install Python 3.10 or newer and open this folder in VS Code.
2. In the VS Code terminal, create and activate an isolated environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

   If PowerShell blocks activation, use `\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `\.venv\Scripts\python.exe -m streamlit run app.py` directly.
3. Start the app:

   ```powershell
   streamlit run app.py
   ```

4. Open the local URL printed by Streamlit, normally `http://localhost:8501`.

The app starts with `sample_data/sales_demo.csv`, which has 24 synthetic records. No hosted API key is required for the local deterministic analyst, lessons, charting, or TF-IDF RAG.

## Using your own files

You can upload files with the page's file picker, or copy them into the project folders below and select them in the app:

- `uploads/datasets/`: CSV, XLSX, or XLS files for the AI Data Analyst.
- `uploads/documents/`: PDF or TXT reference files for the RAG Document Assistant.

The `uploads/` contents are ignored by Git and stay on this computer. Dataset rows are loaded into the active app session; document chunks are kept in session memory. Remove files from these folders when you no longer need them.

## Optional Groq inference

Groq is used only when an API key is configured. Copy `.env.example` to `.env`, set `GROQ_API_KEY`, and restart Streamlit. `GROQ_MODEL` defaults to `openai/gpt-oss-20b`; the model ID is configurable because hosted model availability can change. Groq supports hosted text models and Whisper transcription; see [current model IDs](https://console.groq.com/docs/models) before changing the setting.

Hosted inference sends the selected prompt, retrieved context, or media to Groq. Do not submit private data unless you are authorized to share it. The data analyst always computes values locally; the LLM can propose an expression only when the local planner cannot handle a question, and it can verbalize a computed result without changing its numeric value.

## Optional deep learning / dense retrieval

The base install stays lightweight. For PyTorch model demonstrations, Hugging Face Transformers, Accelerate, and Sentence Transformers + FAISS dense vector retrieval:

```powershell
pip install -r requirements-ml.txt
```

The Transformers page, Prompt Engineering Playground, and AI Data Analyst can use `qwen2.5-coder:1.5b` through a local Ollama service. Install Ollama, run `ollama pull qwen2.5-coder:1.5b`, and keep Ollama running. The analyst only calls Qwen when you enable its checkbox and the local planner cannot answer. Generated dataframe expressions still pass through the project validator and isolated executor. The 7B Hugging Face model is also available in the Transformer page but needs substantially more RAM.

For video keyframe extraction and offline system text-to-speech, install the separate Windows multimedia extras with `pip install -r requirements-video.txt`.

The toy Autoencoder, VAE, GAN, DCGAN, and conditional GAN train on generated 8×8 shapes. They are educational toy models, not production-quality generators. CycleGAN is shown with an invertible toy transform to explain cycle consistency, not a trained GAN. StyleGAN is explained but not reproduced or supplied with pretrained weights. Dense retrieval downloads the Sentence Transformers model on first use.

## Features

- **Data Analyst:** CSV/XLSX upload, schema and quality profile, answer-type identification, type-filtered few-shot examples, local expression planning, AST allowlist, isolated worker, result validation, optional Groq correction/explanation, evidence, plots, and SQLite history.
- **Prompt Engineering:** Persona Pattern, Root Prompt, RGC, chain-of-thought summary request, Comparative Prompting, tone/style/length controls, context, injection heuristics, prompt comparison, and saved prompts. Generation requires the optional Groq API.
- **RAG:** PDF/TXT extraction, chunking and citations, TF-IDF retrieval by default, optional Sentence Transformers + FAISS retrieval, source snippets, and a grounded Groq answer when configured.
- **AI Agent:** visible plan and action log for explicit read-only tools; it cannot access the shell, network, arbitrary code, or change files.
- **Learning:** AI vs. generative AI, probability, HMM, Autoencoders/VAEs/GAN families, RNN/LSTM/BiLSTM/GRU/BiGRU, attention, transformers, pretraining, foundation models, and multimodal concepts.
- **Multimodal:** optional Groq Whisper audio transcription and image understanding, local system text-to-speech, and sparse-frame video summarization with optional OpenCV + Groq vision.
- **Evaluation:** fixed questions are executed against the included demo data. Exact match, execution success, answer-type accuracy, and response time are calculated from those runs. RAG relevance remains unreported until a labeled retrieval benchmark is supplied.
- **Responsible AI / Industry:** risk guidance, limitations, and illustrative cross-industry workflows.

## Safety and limits

The application accepts a single Python expression from a model, validates every AST node against an allowlist, then evaluates it in a separate short-lived worker with no builtins, a five-second timeout, and dataset caps (100,000 rows / 100 columns). The worker is a defense-in-depth boundary, not an OS-level memory sandbox. Do not use this demo with untrusted code or for high-impact decisions.

Only query text, answer text, expression, elapsed time, and success status are written to SQLite (`data/insightforge.sqlite3`); uploaded tables and document chunks are not persisted by the application. Use `.env` for API keys; never commit secrets.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```text
InsightForge_AI/
├── app.py                 # navigation and app bootstrap
├── pages/                 # 14 interface and learning modules
├── modules/               # data, RAG, agent, prompt, database and safety services
├── models/                # optional PyTorch demo architectures and toy training
├── sample_data/           # synthetic sales CSV
├── tests/                 # unittest suite
├── assets/                # dashboard styling
├── requirements.txt       # base dependencies
├── requirements-ml.txt    # optional ML and dense retrieval stack
├── .env.example
└── PROJECT_REPORT.md
```

## Research inspiration

The analysis stages are inspired by Gao, Chen, and Su's [I2R-NLP at SemEval-2025 Task 8](https://aclanthology.org/2025.semeval-1.14/): answer-type identification, metadata-aware prompting, type-filtered examples, Pandas function generation, and iterative error correction. Their reported scores apply to the SemEval benchmark and their model setup. InsightForge reports its own small demo evaluation separately and does not claim to reproduce the paper's scores.
