import nltk
import ssl
from frame_semantic_transformer import FrameSemanticTransformer
import pandas as pd
import pickle
import logging

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


def get_frame_semantics(filename: str, region: str):
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


if __name__ == "__main__":
    regions = ["UK", "US", "MiddleEast"]
    for region in regions:
        get_frame_semantics(f"./data/processed/{region}.csv", region)
