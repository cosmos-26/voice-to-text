from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "political speech",
    "motivational speech",
    "history",
    "government",
    "education",
    "meeting",
    "interview",
    "lecture"
]

def semantic_tags(text):
    result = classifier(text, labels)
    return result["labels"][:3]