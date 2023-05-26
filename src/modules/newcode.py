import requests
import feedparser
from prettytable import PrettyTable


def get_new_product_announcements(client_id, client_secret):
    producthunt_url = 'https://api.producthunt.com/v2/api/graphql'
    query = """
    query {
        posts(first: 10) {
            edges {
                node {
                    name
                    tagline
                    website
                }
            }
        }
    }
    """

    # Request an access token using the client credentials
    token_url = 'https://api.producthunt.com/v2/oauth/token'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, headers=headers, json=data)
    access_token = response.json()['access_token']

    # Make a request to the Product Hunt API using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(producthunt_url, json={'query': query}, headers=headers)
    new_products_ph = response.json()['data']['posts']['edges']
    new_products_ph_list = [(product['node']['name'], product['node']['tagline'], product['node']['website']) for product in new_products_ph]

    return new_products_ph_list

# Get the new product announcements from Product Hunt
new_products = get_new_product_announcements('VvtRKjTiZbjSg8C3h0oQFbY3AjpIFSpeTA0wHzkppF8','KFuVZ1WbQLkSvvwr6CcJ1fSSrYUwKW_tAwpPfr1h84E')

# Create a table to display the new product announcements
table = PrettyTable(['Name', 'Tagline', 'Website'])
for product in new_products:
    table.add_row([product[0], product[1], product[2]])

# Print the table to the console
print(table)


#LaunchingNext Feed
launching_next_rss_url = 'https://feeds.feedburner.com/LaunchingNext'

feed = feedparser.parse(launching_next_rss_url)
new_products_ln = [(entry['title'], entry['link']) for entry in feed.entries[:10]]

# Create a table to display the new product announcements
table = PrettyTable(['Title', 'Link'])
for product in new_products_ln:
    table.add_row([product[0], product[1]])

# Print the table to the console
print("New products on Launching Next today:\n")
print(table)


startup_ranking_api_url = 'https://www.startupranking.com/api/startups'
params = {
    'sort': 'launch_date',
    'order': 'desc',
    'page': 1,
    'size': 10
}

response = requests.get(startup_ranking_api_url, params=params)
new_products_sr = [(startup['name'], f"https://www.startupranking.com{startup['url']}") for startup in response.json()['startups']]
new_products_sr_text = "\n\nNew products on Startup Ranking today:\n" + "\n".join([f"{product[0]} ({product[1]})" for product in new_products_sr])

print(new_products_sr_text)

"""
crunchbase_api_url = 'https://api.crunchbase.com/v3.1/products'
params = {
    'sort_order': 'desc',
    'sort_field': 'release_date',
    'page': 1,
    'items_per_page': 10
}
api_key = 'c1a267d29398d11a246c32944143c699'

response = requests.get(crunchbase_api_url, params=params, headers={'X-Crunchbase-Key': api_key})
new_products_cb = [(product['properties']['name'], product['properties']['homepage_url']) for product in response.json()['data']['items']]
new_products_cb_text = "\n\nNew products on Crunchbase today:\n" + "\n".join([f"{product[0]} ({product[1]})" for product in new_products_cb])

print(new_products_cb_text)
"""
