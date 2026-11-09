from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET

ROOT = Path(r"C:\Users\hp\OneDrive - RV University\Documents\GEN AI project")
OUT = ROOT / "InsightForge_AI" / "InsightForge_AI_Demo_Presentation.pptx"
EMU = 9525  # 96 px per inch
W, H = 1280, 720
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}
for prefix, uri in NS.items():
    if prefix not in {"rel", "ct"}:
        ET.register_namespace(prefix, uri)
ET.register_namespace("", NS["ct"])
P, A, R = ("{" + NS[k] + "}" for k in ("p", "a", "r"))

NAVY = "12233F"
INK = "19283F"
TEAL = "0D8F89"
MINT = "DDF3EF"
GOLD = "F0B34D"
WHITE = "FFFFFF"
PALE = "F5F8FB"
MID = "5C6B80"
RULE = "DAE2EA"


def px(v: float) -> int:
    return int(round(v * EMU))


def el(parent, tag, attrs=None, text=None):
    node = ET.SubElement(parent, tag, attrs or {})
    if text is not None:
        node.text = text
    return node


def solid(parent, color):
    sf = el(parent, A + "solidFill")
    el(sf, A + "srgbClr", {"val": color})


def add_shape(sp_tree, sid, name, x, y, w, h, fill=None, geom="rect", line=None):
    sp = el(sp_tree, P + "sp")
    nv = el(sp, P + "nvSpPr")
    el(nv, P + "cNvPr", {"id": str(sid), "name": name})
    el(nv, P + "cNvSpPr")
    el(nv, P + "nvPr")
    pr = el(sp, P + "spPr")
    xf = el(pr, A + "xfrm")
    el(xf, A + "off", {"x": str(px(x)), "y": str(px(y))})
    el(xf, A + "ext", {"cx": str(px(w)), "cy": str(px(h))})
    pg = el(pr, A + "prstGeom", {"prst": geom})
    el(pg, A + "avLst")
    if fill:
        solid(pr, fill)
    else:
        el(pr, A + "noFill")
    ln = el(pr, A + "ln", {"w": str(px(1.2))})
    if line:
        solid(ln, line)
    else:
        el(ln, A + "noFill")
    return sp


def add_text(sp_tree, sid, name, x, y, w, h, text, size=19, color=INK,
             bold=False, font="Aptos", align="l", valign="t", margin=0,
             fill=None, line=None):
    sp = add_shape(sp_tree, sid, name, x, y, w, h, fill, "rect", line)
    nv = sp.find(P + "nvSpPr")
    nv.find(P + "cNvSpPr").set("txBox", "1")
    tx = el(sp, P + "txBody")
    body = el(tx, A + "bodyPr", {"wrap": "square", "anchor": valign,
                                  "lIns": str(px(margin)), "rIns": str(px(margin)),
                                  "tIns": str(px(margin)), "bIns": str(px(margin))})
    el(tx, A + "lstStyle")
    for i, line_text in enumerate(str(text).split("\n")):
        para = el(tx, A + "p")
        el(para, A + "pPr", {"algn": align})
        run = el(para, A + "r")
        rp = el(run, A + "rPr", {"lang": "en-US", "sz": str(int(size * 100)),
                                   "b": "1" if bold else "0", "dirty": "0"})
        solid(rp, color)
        el(rp, A + "latin", {"typeface": font})
        el(rp, A + "ea", {"typeface": font})
        el(rp, A + "cs", {"typeface": font})
        txt = el(run, A + "t")
        if line_text.startswith(" ") or line_text.endswith(" "):
            txt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        txt.text = line_text
        end = el(para, A + "endParaRPr", {"lang": "en-US", "sz": str(int(size * 100))})
        solid(end, color)
    return sp


def add_line(sp_tree, sid, name, x1, y1, x2, y2, color=RULE, width=1.5):
    shape = el(sp_tree, P + "sp")
    nv = el(shape, P + "nvSpPr")
    el(nv, P + "cNvPr", {"id": str(sid), "name": name})
    el(nv, P + "cNvSpPr")
    el(nv, P + "nvPr")
    pr = el(shape, P + "spPr")
    xf = el(pr, A + "xfrm")
    el(xf, A + "off", {"x": str(px(min(x1, x2))), "y": str(px(min(y1, y2)))})
    el(xf, A + "ext", {"cx": str(px(max(1, abs(x2 - x1)))), "cy": str(px(max(1, abs(y2 - y1))))})
    pg = el(pr, A + "prstGeom", {"prst": "line"})
    el(pg, A + "avLst")
    ln = el(pr, A + "ln", {"w": str(px(width))})
    solid(ln, color)
    return shape


