from newsplease import NewsPlease, NewsArticle
import json
import os
import logging
import pandas as pd


def retrieve_article_from_url(url: str) -> NewsArticle:
    """Retrieve text of article given url

    Args:
        url (str): url to get data from

    Returns:
        NewsPlease.from_url: object of type
    """
    try:
        article = NewsPlease.from_url(url, timeout=4)
    except Exception as e:
        print(e)
    return article


def extract_articles_from_csvs(filepath: str, outfolder: str):
    """Extract article objects given urls in csvs

    Args:
        filepath (str): name of csv
        outfolder (str): name of folder to save articles

    Returns:
        None
    """
    data = pd.read_csv(filepath)
    data = data[data.language == "en"]
    
    article_count = 1
    count = 0
    for _, row in data.iterrows():
        count += 1
        link = row['url']
        try:
            article = retrieve_article_from_url(link)
            outfile_name = outfolder + f"{article_count}.json"
            with open(outfile_name, 'a+', newline='\n') as f:
                json.dump(article.get_serializable_dict(), f)
                article_count += 1
                f.close()
                print(article.title)
                print(count)
        except Exception as e:
            print(e)
            continue
    return None

if __name__ == "__main__":
    reg = "US"
    outfolder = f"data/raw/{reg}/"
    os.mkdir(outfolder)
    filepath = f"data/links/WayBackMachine/filtered/{reg}.csv"
    extract_articles_from_csvs(filepath, outfolder)
