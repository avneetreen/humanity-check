from newsplease import NewsPlease, NewsArticle
import json
import os 
import csv 
import logging 

def retrieve_article_from_url(url: str) -> NewsArticle:
    """Retrieve text of article given url

    Args:
        url (str): url to get data from

    Returns:
        NewsPlease.from_url: object of type
    """
    article = NewsPlease.from_url(url, timeout=4)
    return article
    
def extract_articles_from_csvs(filename: str):
    """Extract article objects given urls in csvs

    Args:
        filename (str): name of csv

    Returns:
        None
    """
    list_of_articles = []
    with open(os.path.join("../data/links/",filename), "r") as csvFile:
        reader = csv.DictReader(csvFile)
        count = 0
        out_file = open("../data/data.jsonl", 'w', newline='\n')
        for line in reader: 
            count+=1
            link = line['Link']
            try: 
                article = retrieve_article_from_url(link)
                out_file.write(str(article.get_serializable_dict()))
                out_file.write("\n")
                print(article.title)
                print(count)
            except Exception as e:
                print("Unable to get data from: ", link)
                print("Exception: ", e)
                continue
    return

    
            
    
if __name__ == "__main__": 
    for filename in os.listdir("../data/links"):
        print(filename)
        extract_articles_from_csvs(filename)