slides = []


def cover():
    slides.append({"kind": "cover", "title": "InsightForge AI",
        "subtitle": "An Intelligent Data Analyst Copilot",
        "text": "Using Generative AI and Advanced Prompt Engineering\nProject presentation | Demonstration-ready walkthrough",
        "notes": "Introduce the project as a Streamlit learning application and working data-analysis copilot. It combines exact local calculations with optional language models, while showing evidence and the calculation path.",
    })


def intro(title, kicker, left_head, left, right_head, right, bottom, notes=""):
    slides.append({"kind": "two", "title": title, "kicker": kicker,
        "left_head": left_head, "left": left,
        "right_head": right_head, "right": right,
        "bottom": bottom, "notes": notes})


cover()
intro("Introduction", "PROJECT OVERVIEW", "WHAT IS GENERATIVE AI?",
      "AI systems perform tasks such as prediction, perception, and reasoning. Generative AI learns patterns from data and creates new content, including text, images, audio, or code.",
      "WHAT IS INSIGHTFORGE?",
      "A Streamlit copilot that lets a user upload a CSV or Excel table, ask questions in plain language, and inspect the calculated answer, evidence, and chart.",
      "The project connects classroom topics—models, prompting, RAG, agents, multimodal AI, and responsible use—to a hands-on analyst workflow.",
      "Explain the difference between AI and Generative AI in plain terms. InsightForge's main task is practical: make a table easier to inspect and query without requiring the user to write pandas code.")
intro("Problem statement", "WHY THIS PROJECT EXISTS", "THE USER PROBLEM",
      "Many students and small teams have useful tabular data but lack SQL or Python skills. Manual filtering and charting takes time and can introduce mistakes.",
      "THE TRUST PROBLEM",
      "A free-form AI answer can sound confident while inventing a number. Users need to see which data was analyzed and how a numeric answer was computed.",
      "Problem: create an approachable data-analysis assistant that answers supported questions from uploaded tables and makes its calculation path reviewable.",
      "State the gap as both usability and trust. Natural language reduces the coding barrier; evidence and calculation details reduce blind reliance on generated prose.")
intro("Project objectives and scope", "WHAT THE DEMO SETS OUT TO DO", "CORE OBJECTIVES",
      "• Load CSV and Excel data\n• Profile rows, columns, missing cells, and types\n• Answer common questions with local calculations\n• Show evidence, charts, and query history",
      "LEARNING OBJECTIVES",
      "• Explain model families and Transformers\n• Practice prompt patterns\n• Demonstrate document retrieval and bounded tools\n• Discuss evaluation and responsible AI",
      "The local analyst is the dependable core. Qwen runs locally through Ollama for broader language coverage; Groq features are optional and require a private API key.",
      "Describe the project boundary. The lesson pages explain concepts, while the data analyst is the main interactive workflow. Hosted functions are opt-in and may send prompts or media to an external provider.")

slides.append({"kind":"flow", "title":"How the application works", "kicker":"END-TO-END ANALYSIS FLOW",
    "steps":[("01","Upload","CSV / Excel"),("02","Inspect","Schema + quality"),("03","Ask","Plain-language question"),("04","Plan","Local rules; optional Qwen"),("05","Validate","Safe expression + worker"),("06","Explain","Result + evidence + chart")],
    "bottom":"Numeric answers come from local dataframe calculations. The model proposes a plan only when enabled; the app validates the expression before execution.",
    "notes":"Walk from the user's file to the answer. Explain the separation of responsibilities: pandas calculates, a language model may interpret an unfamiliar question, and validation limits what code can execute."})

slides.append({"kind":"flow", "title":"Application architecture", "kicker":"COMPONENTS AND DATA FLOW",
    "steps":[("A","Interface","Streamlit pages"),("B","Data layer","Pandas + profiler"),("C","Analysis","Planner / Qwen"),("D","Safety","AST + worker"),("E","Output","Explanation + chart")],
    "bottom":"Local route: browser → local app → local calculation. Optional routes: Ollama Qwen stays on the machine; Groq is hosted and only used when configured.",
    "notes":"Clarify the technology choices: Streamlit provides a quick interactive UI; Pandas handles tables; Ollama provides a local quantized model; SQLite stores limited query history; charts are generated from the active dataframe. The agent and RAG are separate features, not silently mixed into table answers."})

