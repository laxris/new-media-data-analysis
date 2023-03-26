import os
import openai
import argparse
import csv
from typing import List, Tuple


openai.api_key = "<key> or load it from your .env file"

# restart_sequence = "\n"

def process_files(promptfile: str, query_file: str) -> List[List[str]]:
    """
    Process two input files and return the combined CSV data as a list of lists.

    Args:
        prompt (str): The path to the input file containing the prompt.
        query_file (str): The path to the input file containing the queries.

    Returns:
        List[List[str]]: The combined CSV data as a list of lists.
    """

    totals = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
    responses = []

    with open(promptfile) as fh:
      prompt = fh.read()

    with open(query_file) as fh:
      queries = fh.readlines()

      for query in queries:
        json_response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a zero-shot classifier. You can answer questions the topics of news articles."},
                {"role": "user", "content": prompt + "\n" + query},
                #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                #{"role": "user", "content": "Where was it played?"}
            ]
        )


        cats = json_response["choices"][0]["message"]["content"].split("\n")
        print(len(cats))
        responses.append(json_response["choices"][0]["message"]["content"].split("\n"))

        usage = json_response["usage"]
        completion_tokens = usage["completion_tokens"]
        prompt_tokens = usage["prompt_tokens"]
        total_tokens = usage["total_tokens"]

        # Update the running totals
        totals["completion_tokens"] += completion_tokens
        totals["prompt_tokens"] += prompt_tokens
        totals["total_tokens"] += total_tokens

    return responses, totals


def main():
    """
    Parse command line arguments and call the process_files() function to process the input files
    and write the output CSV file.
    """
    parser = argparse.ArgumentParser(description='Process two input files and output a CSV file.')
    parser.add_argument('prompt', type=str, default='prompt.txt', nargs='?', help='the second input file (default: prompt.txt)')
    parser.add_argument('queries', type=str, default='inputs.csv', nargs='?', help='the first input file (default: inputs.csv)')

    parser.add_argument('result', type=str, default='result.csv', nargs='?', help='the output file (default: result.csv)')
    
    args = parser.parse_args()
    
    # Call the process_files function passing the input files
    processed_csv_data, totals = process_files(args.prompt, args.queries)
    print(processed_csv_data)

    with open(args.result, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the processed CSV data to the output file
        writer.writerows(processed_csv_data)
    
    print(f"Total tokens used: {totals['total_tokens']}")
    print(f"Total cost: {totals['total_tokens'] / 1000 * 0.0002}")

    
if __name__ == '__main__':
    main()