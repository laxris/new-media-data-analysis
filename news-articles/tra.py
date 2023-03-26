import sys
import json
import csv
from typing import List, Dict, Any
import trafilatura
from tqdm import tqdm


def process_url(url: str, basepath: str) -> None:
    """
    Process a given URL and extract the article's information using the Trafilatura library.
    Save the extracted information as a JSON file and append the data to a CSV file.

    :param url: The URL of the news article to be processed.
    :type url: str
    :param basepath: The base path where the JSON and CSV files will be saved.
    :type basepath: str
    :return: None
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        result = trafilatura.extract(downloaded, output_format='json', with_metadata=True)
        article = json.loads(result)

        # Write JSON file
        with open(basepath + article['title'].replace(" ", "_") + '.json', 'w', encoding="utf-8") as outfile:
            content = json.dumps(article, indent=4, sort_keys=True, default=str, ensure_ascii=False)
            outfile.write(content)

        # Get article fields for CSV
        csv_fields = [
            'author', 'date', 'description', 'text', 'title', 'url', 'original_url'
        ]

        # Write CSV file
        with open(basepath + 'articles.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow({k: article[k] if k in article else url for k in csv_fields})

    except Exception as e:
        print(f'Error processing {url}: {e}')
        with open(basepath + 'errors.txt', 'a', encoding='utf-8') as errorfile:
            errorfile.write(f'{url} | {e}\n')

def main(url_list: List[str], basepath: str) -> None:
    # Create the CSV header
    with open(basepath + 'articles.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'author', 'date', 'description', 'text', 'title', 'url', 'original_url'
        ])
        writer.writeheader()

    # Process URLs from the list
    for url in tqdm(url_list):
        process_url(url, basepath)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py <url_list_file>')
        sys.exit(1)

    basepath = '/home/chris/sara/'
    url_list_file = sys.argv[1]

    with open(url_list_file, 'r', encoding='utf-8') as f:
        url_list = [line.strip() for line in f if line.strip()]

    main(url_list, basepath)