intro("Fourteen pages, one project", "APPLICATION MAP", "LEARN AND EXPLORE",
      "01 Home Dashboard\n02 AI Fundamentals\n03 Generative Models\n04 Deep Learning Models\n05 Transformers and LLMs\n06 Prompt Engineering Playground\n07 AI Data Analyst",
      "RETRIEVE, APPLY, REVIEW",
      "08 RAG Document Assistant\n09 AI Agent\n10 Multimodal AI\n11 Responsible AI\n12 Industry Applications\n13 Project Evaluation\n14 About Project",
      "The menu separates learning content from working tools so a presenter can teach a concept, open the matching demo, and discuss its limits.",
      "Point to the full sidebar. The order begins with concepts, moves through model and prompt tools, then explores analysis, retrieval, agents, multimodal use, safety, evaluation, and references.")

intro("Page 01 · Home Dashboard", "PROJECT ENTRY POINT", "WHAT IT DOES",
      "Introduces InsightForge, previews the built-in synthetic sales table, and shows revenue by region. It summarizes the main project capabilities.",
      "WHY IT WORKS THIS WAY",
      "A small working example reduces setup friction. The visitor can see the kind of data and output before uploading a file.",
      "Use it to open the presentation and orient the teacher: the main deliverable is transparent question answering over tables.",
      "The homepage uses sample data, so the teacher can see a chart immediately. The data is explicitly labeled synthetic, not a business benchmark.")
intro("Page 02 · AI Fundamentals", "CONCEPTS BEFORE MODELS", "WHAT IT DOES",
      "Compares discriminative/predictive systems with generative models; reviews probability, softmax, and neural-network basics.",
      "WHY IT WORKS THIS WAY",
      "The project starts with the output goal: classify or estimate a known value versus model a distribution and create a sample. A small softmax control makes probability visible.",
      "Use it to connect course theory to the analyst: the analyst computes a statistic, while a language model can help interpret a question.",
      "The slider's probabilities are illustrative values, not actual trained-model predictions. Reinforce that a model's confidence does not prove truth.")
intro("Page 03 · Generative Models", "MODEL FAMILY EXPLORER", "WHAT IT DOES",
      "Covers the evolution from probability models to latent-variable models, GAN families, and foundation models. Includes HMM sampling and optional toy training.",
      "WHY IT WORKS THIS WAY",
      "Cards compare each model's architecture, working principle, applications, and limits. Tiny synthetic patterns make training mechanics visible without large datasets.",
      "Use it to discuss HMMs, Autoencoders, VAEs, GANs, DCGANs, conditional GANs, StyleGAN, and CycleGAN in one guided page.",
      "The HMM is a hand-set probabilistic illustration. The PyTorch demonstrations train on 8×8 toy patterns; they are not production generators. StyleGAN is explained, not trained here; CycleGAN is a cycle-consistency concept demonstration.")
intro("Page 04 · Deep Learning Models", "SEQUENCE LEARNING", "WHAT IT DOES",
      "Compares RNN, LSTM, BiLSTM, GRU, and BiGRU, then displays an illustrative attention heatmap for a short token sequence.",
      "WHY IT WORKS THIS WAY",
      "The model table makes memory, directionality, strengths, and trade-offs easy to compare. The heatmap shows how attention can weight one token against another.",
      "Use it to explain that the sequence-model implementations are runnable forward passes but intentionally untrained; the attention vectors are deterministic toy values.",
      "Avoid presenting the model outputs as predictive results. This page teaches architecture, sequence order, gating, bidirectional context, and attention cost.")
intro("Page 05 · Transformers and LLMs", "FOUNDATION MODELS AND INFERENCE", "WHAT IT DOES",
      "Explains attention, autoregressive generation, pretraining versus fine-tuning, foundation models, and multimodal systems. Offers optional Groq and local Qwen text demos.",
      "WHY IT WORKS THIS WAY",
      "The page separates conceptual learning from inference. The default Qwen2.5-Coder 1.5B route uses Ollama locally; hosted generation is visibly optional.",
      "Use it to show a real local model response. Large Hugging Face models need much more memory; local Qwen avoids loading the 7B weights into Transformers.",
      "The host uses Qwen 1.5B through Ollama. A hosted call sends the prompt to Groq only when configured. Explain pretraining as broad initial learning and fine-tuning as adaptation to a task or behavior.")
