import nltk
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

nltk.download('wordnet')
nltk.download('framenet_v17')

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
            pickle.dump(pickle_obj, file=open(
                f"./data/processed/frame_semantics_{region}.pickle", "wb"))


# Function to process each article and return frames
def process_article(article_text: str):
    """Function to process each article 
        and tokenize sentences

    Args:
        article_text (_type_): string

    Returns:
        _type_: list
    """
    # Tokenize the article into sentences
    try:
        doc = nlp(article_text)
        sentences = [sent.text for sent in doc.sents]
        sentences = [sent for sent in sentences if sent.strip() != ""]
        return sentences
    except Exception as e:
        logger.error(e)
    else:
        return []


def get_frame_semantics_docs(filename: str, region: str):
    """Function to get frame semantics 

    Args:
        df (pd.DataFrame): dataframe for region
        filename (str): name of file
    """

    pickle_obj = {"index": [], "frame_semantics": []}

    df = pd.read_csv(filename)
    frame_transformer = FrameSemanticTransformer()

    try:
        for row in df.iterrows():
            index = row[0]
            doc_semantics = []
            article_text = row[1].maintext
            sentences = process_article(article_text)
            print(index, len(sentences))
            try:
                doc_semantics = [
                    frame_transformer.detect_frames(sentence)
                    for sentence in sentences]
            except Exception as e:
                logger.error(e)
                pass
    except Exception as e:
        logger.error(e)
    else:
        pickle_obj["index"].append(index)
        pickle_obj["frame_semantics"].append(doc_semantics)
        pickle.dump(
            pickle_obj,
            file=open(
                f"../data/processed/doc_semantics/frame_semantics_{region}.pickle",
                "wb"))


if __name__ == "__main__":
    regions = ["UK", "US", "MiddleEast"]
    for region in regions:
        get_frame_semantics_docs(
            f"./data/raw/filtered_data/{region}.csv", region)
