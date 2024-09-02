import argparse
import json
import os
import requests
import yaml
import logging

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("script.log"),
        logging.StreamHandler()
    ]
)

def load_secrets(secret_file):
    """
    Load secrets from the specified secret file.
    """
    logging.info(f"Loading secrets from {secret_file}")
    try:
        with open(secret_file, 'r') as file:
            secrets = json.load(file)
            logging.debug(f"Secrets loaded: {secrets}")
            return secrets
    except Exception as e:
        logging.error(f"Failed to load secrets: {e}")
        raise

def load_config(config_file):
    """
    Load the configuration from the specified config file.
    If the file doesn't exist, create it with default settings.
    """
    logging.info(f"Loading configuration from {config_file}")
    default_config = {
        'query': "dont sucres",
        'filetype': "pdf",
        'site': "example.com",
        'referer': None,
        'dest_folder': 'downloads'
    }

    if not os.path.exists(config_file):
        logging.warning(f"{config_file} does not exist. Creating with default configuration.")
        with open(config_file, 'w') as file:
            yaml.dump(default_config, file)
        return default_config

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            logging.debug(f"Configuration loaded: {config}")
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise

def save_config(config, config_file):
    """
    Save the updated configuration back to the config file.
    """
    logging.info(f"Saving updated configuration to {config_file}")
    try:
        with open(config_file, 'w') as file:
            yaml.dump(config, file)
        logging.debug(f"Configuration saved: {config}")
    except Exception as e:
        logging.error(f"Failed to save configuration: {e}")
        raise

def perform_search(query, headers, secrets, start, stop):
    """
    Perform the search using Google Custom Search API and handle pagination.
    """
    logging.info(f"Performing search from result {start} to {stop}")
    all_results = []

    for start_index in range(start, stop, 10):
        url = (
            f"https://www.googleapis.com/customsearch/v1?q={query}&cx={secrets['SEARCH_ENGINE_ID']}"
            f"&key={secrets['API_KEY']}&start={start_index}"
        )
        logging.debug(f"Requesting URL: {url}")
        try:
            response = requests.get(url, headers=headers)
            results = response.json()
            logging.debug(f"API response: {results}")

            if 'items' in results:
                all_results.extend(results['items'])
            else:
                logging.warning("No more results found or an error occurred.")
                break

        except Exception as e:
            logging.error(f"Failed to perform search: {e}")
            break

    return all_results

def download_pdfs(pdf_links, dest_folder):
    """
    Download PDF files from the given list of links into the destination folder.
    """
    logging.info(f"Downloading PDFs to {dest_folder}")
    os.makedirs(dest_folder, exist_ok=True)

    for link in pdf_links:
        try:
            logging.info(f"Downloading: {link}")
            pdf_response = requests.get(link)
            pdf_name = os.path.join(dest_folder, link.split('/')[-1])
            with open(pdf_name, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            logging.info(f"Downloaded: {pdf_name}")
        except Exception as e:
            logging.error(f"Failed to download {link}: {e}")

def main(args):
    logging.info("Starting main function")

    # Load secrets and config
    try:
        secrets = load_secrets(args.secret_file)
        config = load_config(args.config_file)
    except Exception as e:
        logging.critical(f"Critical error loading secrets or configuration: {e}")
        return

    # Update config with command-line arguments if provided
    config.update({k: v for k, v in vars(args).items() if v is not None})
    logging.debug(f"Configuration after update: {config}")

    # Save updated configuration
    save_config(config, args.config_file)

    # Prepare search query and headers
    full_query = f'"{config["query"]}" filetype:{config["filetype"]} site:{config["site"]}'
    headers = {'referer': config['referer']} if config['referer'] else {}
    logging.info(f"Search query: {full_query}")

    # Perform search and handle pagination
    search_results = perform_search(full_query, headers, secrets, args.start, args.stop)

    if not search_results:
        logging.warning("No results found.")
        return

    pdf_links = [item['link'] for item in search_results if item['link'].endswith('.pdf')]
    logging.info(f"Found {len(pdf_links)} PDF links")

    # Download PDF files
    download_pdfs(pdf_links, config['dest_folder'])

if __name__ == '__main__':
    # Set up argparse
    parser = argparse.ArgumentParser(description='Download PDFs using Google Custom Search API.')
    parser.add_argument('--query', type=str, help='The search query to use.')
    parser.add_argument('--filetype', type=str, help='The type of file to search for (default: pdf).')
    parser.add_argument('--site', type=str, help='The site to target for the search.')
    parser.add_argument('--secret-file', type=str, default='.secret', help='Path to the JSON file containing secrets.')
    parser.add_argument('--config-file', type=str, default='config.yaml', help='Path to the YAML configuration file.')
    parser.add_argument('--dest-folder', type=str, help='Destination folder for downloaded files.')
    parser.add_argument('--referer', type=str, help='Referer header for the request.')
    parser.add_argument('--start', type=int, default=1, help='Start index for search results pagination.')
    parser.add_argument('--stop', type=int, default=10000000, help='Stop index for search results pagination.')

    args = parser.parse_args()

    # Call the main function with the arguments
    main(args)