intro("Page 06 · Prompt Engineering Playground", "DESIGNING EFFECTIVE INSTRUCTIONS", "WHAT IT DOES",
      "Builds and previews prompts using Persona Pattern, Root Prompt, RGC (Role, Goal, Context, Constraints), chain-of-thought summary, or comparative prompting.",
      "WHY IT WORKS THIS WAY",
      "Persona, tone, style, length, background context, and output format are explicit controls. The user can compare prompt versions and save reusable prompts.",
      "Use it to demonstrate that prompt structure changes instructions—not model knowledge—and that quoted background is treated as untrusted input.",
      "The injection detector uses common phrase heuristics and cannot prove safety. The chain-of-thought option requests a concise reasoning summary only; it does not ask the model to reveal private internal reasoning.")

intro("Page 07 · AI Data Analyst", "THE MAIN PROJECT FEATURE", "WHAT IT DOES",
      "Accepts CSV/XLSX uploads or project files. Profiles the dataset, summarizes types and missingness, previews records, and asks natural-language questions.",
      "WHY IT WORKS THIS WAY",
      "A deterministic local planner handles common calculations first. Optional Qwen proposes an expression for broader questions; an AST allowlist and short-lived worker guard execution.",
      "Answers show the result, expression, dataset evidence, explanation path, and a relevant chart. Query history records the query outcome, not uploaded table rows.",
      "Show a count or total first, then a grouped comparison. If a question is unsupported, the page gives guidance or uses Qwen when the checkbox is enabled. The dataframe remains the source of numeric truth.")

intro("Page 07 · CSV question demonstration", "VERIFIED SAMPLE OUTPUT", "ASK IN PLAIN LANGUAGE",
      "“Which region has the highest revenue?”\n“Show total revenue by product.”\n“What is average revenue by region?”\n“How many missing values are there?”",
      "CALCULATED FROM THE SAMPLE",
      "Rows: 24\nTotal revenue: 4,633.50\nHighest region: East · 1,266.00\nNorth: 1,155.00 · West: 1,107.00\nSouth: 1,105.50 · Missing cells: 0",
      "These values come from the bundled synthetic sales CSV. Upload your own file to calculate from your data; always check column meaning and data quality.",
      "The sample figures were computed from sample_data/sales_demo.csv. The table contains 24 synthetic records. Results are examples to demonstrate the pipeline, not claims about a real business.")

intro("Page 08 · RAG Document Assistant", "RETRIEVAL-AUGMENTED GENERATION", "WHAT IT DOES",
      "Accepts PDF and TXT files, extracts text, splits it into overlapping chunks, retrieves relevant passages, and shows source snippets and page references.",
      "WHY IT WORKS THIS WAY",
      "TF-IDF retrieval runs locally with a light setup. Optional Sentence Transformers plus FAISS can support dense semantic retrieval when installed.",
      "Use it to ground answers in uploaded reference documents. Retrieved text is evidence to inspect—not a new instruction or a guaranteed correct answer.",
      "Explain RAG as retrieval followed by a grounded response. In this project, retrieval works locally; final natural-language generation may depend on the configured provider. Citations let the user inspect the source.")
intro("Page 09 · AI Agent", "BOUNDED TOOL USE", "WHAT IT DOES",
      "Plans a task, selects named read-only tools, runs the constrained analyst, then displays the plan, permissions, completed actions, result, and chart.",
      "WHY IT WORKS THIS WAY",
      "The agent exposes only a small set of tools for summary, statistics, grouping, charting, and document retrieval. Every tabular calculation passes through the same validated analyst path.",
      "Use it to demonstrate visible planning and tool use without granting shell, network, filesystem, arbitrary Python, or mutation access.",
      "This is a bounded educational agent, not an autonomous computer user. It does not silently combine document retrieval with table analysis.")
intro("Page 10 · Multimodal AI", "TEXT, AUDIO, IMAGE, AND VIDEO", "WHAT IT DOES",
      "Shows text prompting, audio transcription, offline text-to-speech, image questions, and sparse video keyframe summaries.",
      "WHY IT WORKS THIS WAY",
      "Capabilities appear in separate tabs with explicit dependency and provider status. Video samples at most five frames and summarizes timestamped image captions.",
      "Use it to explain that multimodal models work across media, but a text model cannot automatically inspect images, audio, or video.",
      "Speech synthesis can run locally if optional packages exist. Audio transcription, image understanding, and video frame captions require a Groq key and transmit selected media. Video does not transcribe its audio.")
intro("Page 11 · Responsible AI", "RISKS, CONTROLS, AND REVIEW", "WHAT IT DOES",
      "Lists risks such as bias, privacy, hallucinations, deepfakes, copyright, misinformation, and lack of transparency, with mitigations and a human review checklist.",
      "WHY IT WORKS THIS WAY",
      "Safeguards are linked to actual project behavior: expression-only code, AST validation, a worker timeout, upload caps, local evidence, and explicit hosted-data notices.",
      "Use it to explain that safety is a process. A timeout and row cap reduce risk but do not create a full operating-system sandbox.",
      "Emphasize source verification, privacy, subgroup checks, and human oversight. The app is educational and should not be the sole basis for high-impact decisions.")
