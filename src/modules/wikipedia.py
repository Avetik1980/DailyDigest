import requests
import datetime
import random


def get_random_wikipedia_article():
    # Get the current date
    today = datetime.date.today()

    # Format the date as required by the Wikipedia API
    date_str = today.strftime("%B_%d")

    # Construct the URL for the Wikipedia API
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={date_str}&format=json"

    # Send a GET request to the Wikipedia API and get the response as JSON
    response = requests.get(url).json()

    # Extract the search results from the response
    search_results = response["query"]["search"]

    # Get a random article from the search results
    random_article = random.choice(search_results)

    # Get the title and page ID of the random article
    article_title = random_article["title"]
    article_id = random_article["pageid"]

    # Construct the link to the full article
    article_link = f"https://en.wikipedia.org/?curid={article_id}"

    # Construct the article data dictionary
    article_data = {'Article': article_title, 'Link': article_link}

    # Return the article data dictionary
    return article_data
