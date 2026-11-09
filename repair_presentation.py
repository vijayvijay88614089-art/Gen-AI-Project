from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET

SOURCE = Path(r"C:\Users\hp\Downloads\InsightForge_AI_Prompt_Engineering_Methodology.pptx")
OUTPUT = Path(r"C:\Users\hp\OneDrive - RV University\Documents\GEN AI project\InsightForge_AI\InsightForge_AI_Demo_Presentation.pptx")
TMP = OUTPUT.with_suffix(".tmp.pptx")
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}
for pre in ("p", "a", "r"):
    ET.register_namespace(pre, NS[pre])
ET.register_namespace("", NS["ct"])
P, A, R = "{" + NS["p"] + "}", "{" + NS["a"] + "}", "{" + NS["r"] + "}"

# This original project methodology presentation is used as a PowerPoint-native
# design base. Its existing slide parts, master, theme and relationships remain intact.
PAGE_SLIDES = [
    ("Page 01 | Home Dashboard", "The project entry point and working sample",
     "What it does", "Introduces InsightForge and previews the included synthetic sales table. A chart groups revenue by region, while summary text links the main analysis and learning features.",
     "Why this design", "A ready-to-use example removes setup friction. Visitors can see the kind of file and output expected before uploading their own data.",
     "Use it to introduce the project: the main feature is transparent question answering over an uploaded table."),
    ("Page 02 | AI Fundamentals", "Core distinctions behind generative modelling",
     "What it does", "Compares discriminative prediction with generative modelling. Expands probability and neural-network basics, and includes a small softmax probability control.",
     "Why this design", "The page explains what a model is trying to produce before comparing architectures. The slider makes probability visible without claiming to run a trained model.",
     "Use it to explain AI versus Generative AI, probability, and neural-network layers. Softmax values are illustrative—not model predictions."),
    ("Page 03 | Generative Models", "Model families, evolution, and toy demonstrations",
     "What it does", "Explores HMMs, Autoencoders, VAEs, GANs, DCGANs, conditional GANs, StyleGAN, and CycleGAN concepts. It includes a hand-set Markov sample and optional tiny training demos.",
     "Why this design", "Model cards compare architecture, learning principle, uses, and limits. Small synthetic examples make model mechanics easier to see without large training data.",
     "Use it to teach how generative models developed. Toy training uses 8×8 patterns; StyleGAN is explained rather than trained, and CycleGAN is a concept illustration."),
    ("Page 04 | Deep Learning Models", "Sequence models and attention",
     "What it does", "Compares RNN, LSTM, BiLSTM, GRU, and BiGRU. An interactive heatmap illustrates attention weights for a short token sequence.",
     "Why this design", "A model comparison highlights memory, directionality, strengths, and trade-offs. The heatmap gives a visual explanation of how tokens can attend to one another.",
     "Use it to teach sequence modelling and attention. The classifier implementations are untrained; toy attention vectors are demonstrations, not learned results."),
    ("Page 05 | Transformers and LLMs", "Foundation models and text generation",
     "What it does", "Explains attention, autoregressive generation, pretraining versus fine-tuning, foundation models, and multimodality. Offers optional hosted Groq and local Qwen text generation.",
     "Why this design", "Concept explanations are separated from model execution. Qwen 2.5 Coder 1.5B runs locally through Ollama; hosted requests remain opt-in.",
     "Use it to show a local model response and explain how a foundation model can be adapted. Large Hugging Face models need substantially more RAM."),
    ("Page 06 | Prompt Engineering", "Structured instructions and prompt safety",
     "What it does", "Builds prompts with Persona Pattern, Root Prompt, RGC (Role, Goal, Context, Constraints), chain-of-thought summary, and Comparative Prompting. Tone, format, length, and background can be set.",
     "Why this design", "The page previews the assembled prompt before generation, supports comparison and saving, and treats background text as untrusted reference content.",
     "Use it to show how instruction structure controls output. Injection detection is a heuristic; the chain-of-thought option asks for a concise summary only."),
    ("Page 07 | AI Data Analyst", "The main project feature",
     "What it does", "Loads CSV or Excel uploads, profiles rows and columns, reports missing values, previews data and statistics, and accepts natural-language questions.",
     "Why this design", "A deterministic local planner handles common questions first. Optional Qwen can propose a plan for less familiar questions; expressions pass validation before execution.",
     "Use it to demonstrate a real answer with its expression, evidence, explanation path, and relevant chart. Uploaded rows are not written to query history."),
    ("Page 08 | RAG Document Assistant", "Ground answers in retrieved document passages",
     "What it does", "Accepts PDF and TXT files, extracts text, creates overlapping chunks, retrieves passages, and displays source snippets and page references.",
     "Why this design", "Local TF-IDF retrieval works with a lightweight setup. Optional Sentence Transformers and FAISS can provide dense semantic retrieval when installed.",
     "Use it to demonstrate retrieval-augmented generation. Retrieved passages are evidence to inspect; they cannot override system instructions or guarantee truth."),
    ("Page 09 | AI Agent", "A visible, bounded tool-using workflow",
     "What it does", "Shows a task plan, selected named tools, permissions, completed actions, result, calculation expression, and chart.",
     "Why this design", "The agent exposes a small read-only tool set and routes calculations through the same constrained analyst pipeline. Its actions remain visible to the user.",
     "Use it to discuss agent planning without shell, network, filesystem, arbitrary Python, or mutation access. Document retrieval is not silently mixed into table analysis."),
    ("Page 10 | Multimodal AI", "Text, audio, image, and video examples",
     "What it does", "Shows text prompting, audio transcription, offline text-to-speech, image questions, and sparse video keyframe summaries.",
     "Why this design", "Separate tabs make modality, dependencies, and provider requirements clear. Video analysis samples up to five frames and summarizes their captions.",
     "Use it to explain that models need modality-specific capabilities. Groq audio/image/video calls transmit selected media; video analysis does not transcribe audio."),
    ("Page 11 | Responsible AI", "Risks, controls, and human review",
     "What it does", "Covers bias, privacy, hallucinations, deepfakes, copyright, misinformation, and transparency, with mitigations and a user review checklist.",
     "Why this design", "Controls reflect the actual app: AST validation, expression-only code, a worker timeout, upload caps, visible evidence, and notices before hosted transmission.",
     "Use it to explain that safeguards reduce risk but do not prove every answer is correct or create a full OS sandbox. Keep human review for consequential decisions."),
    ("Page 12 | Industry Applications", "Illustrative uses across sectors",
     "What it does", "Presents possible workflows in healthcare, finance, education, retail, marketing, manufacturing, software, and customer support.",
     "Why this design", "Each example follows a common pattern: approved data, quality review, a bounded question, a checked answer, and human review.",
     "Use it to discuss possible applications and their controls. These examples are educational workflows, not validated deployments or performance claims."),
    ("Page 13 | Project Evaluation", "Measure performance on a fixed demonstration set",
     "What it does", "Runs six known questions against the synthetic demo data and calculates exact-match accuracy, execution success, answer-type validation, and response time.",
     "Why this design", "Expected answers are known for this dataset, so the app calculates actual results rather than presenting invented performance scores.",
     "Use it to explain reproducible evaluation. Results apply only to this six-question demo set—not the SemEval benchmark or general model performance."),
    ("Page 14 | About Project", "Project context, scope, and references",
     "What it does", "Names the project, summarizes its modules and setup, and links research that informed the educational and tabular QA portions.",
     "Why this design", "The project report and reference list make scope and research inspiration traceable. The app separates its own demo results from published scores.",
     "Use it to close the presentation and answer questions about research inspiration, implementation scope, and project limitations."),
    ("CSV demo | Example questions and answers", "Verified values from the included 24-row synthetic dataset",
     "Ask in plain language", "Which region has the highest revenue?  •  Show total revenue by product.  •  What is average revenue by region?  •  How many missing values are there?",
     "Calculated sample output", "Rows: 24  •  Total revenue: 4,633.50  •  Highest region: East — 1,266.00  •  North: 1,155.00  •  West: 1,107.00  •  South: 1,105.50  •  Missing cells: 0",
     "Figures are computed from sample_data/sales_demo.csv, which is synthetic. Upload a real CSV to calculate from its records; confirm column meaning and data quality."),
]