intro("Page 12 · Industry Applications", "WHERE THE WORKFLOW MAY HELP", "WHAT IT DOES",
      "Shows illustrative scenarios for healthcare, finance, education, retail, marketing, manufacturing, software, and customer support.",
      "WHY IT WORKS THIS WAY",
      "Each example follows the same workflow: approved data → quality review → bounded question → verified result → human review.",
      "Use it to discuss possible applications and the controls each domain needs. These are workflow examples, not deployed systems or performance claims.",
      "Keep the examples grounded. A healthcare use must protect health data and retain clinician review; financial uses need audits and approved decision controls.")
intro("Page 13 · Project Evaluation", "MEASURE WHAT THE DEMO DOES", "WHAT IT DOES",
      "Runs six fixed questions against the bundled synthetic dataset and calculates exact-match accuracy, execution success, answer-type validation, and response time.",
      "WHY IT WORKS THIS WAY",
      "The expected answers are known for the demo table, so the app can measure the actual run instead of presenting invented scores.",
      "Use it to show reproducible evaluation. Results belong only to this six-question demo set; they are not the SemEval paper's scores or general model benchmarks.",
      "The page calculates metrics at run time. Error correction is reported only if attempts occur. RAG relevance is not scored because no labeled relevance benchmark is provided.")
intro("Page 14 · About Project", "SOURCES AND PROJECT CONTEXT", "WHAT IT DOES",
      "Names the project, describes its modules and setup, and lists research references that informed the lessons and tabular analysis workflow.",
      "WHY IT WORKS THIS WAY",
      "The project report makes scope, limitations, and research inspiration traceable. It distinguishes this implementation from published benchmark results.",
      "Use it to close with the project contribution and answer questions about the sources behind the educational material.",
      "The app references I2R-NLP at SemEval-2025 Task 8, Attention Is All You Need, Auto-Encoding Variational Bayes, and Generative Adversarial Nets. The project does not claim to reproduce published scores.")

intro("How to present the live demo", "A SHORT TEACHER WALKTHROUGH", "LIVE SEQUENCE",
      "1. Open Home Dashboard\n2. Choose AI Data Analyst\n3. Upload a CSV or use sample sales data\n4. Review the row/column and missing-value profile\n5. Ask: “Which region has the highest revenue?”",
      "WHAT TO POINT OUT",
      "Show the result and calculation expression. Expand evidence, inspect the chart, then compare a second question such as average revenue by region.",
      "Optional: enable Qwen for a broader question, then visit Prompt Engineering, RAG, or the AI Agent to show how the project extends beyond CSV analysis.",
      "The current app is available at localhost port 8502 in the demonstration environment. Qwen runs locally through Ollama. The local analyst does not require a Groq API key.")
intro("Limits and next steps", "HONEST SCOPE", "CURRENT LIMITS",
      "The local planner covers common tabular questions; unfamiliar wording may need Qwen. Model-generated expressions can fail and are still subject to validation.",
      "NEXT IMPROVEMENTS",
      "Expand filters and aggregation coverage, add a labeled test suite for more question types, and add dataset-specific clarification when column meanings are ambiguous.",
      "Multimodal hosted features need a key and optional packages. Toy neural demonstrations teach concepts but do not represent trained production systems.",
      "This slide gives a credible boundary statement. The project is demo-ready for common CSV questions, but no software can guarantee every question or every input file will produce a useful answer.")
intro("Project takeaway", "CLOSING", "THE CONTRIBUTION",
      "InsightForge turns a table into an interactive analysis session: upload, inspect, ask, calculate, and review.",
      "THE DESIGN CHOICE",
      "Use deterministic computation where possible; add generative models where language flexibility helps; keep outputs reviewable with evidence and safety checks.",
      "Thank you · Questions",
      "Close by returning to the original problem: natural-language access to analysis with a visible calculation path. Invite questions about the pipeline, safety boundaries, or learning pages.")


