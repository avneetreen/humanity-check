import spacy
import pandas as pd
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

    pickle_obj_head = {"index": [], "ner_output": []}
    pickle_obj_main = {"index": [], "ner_output": []}

    df = pd.read_csv(filename)

    try:
        for row in df.iterrows():
            index = row[0]
            print(row[0])
            ner_outputs_head = []
            ner_outputs_main = []
            article_headline = row[1].title
            article_text = row[1].maintext
            try:
                head_doc = nlp(article_headline)
                ner_outputs_head.append(
                    [[ent.text, ent.start_char, ent.end_char, ent.label_]
                     for ent in head_doc.ents])
                main_doc = nlp(article_text)
                ner_outputs_main.append(
                    [[ent.text, ent.start_char, ent.end_char, ent.label_]
                     for ent in main_doc.ents])
            except Exception as e:
                logger.error(e)
                pass
            else:
                pickle_obj_head["index"].append(index)
                pickle_obj_head["ner_output"].append(ner_outputs_head)
                pickle.dump(pickle_obj_head, file=open(
                    f"./data/processed/ner/ner_{region}_headline.pickle", "wb"))
                
                pickle_obj_head["index"].append(index)
                pickle_obj_main["ner_output"].append(ner_outputs_main)
                pickle.dump(pickle_obj_main, file=open(
                    f"./data/processed/ner/ner_{region}_main.pickle", "wb"))
    except Exception as e:
        logger.error(e)
        pass

if __name__ == "__main__":
    regions = ["UK", "US", "MiddleEast"]
    for region in regions:
        run_spacy_ner(
            f"./data/processed/{region}.csv", region)
