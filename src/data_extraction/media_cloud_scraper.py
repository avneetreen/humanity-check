from newsplease import NewsPlease, NewsArticle
import json
import os
import csv
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


def extract_articles_from_csvs(filename: str):
    """Extract article objects given urls in csvs

    Args:
        filename (str): name of csv

    Returns:
        None
    """
    data = pd.read_csv(os.path.join("data/links/mediacloud",
                                    filename))
    article_count = 1
    count = 0
    for index, row in data.iterrows():
        count += 1
        link = row['url']
        try:
            article = retrieve_article_from_url(link)
            outfile_name = outfile + f"{article_count}.json"
            with open(outfile_name, 'a+', newline='\n') as f:
                json.dump(article.get_serializable_dict(), f)
                article_count += 1
                f.close()
                print(article.title)
                print(count)
        except Exception as e:
            print(e)
            continue
    return


if __name__ == "__main__":
    # for filename in os.listdir("../data/links"):
    #    print(filename)
    outfile = "data/US/"
    filename = "mc-onlinenews-mediacloud-20240201135145-content_USA.csv"
    extract_articles_from_csvs(filename)