def set_shape_text(xml_root, shape_id: str, value: str):
    for shape in xml_root.findall(".//p:sp", NS):
        c_nv = shape.find("./p:nvSpPr/p:cNvPr", NS)
        if c_nv is None or c_nv.get("id") != str(shape_id):
            continue
        nodes = shape.findall(".//a:t", NS)
        if not nodes:
            raise ValueError(f"Text shape {shape_id} has no text run")
        nodes[0].text = value
        for node in nodes[1:]:
            node.text = ""
        return
    raise ValueError(f"Could not find shape ID {shape_id}")


def rels_for_clone(source_rels: bytes) -> bytes:
    # Slide 2 has only a slide-layout relationship, so its rels are safe to clone.
    root = ET.fromstring(source_rels)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main():
    with ZipFile(SOURCE) as src:
        package = {info.filename: src.read(info.filename) for info in src.infolist()}

    # Update the original cover and the two project-level slides that no longer
    # accurately described the working implementation.
    slide1 = ET.fromstring(package["ppt/slides/slide1.xml"])
    set_shape_text(slide1, "7", "Generative AI, prompt engineering, and verified data analysis")
    set_shape_text(slide1, "8", "Project Presentation • Complete application walkthrough")
    set_shape_text(slide1, "9", "DEMO PROJECT  |  CSV + EXCEL ANALYSIS")
    package["ppt/slides/slide1.xml"] = ET.tostring(slide1, encoding="utf-8", xml_declaration=True)

    slide3 = ET.fromstring(package["ppt/slides/slide3.xml"])
    workflow_text = {
        "2": "02  |  End-to-End Workflow",
        "4": "A staged process from upload to a checked answer",
        "7": "1", "8": "Upload file", "9": "CSV / Excel",
        "12": "2", "13": "Inspect", "14": "Schema + quality",
        "17": "3", "18": "Ask", "19": "Plain-language question",
        "22": "4", "23": "Plan", "24": "Local rules / optional Qwen",
        "27": "5", "28": "Validate", "29": "Safe expression + worker",
        "32": "6", "33": "Review", "34": "Answer + evidence + chart",
        "35": "Numeric answers come from local dataframe calculations. Optional Qwen can propose a plan; the app checks expressions before execution.",
    }
    for shape_id, value in workflow_text.items():
        set_shape_text(slide3, shape_id, value)
    package["ppt/slides/slide3.xml"] = ET.tostring(slide3, encoding="utf-8", xml_declaration=True)

    slide10 = ET.fromstring(package["ppt/slides/slide10.xml"])
    implementation_text = {
        "2": "09  |  Working Application",
        "4": "Core components in the current demonstration",
        "5": "10",
        "8": "User interface", "9": "Streamlit pages / File uploads, questions, learning content, and results.",
        "12": "Data layer", "13": "Pandas + profile / Load tables, inspect columns, summarize quality and statistics.",
        "16": "Analysis + safety", "17": "Planner, Qwen, validator / Calculate locally; check generated expressions in a bounded worker.",
        "20": "Evidence + review", "21": "Charts + evaluation / Show calculation evidence, history, and measured demo results.",
        "22": "The local analyst works without a Groq key. Ollama Qwen is an optional local language-model path for broader question wording.",
    }
    for shape_id, value in implementation_text.items():
        set_shape_text(slide10, shape_id, value)
    package["ppt/slides/slide10.xml"] = ET.tostring(slide10, encoding="utf-8", xml_declaration=True)

    # Clone the valid two-column content slide, preserving the template's native
    # slide geometry and editable PowerPoint shapes.
    base_slide = ET.fromstring(package["ppt/slides/slide2.xml"])
    base_rels = package["ppt/slides/_rels/slide2.xml.rels"]
    for new_number, record in enumerate(PAGE_SLIDES, 12):
        header, subtitle, left_head, left_body, right_head, right_body, takeaway = record
        slide = deepcopy(base_slide)
        values = {"2": header, "4": subtitle, "5": f"{new_number:02d}",
                  "8": left_head, "9": left_body, "12": right_head,
                  "13": right_body, "14": takeaway}
        for shape_id, value in values.items():
            set_shape_text(slide, shape_id, value)
        package[f"ppt/slides/slide{new_number}.xml"] = ET.tostring(slide, encoding="utf-8", xml_declaration=True)
        package[f"ppt/slides/_rels/slide{new_number}.xml.rels"] = rels_for_clone(base_rels)

    # Append the new slide references to the original presentation manifest.
    pres = ET.fromstring(package["ppt/presentation.xml"])
    sld_ids = pres.find("p:sldIdLst", NS)
    rel_root = ET.fromstring(package["ppt/_rels/presentation.xml.rels"])
    rel_tag = "{" + NS["rel"] + "}Relationship"
    existing_ids = [int(x.get("id")) for x in sld_ids.findall("p:sldId", NS)]
    rel_numbers = []
    for item in rel_root.findall(rel_tag):
        rid = item.get("Id", "")
        if rid.startswith("rId") and rid[3:].isdigit():
            rel_numbers.append(int(rid[3:]))
    next_rid = max(rel_numbers) + 1
    for n in range(12, 12 + len(PAGE_SLIDES)):
        rid = f"rId{next_rid}"
        sld_ids.append(ET.Element(P + "sldId", {"id": str(max(existing_ids) + (n - 11)), R + "id": rid}))
        ET.SubElement(rel_root, rel_tag, {"Id": rid,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide",
            "Target": f"slides/slide{n}.xml"})
        next_rid += 1
    package["ppt/presentation.xml"] = ET.tostring(pres, encoding="utf-8", xml_declaration=True)
    package["ppt/_rels/presentation.xml.rels"] = ET.tostring(rel_root, encoding="utf-8", xml_declaration=True)

    # Register each cloned slide's MIME type with the package.
    types = ET.fromstring(package["[Content_Types].xml"])
    override_tag = "{" + NS["ct"] + "}Override"
    existing_parts = {o.get("PartName") for o in types.findall(override_tag)}
    for n in range(12, 12 + len(PAGE_SLIDES)):
        part = f"/ppt/slides/slide{n}.xml"
        if part not in existing_parts:
            ET.SubElement(types, override_tag, {"PartName": part,
                "ContentType": "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"})
    package["[Content_Types].xml"] = ET.tostring(types, encoding="utf-8", xml_declaration=True)

    app_key = "docProps/app.xml"
    if app_key in package:
        app = ET.fromstring(package[app_key])
        for element in app.iter():
            if element.tag.endswith("}Slides") or element.tag == "Slides":
                element.text = str(11 + len(PAGE_SLIDES))
        package[app_key] = ET.tostring(app, encoding="utf-8", xml_declaration=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(TMP, "w", ZIP_DEFLATED) as dst:
        for name, data in package.items():
            dst.writestr(name, data)
    TMP.replace(OUTPUT)
    print(f"Built {OUTPUT} with {11 + len(PAGE_SLIDES)} slides from the PowerPoint-native source package.")


if __name__ == "__main__":
    main()