def base_slide(idx, title, kicker=None, bg=WHITE):
    sld = ET.Element(P + "sld", {"showMasterSp": "0"})
    cs = el(sld, P + "cSld")
    bg_el = el(cs, P + "bg")
    bgpr = el(bg_el, P + "bgPr")
    solid(bgpr, bg)
    el(bgpr, A + "effectLst")
    tree = el(cs, P + "spTree")
    nv = el(tree, P + "nvGrpSpPr")
    el(nv, P + "cNvPr", {"id": "1", "name": ""})
    el(nv, P + "cNvGrpSpPr")
    el(nv, P + "nvPr")
    grp = el(tree, P + "grpSpPr")
    xf = el(grp, A + "xfrm")
    el(xf, A + "off", {"x": "0", "y": "0"})
    el(xf, A + "ext", {"cx": "0", "cy": "0"})
    el(xf, A + "chOff", {"x": "0", "y": "0"})
    el(xf, A + "chExt", {"cx": "0", "cy": "0"})
    sid = 2
    if kicker:
        add_text(tree, sid, "Section label", 76, 40, 600, 24, kicker.upper(), 12, TEAL, True); sid += 1
    add_text(tree, sid, "Slide title", 76, 78, 1130, 64, title, 34, NAVY, True); sid += 1
    add_shape(tree, sid, "Title rule", 76, 154, 66, 4, TEAL); sid += 1
    # Persistent footer anchors the source and page number.
    add_line(tree, sid, "Footer rule", 76, 676, 1204, 676, RULE, 1); sid += 1
    add_text(tree, sid, "Footer", 76, 684, 920, 20, "INSIGHTFORGE AI  ·  PROJECT PRESENTATION", 9, MID, True); sid += 1
    add_text(tree, sid, "Page number", 1154, 684, 48, 20, f"{idx:02d}", 9, MID, True, align="r"); sid += 1
    color_override = el(sld, P + "clrMapOvr")
    el(color_override, A + "masterClrMapping")
    return sld, tree, sid


def build_cover(idx, data):
    sld, tree, sid = base_slide(idx, "", None, NAVY)
    add_shape(tree, sid, "Cover accent", 78, 94, 8, 492, TEAL); sid += 1
    add_text(tree, sid, "Project name", 126, 156, 1030, 92, data["title"], 54, WHITE, True); sid += 1
    add_text(tree, sid, "Project subtitle", 128, 256, 940, 92, data["subtitle"], 36, "CBE2E6", True); sid += 1
    add_line(tree, sid, "Cover divider", 128, 374, 608, 374, GOLD, 3); sid += 1
    add_text(tree, sid, "Cover description", 128, 408, 880, 90, data["text"], 22, WHITE); sid += 1
    add_text(tree, sid, "Cover type", 128, 624, 700, 28, "INTELLIGENT DATA ANALYST COPILOT", 12, "91D9CE", True); sid += 1
    return sld


def build_two(idx, d):
    sld, tree, sid = base_slide(idx, d["title"], d.get("kicker"))
    add_text(tree, sid, "Opening statement", 76, 178, 1125, 72,
             d.get("lead", ""), 20, MID); sid += 1
    # Editorial two-column text composition; no decorative image panels.
    left_x, right_x, col_w = 78, 666, 530
    add_text(tree, sid, "Left section heading", left_x, 276, col_w, 28,
             d["left_head"], 13, TEAL, True); sid += 1
    add_text(tree, sid, "Left section content", left_x, 316, col_w, 228,
             d["left"], 19, INK); sid += 1
    add_line(tree, sid, "Column divider", 634, 274, 634, 552, RULE, 1); sid += 1
    add_text(tree, sid, "Right section heading", right_x, 276, col_w, 28,
             d["right_head"], 13, TEAL, True); sid += 1
    add_text(tree, sid, "Right section content", right_x, 316, col_w, 228,
             d["right"], 19, INK); sid += 1
    add_line(tree, sid, "Takeaway rule", 78, 574, 1202, 574, TEAL, 2); sid += 1
    add_text(tree, sid, "Slide takeaway", 78, 594, 1125, 64,
             d["bottom"], 16, NAVY, True); sid += 1
    return sld


def build_flow(idx, d):
    sld, tree, sid = base_slide(idx, d["title"], d["kicker"])
    steps = d["steps"]
    if len(steps) == 6:
        xs, widths, y = [66, 270, 474, 678, 882, 1086], [146]*6, 294
    else:
        xs, widths, y = [88, 323, 558, 793, 1028], [164]*5, 296
    for i, (num, head, detail) in enumerate(steps):
        x, w = xs[i], widths[i]
        add_text(tree, sid, f"Step {num}", x, y-60, w, 30, num, 13, TEAL, True, align="c"); sid += 1
        add_shape(tree, sid, f"Step baseline {num}", x, y-12, w, 4, TEAL if i == 0 else RULE); sid += 1
        add_text(tree, sid, f"Step heading {num}", x, y+14, w, 52, head, 20, NAVY, True, align="c"); sid += 1
        add_text(tree, sid, f"Step detail {num}", x-3, y+77, w+6, 82, detail, 16, MID, align="c"); sid += 1
        if i < len(steps)-1:
            add_text(tree, sid, f"Flow arrow {num}", x+w+4, y+32, 38, 40, "→", 23, TEAL, True, align="c"); sid += 1
    add_line(tree, sid, "Diagram takeaway rule", 78, 506, 1202, 506, TEAL, 2); sid += 1
    add_text(tree, sid, "Diagram takeaway", 78, 528, 1124, 120, d["bottom"], 19, INK)
    return sld


