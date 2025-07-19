import requests
import json
import time
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

INPUT_FILENAME = "leetcode_algorithms_raw.json"
OUTPUT_FILENAME = "leetcode_algorithms_processed.json"

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
GRAPHQL_REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
GRAPHQL_QUERY = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    content
    difficulty
  }
}
"""

REQUEST_DELAY_SECONDS = 0.7
REQUEST_TIMEOUT_SECONDS = 20
SAVE_PROGRESS_INTERVAL = 100

def clean_html_description(html_content):
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    plain_text = soup.get_text()
    normalized_text = " ".join(plain_text.split())

    example_match = re.search(r'Example 1:', normalized_text, re.IGNORECASE)
    constraints_match = re.search(r'Constraints:', normalized_text, re.IGNORECASE)

    truncation_index = -1
    if example_match:
        truncation_index = example_match.start()
    if constraints_match:
        if truncation_index == -1 or constraints_match.start() < truncation_index:
            truncation_index = constraints_match.start()

    if truncation_index != -1:
        return normalized_text[:truncation_index].strip()
    return normalized_text.strip()

def load_problem_metadata():
    try:
        with open(INPUT_FILENAME, "r", encoding="utf-8") as file:
            all_problems = json.load(file)
        
        non_premium_problems = [
            problem for problem in all_problems if not problem.get("paid_only", False)
        ]
        print(f"Loaded {len(non_premium_problems)} non-premium problems from '{INPUT_FILENAME}'.")
        return non_premium_problems
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILENAME}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_FILENAME}'.")
        return None

def process_and_fetch_details(problem_list):
    processed_problems = []
    
    print(f"Starting to fetch details for {len(problem_list)} problems...")

    for index, problem_meta in enumerate(tqdm(problem_list, desc="Fetching Descriptions")):
        slug = problem_meta.get("stat", {}).get("question__title_slug")
        if not slug:
            tqdm.write(f"Skipping a problem due to missing slug: {problem_meta}")
            continue

        payload = {
            "query": GRAPHQL_QUERY,
            "variables": {"titleSlug": slug}
        }

        try:
            response = requests.post(LEETCODE_GRAPHQL_URL, json=payload, headers=GRAPHQL_REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            graphql_data = response.json()

            question_details = graphql_data.get("data", {}).get("question")

            if question_details and question_details.get("content"):
                cleaned_description = clean_html_description(question_details["content"])
                if cleaned_description:
                    processed_problems.append({
                        "id": question_details["questionFrontendId"],
                        "title": question_details["title"],
                        "difficulty": question_details["difficulty"],
                        "description": cleaned_description,
                        "url": f"https://leetcode.com/problems/{slug}/"
                    })

        except requests.exceptions.RequestException as error:
            tqdm.write(f"Network error for slug '{slug}': {error}")
        except Exception as error:
            tqdm.write(f"An unexpected error occurred for slug '{slug}': {error}")

        time.sleep(REQUEST_DELAY_SECONDS)

        if (index + 1) % SAVE_PROGRESS_INTERVAL == 0 and len(problem_list) > SAVE_PROGRESS_INTERVAL:
            with open(OUTPUT_FILENAME, "w", encoding="utf-8") as file:
                json.dump(processed_problems, file, indent=4, ensure_ascii=False)
            tqdm.write(f"Progress saved. {len(processed_problems)} problems processed.")

    return processed_problems

def main():
    problem_metadata_list = load_problem_metadata()
    if not problem_metadata_list:
        return

    final_problem_data = process_and_fetch_details(problem_metadata_list)

    try:
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            json.dump(final_problem_data, file, indent=4, ensure_ascii=False)
        print(f"\nProcessing complete. Saved {len(final_problem_data)} problems to '{OUTPUT_FILENAME}'.")
    except IOError as error:
        print(f"Could not write final data to file '{OUTPUT_FILENAME}': {error}")

if __name__ == "__main__":
    main()
