

import os
import json
from flask import Flask, render_template, request

from modules.transcriber import transcribe_audio
from modules.entity_extractor import extract_entities
from modules.summarizer import generate_summary
from modules.semantic_tagger import semantic_tags
from modules.knowledge_graph import extract_relationships

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        if "audio" not in request.files:
            return "No file uploaded"

        file = request.files["audio"]

        if file.filename == "":
            return "No selected file"

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 1. Transcribe audio
        transcript = transcribe_audio(file_path)
        text = transcript["text"]

        # 2. Extract information
        summary = generate_summary(text)
        entities = extract_entities(text)
        tags = semantic_tags(text)
        relationships = extract_relationships(text)

        # 3. Store all results
        result = {
            "transcript": text,
            "summary": summary,
            "entities": entities,
            "tags": tags,
            "relationships": relationships
        }

        # 4. Save result to JSON
        output_file = os.path.join(OUTPUT_FOLDER, "result.json")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)