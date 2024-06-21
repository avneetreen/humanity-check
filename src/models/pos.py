import spacy
from spacy.tokens import Doc
from spacy.language import Language
import pandas as pd
import pickle

# Load the spaCy model
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
# Add the sentencizer to the pipeline
nlp.add_pipe('sentencizer')


def read_file(filename: str):
    data = pd.read_csv(filename)
    return data


def batch_extract_docs_tokens_pos(documents, batch_size=1000):
    # This will hold the final results: A list of documents, each containing a list of sentence POS tags
    docs_tokens_pos = ()

    # Process documents in batches using spaCy's pipe for efficient batch processing
    for doc in nlp.pipe(documents, batch_size=batch_size):
        # Temporary list to store sentence-wise token POS tags for the current document
        doc_tokens_pos = []

        # Iterate through each sentence in the document
        for sent in doc.sents:
            # Extract tokens and POS tags for the current sentence
            sentence_tokens_pos = [(token.text, token.pos_) for token in sent]
            # Append the sentence's tokens POS tags to the document's list
            doc_tokens_pos.append(sentence_tokens_pos)

        # Append the processed document to the main list
        docs_tokens_pos.append(doc_tokens_pos)

    return docs_tokens_pos


def frame_based_batch_extract_docs_tokens_pos(
        frame_sentences_dict, batch_size=1000):
    # This will hold the final results: A dict with frames as keys and lists of POS tags as values
    frame_docs_tokens_pos = {}

    # Iterate over each frame and its list of sentences
    for frame, sentences in frame_sentences_dict.items():
        # Process the sentences in batches using spaCy's pipe for efficient batch processing
        docs = nlp.pipe(sentences, batch_size=batch_size)

        # Temporary list to store all sentence-wise token POS tags for the current frame
        frame_tokens_pos = []

        # Iterate through each doc (sentences) processed for the current frame
        for doc in docs:
            # Extract tokens and POS tags for each sentence in the document
            for sent in doc.sents:
                sentence_tokens_pos = [(token.text, token.pos_)
                                       for token in sent]
                frame_tokens_pos.append(sentence_tokens_pos)

        # Associate the collected POS tags with their corresponding frame in the result dictionary
        frame_docs_tokens_pos[frame] = frame_tokens_pos

    return frame_docs_tokens_pos


if __name__ == '__main__':
    """
    with open("../../data/processed/pos/input_verbs_frames.pickle", "rb") as f:
        UK_frame_semantics = pickle.load(f)
    all_documents = []
    for document in UK_frame_semantics["frame_semantics"]:
        sentences = [sentence.sentence for sentence in document]
        all_documents.append(" ".join(sentences))
    processed_documents = batch_extract_docs_tokens_pos(all_documents)
    with open('pos_UK.pkl', 'wb') as f:
        pickle.dump(processed_documents, f)"""

    with open("../../data/processed/pos/input_verbs_frames.pickle", "rb") as f:
        frames_sentences = pickle.load(f)
    frame_docs_tokens_pos = frame_based_batch_extract_docs_tokens_pos(
        frames_sentences)
    with open('pos_sentences_frames_UK.pkl', 'wb') as f:
        pickle.dump(frame_docs_tokens_pos, f)
