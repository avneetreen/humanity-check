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
        return "None"
    return article


def extract_articles_from_csvs(filename: str):
    """Extract article objects given urls in csvs

    Args:
        filename (str): name of csv

    Returns:
        None
    """
    list_of_articles = []
    # with open(os.path.join("data/links/mediacloud", filename), "r") as csvFile:
    # reader = csv.DictReader(csvFile)
    # csvFile.close()
    data = pd.read_csv(os.path.join("data/links/mediacloud",
                                    filename))
    article_count = 1
    count = 0
    for index, row in data.iterrows():
        count += 1
        link = row['url']
        try:
            article = retrieve_article_from_url(link)
            with open(f"data/US/{article_count}.json", 'a+', newline='\n') as f:
                json.dump(article.get_serializable_dict(), f)
                article_count += 1
                f.close()
                # out_file.dump(str(article.get_serializable_dict()))
                # out_file.write(str(article.get_serializable_dict()))
                # out_file.write("\n")
                print(article.title)
                print(count)
        except Exception as e:
            print("Unable to get data from: ", link)
            print("Exception: ", e)
            continue
    return


if __name__ == "__main__":
    # for filename in os.listdir("../data/links"):
    #    print(filename)
    filename = "mc-onlinenews-mediacloud-20240201135145-content_USA.csv"
    extract_articles_from_csvs(filename)
