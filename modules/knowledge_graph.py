

import spacy
import networkx as nx

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def extract_relationships(text):
    """
    Extract subject-relation-object triples from text.
    Example:
    'Alice built a robot.' ->
    {'subject': 'Alice', 'relation': 'build', 'object': 'robot'}
    """
    doc = nlp(text)
    relationships = []

    for sent in doc.sents:
        subject = None
        relation = None
        obj = None

        for token in sent:
            # Subject
            if "subj" in token.dep_:
                subject = token.text

            # Main verb / relation
            elif token.dep_ == "ROOT":
                relation = token.lemma_

            # Object
            elif "obj" in token.dep_:
                obj = token.text

        if subject and relation and obj:
            relationships.append({
                "subject": subject,
                "relation": relation,
                "object": obj
            })

    return relationships


def build_graph(relationships):
    """
    Convert relationships into a directed graph.
    """
    graph = nx.DiGraph()

    for rel in relationships:
        graph.add_edge(
            rel["subject"],
            rel["object"],
            relation=rel["relation"]
        )

    return graph


# Optional test
if __name__ == "__main__":
    sample_text = """
    John developed an AI system.
    The AI system analyzes audio.
    Researchers use the system for interviews.
    """

    relationships = extract_relationships(sample_text)

    print("Extracted Relationships:")
    for rel in relationships:
        print(rel)

    graph = build_graph(relationships)

    print("\nGraph Edges:")
    for source, target, data in graph.edges(data=True):
        print(f"{source} --[{data['relation']}]--> {target}")