import ssl
from frame_semantic_transformer import FrameSemanticTransformer
import pandas as pd
import pickle
import logging
import spacy

nlp = spacy.load("en_core_web_sm")

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

logger = logging.getLogger()


def chunks(df: pd.DataFrame, chunk_size: int):
    """Function to yield chunks

    Args:
        df (pd.DataFrame): Dataframe for region
        chunk_size (int): size of chunks

    Yields:
        df: Dataframe of chunk size
    """
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]


def get_frame_semantics_titles(filename: str, region: str):
    """Function to get frame semantics 

    Args:
        df (pd.DataFrame): dataframe for region
        filename (str): name of file
    """

    df = pd.read_csv(filename)
    frame_transformer = FrameSemanticTransformer(batch_size=16)

    iterator = chunks(df, 16)
    pickle_obj = {"indices": [], "frame_semantics": []}
    for chunk in iterator:
        print(chunk)
        try:
            result = frame_transformer.detect_frames_bulk(chunk.title.values)
        except Exception as e:
            logger.error(e)
        else:
            indices = list(chunk.index)
            pickle_obj["indices"].extend(indices)
            pickle_obj["frame_semantics"].extend(result)
            pickle.dump(
                pickle_obj,
                file=open(
                    f"./data/processed/doc_semantics/frame_semantics_{region}_head.pickle",
                    "wb"))


def process_article(article_text: str):
    """Tokenize the article into sentences and clean them."""
    doc = nlp(article_text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def get_frame_semantics_docs(filename: str, region: str):
    """Process documents to extract frame semantics and save periodically."""
    df = pd.read_csv(filename)
    print(df.shape)
    frame_transformer = FrameSemanticTransformer(batch_size=32)
    results = {"index": [], "frame_semantics": [], 'title': []}

    for index, row in df.iterrows():
        try:
            headline = row['title']
            sentences = process_article(row['maintext'])
            print(len(sentences))

            # Create batches of sentences
            batch_size = 32
            sentence_batches = [
                sentences[i: i + batch_size]
                for i in range(0, len(sentences),
                               batch_size)]

            doc_semantics = []
            for batch in sentence_batches:
                batch_semantics = frame_transformer.detect_frames_bulk(batch)
                print(batch_semantics)
                doc_semantics.extend(batch_semantics)

            results['title'].append(headline)
            results['index'].append(index)
            results['frame_semantics'].append(doc_semantics)

            # Save periodically or based on some condition
            if len(results['index']) % 100 == 0:
                save_results(results, region)

        except Exception as e:
            logger.error(f"Error processing index {index}: {e}")
            pass

    # Save remaining results at the end of processing
    if results['index']:
        save_results(results, region)


def save_results(results, region):
    """Save the processed results to a pickle file."""
    filename = f"./data/processed/doc_semantics/frame_semantics_{region}.pickle"
    with open(filename, 'wb') as f:
        pickle.dump(results, f)
    print(f"Saved results to {filename}")


if __name__ == "__main__":
    regions = ["UK", "US", "MiddleEast"]
    for region in regions:
        get_frame_semantics_docs(
            f"./data/raw/filtered_data/{region}.csv", region)
