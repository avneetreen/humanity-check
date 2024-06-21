import spacy
from spacy.tokens import Doc
from spacy.language import Language
import pandas as pd
import pickle

# Load the spaCy model
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Define the custom preprocessing component


def read_file(filename: str):
    data = pd.read_csv(filename)
    return data


@Language.component("custom_preprocessor")
def preprocess_text(doc):
    # Perform lemmatization and remove stopwords and punctuation
    lemmas = [token.lemma_.lower() for token in doc
              if not token.is_stop and not token.is_punct]
    # Create a new Doc from the processed tokens (lemmas)
    processed_doc = Doc(doc.vocab, words=lemmas)
    return processed_doc


# Add the custom component to the pipeline
nlp.add_pipe("custom_preprocessor", last=True)


def process_documents(texts):
    """Process documents using spaCy's pipe for batch processing."""
    # Ensure n_process=1 for compatibility or adjust according to your setup
    return [doc for doc in nlp.pipe(texts, batch_size=50, n_process=-1)]


if __name__ == '__main__':
    US = read_file('../../data/raw/selected_data/selected_US.csv')
    processed_documents = process_documents(US['maintext'].tolist())
    with open('processed_documents_US.pkl', 'wb') as f:
        pickle.dump(processed_documents, f)
