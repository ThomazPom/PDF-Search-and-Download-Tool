# PDF Downloader using Google Custom Search API

This script allows you to download PDFs from a specific website using Google's Custom Search API. It supports configuring search parameters, handling API secrets, and saving the downloaded files into a specified folder.
# Installation
**Clone the Repository:**

Clone the repository to your local machine.

```bash
   git clone https://github.com/yourusername/pdf-downloader.git
   cd pdf-downloader
 ```
Set Up a Virtual Environment (Optional but Recommended):
Create a virtual environment to isolate dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
 ```
Install Required Dependencies:

Install the required Python packages using pip.

 ```bash
pip install -r requirements.txt
 ```
Create Configuration and Secrets Files:

Create a .secret file in the project directory to store your API keys.

 ```json
{
  "API_KEY": "YOUR_API_KEY",
  "SEARCH_ENGINE_ID": "YOUR_SEARCH_ENGINE_ID"
}
 ```

Create a config.yaml file for default search parameters if it doesn't already exist.

 ```yaml
        query: "dont sucres"
        filetype: "pdf"
        site: "example.com"
 ```
# Usage

To run the script, use the following command:

```bash
python main.py [options]
```
# Options

    --query : The search query to use (e.g., "example query"). If not provided, the default from config.yaml is used.
    --filetype : The type of file to search for (default: pdf).
    --site : The site to target for the search. If not provided, the default from config.yaml is used.
    --secret-file : Path to the JSON file containing API secrets (default: .secret).
    --config-file : Path to the YAML configuration file (default: config.yaml).
    --dest-folder : Destination folder for downloaded files (default: downloads). If the folder does not exist, it will be created.
    --start : The index of the first result to return (default: 1).
    --stop : The index of the last result to return (default: 10000).
    --referer : The referer URL to use for the search request, ofter required by the API.
# Examples
Run with Default Configuration:
```bash
python main.py
```
Run with Custom Query and Destination Folder:
```bash
python main.py --query "specific search term" --dest-folder "my_pdfs"
 ```
Run with Custom Site and Filetype:

```bash
python main.py --site "anotherexample.com" --filetype "pdf"
```
Use a Different Secrets or Config File:

```bash
python main.py --secret-file "/path/to/my_secret.json" --config-file "/path/to/my_conf.yaml"
```