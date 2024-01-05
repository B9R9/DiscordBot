from utils.utils_api import load_api_config
from requests_oauthlib import OAuth2Session

async def test42(ctx):
    """Test the 42 API."""

    api_config = load_api_config('config/config.yml', 'FT')
    if api_config is None:
        print("Configuration for 42 not found or an error occurred while loading the configuration.")
        return
    UID = api_config.get('uid')
    SECRET = api_config.get('secret')
    API_BASE_URL = api_config.get('endpoint')
    client = OAuth2Session(client_id=UID, token_endpoint_auth_method='client_secret_post')
    response = client.get(f'{API_BASE_URL}/v2/users/briffard')
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f'Error: {response.status_code}')