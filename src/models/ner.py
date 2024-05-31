import ssl
import spacy
import pandas as pd
import nltk
import pickle
import logging
logger = logging.getLogger()

nlp = spacy.load("en_core_web_sm")


def run_spacy_ner(filename: str, region: str):
    """Function to get frame semantics 

    Args:
        df (pd.DataFrame): dataframe for region
        filename (str): name of file
    """

    pickle_obj = {"index": [], "ner_output": []}

    df = pd.read_csv(filename)

    try:
        for row in df.iterrows():
            index = row[0]
            print(row[0])
            ner_outputs = []
            article_text = row[1].maintext
            try:
                doc = nlp(article_text)
                ner_outputs.append(
                    [[ent.text, ent.start_char, ent.end_char, ent.label_]
                     for ent in doc.ents])
            except Exception as e:
                logger.error(e)
                pass
    except Exception as e:
        logger.error(e)
        pass
    else:
        pickle_obj["index"].append(index)
        pickle_obj["ner_output"].append(ner_outputs)
        pickle.dump(pickle_obj, file=open(
            f"../data/processed/ner/ner_{region}.pickle", "wb"))


if __name__ == "__main__":
    regions = ["UK", "US", "MiddleEast"]
    for region in regions:
        run_spacy_ner(
            f"./data/raw/filtered_data/{region}.csv", region)
