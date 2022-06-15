# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports...
import requests

# Local imports...
from project.constants import BASE_URL



def get_users_data():
    response = requests.get(BASE_URL)
    if response.ok:
        return response
    else:
        return None

# def get_uncompleted_users_data():
#     response = get_users_data()
#     if response is None:
#         return []
#     else:
#         users_data = response.json()
#         return [todo for todo in users_data if todo.get('completed') == False]