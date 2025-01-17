import requests
from pprint import pprint

from consts import api_table_a


start_date = '2025-01-01'
end_date = '2025-01-03'

response = requests.get(f'{api_table_a}/{start_date}/{end_date}')

pprint(response.json())
