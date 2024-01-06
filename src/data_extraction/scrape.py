from newsplease import NewsPlease, NewsArticle
import json

def get_data(url: str) -> NewsArticle:
    """Retrieve text of article given url

    Args:
        url (str): url to get data from

    Returns:
        NewsPlease.from_url: object of type
    """
    article = NewsPlease.from_url(url)
    return article

if __name__ == "__main__": 
    url = "https://www.theguardian.com/world/2023/oct/07/israel-strikes-back-after-massive-palestinian-attack"
    article = get_data(url)
    article_json = json.loads(article)