import yaml

def load_api_config(file_path, api_name):
    """
    Load API configuration from a YAML file and retrieve information for a specific API.

    Parameters:
        file_path (str): The path to the YAML configuration file.
        api_name (str): The name of the API to retrieve configuration for.

    Returns:
        dict or None: A dictionary containing the API configuration if found, otherwise None.
    """
    # Open the YAML file
    with open(file_path, 'r') as config_file:
        try:
            # Load YAML data from the file
            config_data = yaml.safe_load(config_file)

            # Check if data is loaded successfully
            if config_data:
                # Get the list of API configurations from the 'apis' key, default to an empty list if 'apis' is not present
                apis_info = config_data.get('apis', [])

                # Iterate through the list of APIs to find the one with the specified name
                for api in apis_info:
                    if api.get('name') == api_name:
                        return api  # Return the API configuration if found

                # If the loop completes without finding the API, print a message
                print(f"API '{api_name}' not found in the config file.")
                return None
        except yaml.YAMLError as exc:
            # Handle YAML loading errors
            print(f"Error loading YAML file: {exc}")
            return None