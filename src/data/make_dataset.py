import json
import glob
import logging
import pandas as pd

def data_compactor(data_dir: str) -> None:
    """Read files from dir and combine into a dataframe

    Args:
        data_dir (str): name of sub folder to extract data from 

    Returns:
        None: writes the dataframe to a csv file
    """
    data_list = []
    try:
        for name in glob.glob(f"../data/raw/{data_dir}/*.json"):
            article = json.load(open(name,'r'))
            data_list.append(article)
    except FileNotFoundError as e: 
        logging.error(f"File not found: {e}")
    else:   
        df = pd.DataFrame(data_list)
        req_cols = ['description', 'maintext', 'source_domain', 'title', 'url', 'language', 'date_publish']
        df = df[req_cols]
        df.to_csv(f"../data/processed/{data_dir}.csv", index=False)
    return

if __name__ == "__main__":
    data_compactor("UK")
    data_compactor("MiddleEast")
    data_compactor("US")