def slide_xml(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def build_theme():
    theme = ET.Element(A + "theme", {"name": "InsightForge"})
    el(theme, A + "themeElements")
    elems = theme.find(A + "themeElements")
    cs = el(elems, A + "clrScheme", {"name": "InsightForge"})
    colors = [("dk1", "12233F"), ("lt1", "FFFFFF"), ("dk2", "19283F"), ("lt2", "F5F8FB"),
              ("accent1", "0D8F89"), ("accent2", "F0B34D"), ("accent3", "5C6B80"),
              ("accent4", "70B7B1"), ("accent5", "91D9CE"), ("accent6", "CBE2E6"),
              ("hlink", "0563C1"), ("folHlink", "954F72")]
    for key, color in colors:
        entry = el(cs, A + key)
        el(entry, A + "srgbClr", {"val": color})
    fs = el(elems, A + "fontScheme", {"name": "Aptos"})
    major = el(fs, A + "majorFont")
    el(major, A + "latin", {"typeface": "Aptos Display"})
    el(major, A + "ea", {"typeface": "Aptos"})
    el(major, A + "cs", {"typeface": "Aptos"})
    minor = el(fs, A + "minorFont")
    el(minor, A + "latin", {"typeface": "Aptos"})
    el(minor, A + "ea", {"typeface": "Aptos"})
    el(minor, A + "cs", {"typeface": "Aptos"})
    fmt = el(elems, A + "fmtScheme", {"name": "InsightForge"})
    fills = el(fmt, A + "fillStyleLst")
    for _ in range(3):
        sf = el(fills, A + "solidFill"); el(sf, A + "schemeClr", {"val": "phClr"})
    lines = el(fmt, A + "lnStyleLst")
    for width in (6350, 12700, 19050):
        ln = el(lines, A + "ln", {"w": str(width), "cap": "flat", "cmpd": "sng", "algn": "ctr"})
        sf = el(ln, A + "solidFill"); el(sf, A + "schemeClr", {"val": "phClr"})
        el(ln, A + "prstDash", {"val": "solid"}); el(ln, A + "round")
    effects = el(fmt, A + "effectStyleLst")
    for _ in range(3):
        style = el(effects, A + "effectStyle"); el(style, A + "effectLst")
    bg = el(fmt, A + "bgFillStyleLst")
    for key in ("lt1", "lt2", "lt1"):
        sf = el(bg, A + "solidFill"); el(sf, A + "schemeClr", {"val": key})
    el(elems, A + "objectDefaults")
    el(elems, A + "extraClrSchemeLst")
    return ET.tostring(theme, encoding="utf-8", xml_declaration=True)


def make_package():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    built = []
    for i, d in enumerate(slides, 1):
        if d["kind"] == "cover":
            root = build_cover(i, d)
        elif d["kind"] == "flow":
            root = build_flow(i, d)
        else:
            root = build_two(i, d)
        built.append(slide_xml(root))

    types = ET.Element("{" + NS["ct"] + "}Types")
    el(types, "{" + NS["ct"] + "}Default", {"Extension": "rels", "ContentType": "application/vnd.openxmlformats-package.relationships+xml"})
    el(types, "{" + NS["ct"] + "}Default", {"Extension": "xml", "ContentType": "application/xml"})
    overrides = [
        ("/ppt/presentation.xml", "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"),
        ("/ppt/slideMasters/slideMaster1.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"),
        ("/ppt/slideLayouts/slideLayout1.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"),
        ("/ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
    ] + [(f"/ppt/slides/slide{i}.xml", "application/vnd.openxmlformats-officedocument.presentationml.slide+xml") for i in range(1, len(built)+1)]
    for part, ct in overrides:
        el(types, "{" + NS["ct"] + "}Override", {"PartName": part, "ContentType": ct})

    pres = ET.Element(P + "presentation")
    master_ids = el(pres, P + "sldMasterIdLst")
    el(master_ids, P + "sldMasterId", {"id": "2147483648", R + "id": "rId1"})
    slide_ids = el(pres, P + "sldIdLst")
    for i in range(1, len(built)+1):
        el(slide_ids, P + "sldId", {"id": str(255+i), R + "id": f"rId{i+1}"})
    el(pres, P + "sldSz", {"cx": str(px(W)), "cy": str(px(H)), "type": "screen16x9"})
    el(pres, P + "notesSz", {"cx": str(px(720)), "cy": str(px(540))})
    default_text = el(pres, P + "defaultTextStyle")
    el(default_text, A + "defPPr")

    master = ET.Element(P + "sldMaster")
    cs = el(master, P + "cSld")
    tree = el(cs, P + "spTree")
    nv = el(tree, P + "nvGrpSpPr"); el(nv, P + "cNvPr", {"id": "1", "name": ""}); el(nv, P + "cNvGrpSpPr"); el(nv, P + "nvPr")
    grp = el(tree, P + "grpSpPr"); xf = el(grp, A + "xfrm")
    for tag in ("off", "ext", "chOff", "chExt"):
        el(xf, A + tag, {"x": "0", "y": "0", "cx": "0", "cy": "0"} if tag in ("ext", "chExt") else {"x": "0", "y": "0"})
    clrm = el(master, P + "clrMap", {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2", "accent1": "accent1", "accent2": "accent2", "accent3": "accent3", "accent4": "accent4", "accent5": "accent5", "accent6": "accent6", "hlink": "hlink", "folHlink": "folHlink"})
    lays = el(master, P + "sldLayoutIdLst")
    el(lays, P + "sldLayoutId", {"id": "1", R + "id": "rId1"})
    txstyles = el(master, P + "txStyles")
    for nm in ("titleStyle", "bodyStyle", "otherStyle"):
        st = el(txstyles, P + nm)
        el(st, A + "lvl1pPr")

    layout = ET.Element(P + "sldLayout", {"type": "blank", "preserve": "1"})
    lcs = el(layout, P + "cSld")
    lst = el(lcs, P + "spTree")
    nv = el(lst, P + "nvGrpSpPr"); el(nv, P + "cNvPr", {"id": "1", "name": ""}); el(nv, P + "cNvGrpSpPr"); el(nv, P + "nvPr")
    grp = el(lst, P + "grpSpPr"); xf = el(grp, A + "xfrm")
    el(xf, A + "off", {"x":"0","y":"0"}); el(xf, A + "ext", {"cx":"0","cy":"0"}); el(xf, A + "chOff", {"x":"0","y":"0"}); el(xf, A + "chExt", {"cx":"0","cy":"0"})
    el(layout, P + "clrMapOvr")
    layout.find(P + "clrMapOvr").append(ET.Element(A + "masterClrMapping"))

    def rels(items):
        root = ET.Element("{" + NS["rel"] + "}Relationships")
        for rid, typ, target in items:
            el(root, "{" + NS["rel"] + "}Relationship", {"Id": rid, "Type": typ, "Target": target})
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    rel_base = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
    parts = {
        "[Content_Types].xml": ET.tostring(types, encoding="utf-8", xml_declaration=True),
        "_rels/.rels": rels([("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml")]),
        "ppt/presentation.xml": ET.tostring(pres, encoding="utf-8", xml_declaration=True),
        "ppt/_rels/presentation.xml.rels": rels([("rId1", rel_base+"slideMaster", "slideMasters/slideMaster1.xml")] + [(f"rId{i+1}", rel_base+"slide", f"slides/slide{i}.xml") for i in range(1, len(built)+1)]),
        "ppt/slideMasters/slideMaster1.xml": ET.tostring(master, encoding="utf-8", xml_declaration=True),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": rels([("rId1", rel_base+"slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", rel_base+"theme", "../theme/theme1.xml")]),
        "ppt/slideLayouts/slideLayout1.xml": ET.tostring(layout, encoding="utf-8", xml_declaration=True),
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": rels([("rId1", rel_base+"slideMaster", "../slideMasters/slideMaster1.xml")]),
        "ppt/theme/theme1.xml": build_theme(),
    }
    for i, xml in enumerate(built, 1):
        parts[f"ppt/slides/slide{i}.xml"] = xml
        parts[f"ppt/slides/_rels/slide{i}.xml.rels"] = rels([("rId1", rel_base+"slideLayout", "../slideLayouts/slideLayout1.xml")])
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
        for name, content in parts.items():
            zf.writestr(name, content)
    print(f"Created {OUT} with {len(built)} slides ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    make_package()
