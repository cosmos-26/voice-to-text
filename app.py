import json
import os
from modules.transcriber import transcribe_audio
from modules.entity_extractor import extract_entities
from modules.summarizer import generate_summary
from modules.semantic_tagger import semantic_tags

audio_path = r"C:\Users\ipsa1\Downloads\jfk.flac"
print(audio_path)
transcript = transcribe_audio(audio_path)

summary = generate_summary(transcript["text"])
entities = extract_entities(transcript["text"])
tags = semantic_tags(transcript["text"])

output = {
    "transcript": transcript["text"],
    "summary": summary,
    "entities": entities,
    "tags": tags
}

os.makedirs("outputs", exist_ok=True)

with open("outputs/result.json", "w") as f:
    json.dump(output, f, indent=4)

print(json.dumps(output, indent=4))