import os
import re
from flask import Flask, request, jsonify, render_template
from pypdf import PdfReader
from transformers import pipeline

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ======================================================
# Flask App Configuration
# ======================================================
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================================================
# Load Hugging Face Models
# ======================================================

# 1) Summarization model (compression)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0  # use -1 if CPU
)

# 2) Instruction-following model (structuring)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=0  # use -1 if CPU
)

# ======================================================
# Utility Functions
# ======================================================

def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(
        page.extract_text()
        for page in reader.pages
        if page.extract_text()
    )


def split_text(text, max_chunk_words=400):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current, count = [], [], 0

    for s in sentences:
        w = len(s.split())
        if count + w > max_chunk_words:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(s)
        count += w

    if current:
        chunks.append(" ".join(current))

    return chunks


def force_bullets(text, max_items=5):
    text = text.replace("\n", " ").strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)

    bullets = []
    for s in sentences:
        s = s.strip()
        if len(s) > 10:
            bullets.append(f"- {s}")

    return "\n".join(bullets[:max_items])


# ======================================================
# LCEL Helper Functions
# ======================================================

def summarize_chunks(chunks):
    summaries = []
    for chunk in chunks:
        summary = summarizer(
            chunk,
            max_length=120,
            min_length=40,
            do_sample=False
        )[0]["summary_text"]
        summaries.append(summary)
    return " ".join(summaries)


summarize_chunks_r = RunnableLambda(summarize_chunks)


def gen(prompt, max_tokens):
    return generator(
        prompt,
        max_new_tokens=max_tokens,
        do_sample=False
    )[0]["generated_text"].strip()


# ======================================================
# Flask Routes
# ======================================================

@app.route("/", methods=["GET"])
def index():
    """Serve the web UI"""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/summarize", methods=["POST"])
def summarize_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    summary_length = request.form.get("length", "medium")

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # Length control
    length_map = {
        "short": {"exec": 60, "points": 80, "concepts": 60, "takeaway": 40},
        "medium": {"exec": 120, "points": 120, "concepts": 80, "takeaway": 60},
        "long": {"exec": 200, "points": 180, "concepts": 120, "takeaway": 80},
    }

    lm = length_map.get(summary_length, length_map["medium"])

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        text = load_pdf_text(file_path)
        if not text.strip():
            return jsonify({"error": "PDF contains no extractable text"}), 400

        chunks = split_text(text)
        combined_summary = summarize_chunks_r.invoke(chunks)

        # -------- Structured generation --------
        title = gen(
            f"Generate a concise technical title:\n{combined_summary}",
            20
        )

        executive_summary = gen(
            f"Write an executive summary (3–4 sentences):\n{combined_summary}",
            lm["exec"]
        )

        raw_key_points = gen(
            f"Extract the most important points:\n{combined_summary}",
            lm["points"]
        )

        raw_concepts = gen(
            f"List important technical concepts:\n{combined_summary}",
            lm["concepts"]
        )

        final_takeaway = gen(
            f"Write a strong final takeaway sentence:\n{combined_summary}",
            lm["takeaway"]
        )

        return jsonify({
            "title": title,
            "executive_summary": executive_summary,
            "key_points": force_bullets(raw_key_points),
            "important_concepts": force_bullets(raw_concepts),
            "final_takeaway": final_takeaway
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ======================================================
# Run Application
# ======================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
