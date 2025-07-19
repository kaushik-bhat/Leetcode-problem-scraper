# Leetcode Problem Scraper 🚀

A Python scraper to fetch and process all non-premium algorithm problems from LeetCode. It generates a clean JSON file containing the problem ID, title, difficulty, a cleaned description, and URL.


## How It Works

The scraper operates in two distinct stages to ensure reliability and organization. You must run the scripts in order.

### 1. `fetch.py`
This is the first script you run. Its sole purpose is to connect to the LeetCode API and download the complete list of raw metadata for all algorithm problems.

-   **Input:** None.
-   **Action:** Fetches a large JSON object containing data for every algorithm problem.
-   **Output:** Creates a file named `leetcode_algorithms_raw.json`. This file acts as the input for the next step.

### 2. `process.py`
This script does the main work. It reads the raw data from the first step, filters out what's not needed, and then fetches the detailed content for each problem.

-   **Input:** `leetcode_algorithms_raw.json`.
-   **Action:**
    1.  Reads the input file and filters out all premium-only problems.
    2.  For each non-premium problem, it makes a new request to LeetCode's GraphQL API to get detailed information, including the full HTML content.
    3.  It cleans the HTML content, removing everything after "Example 1:" or "Constraints:".
    4.  It structures the cleaned data into a simple format.
-   **Output:** Creates the final, clean dataset named `leetcode_algorithms_processed.json`.

---

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.7+

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Leetcode-problem-scraper.git]
    cd Leetcode-problem-scraper
    ```
    *(Replace `your-username` with your actual GitHub username and obviously do  not include the square brackets)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    The project dependencies are listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

Run the scripts from your terminal in the correct order.

1.  **First, run `fetch.py` to get the raw data:**
    ```bash
    python fetch.py
    ```
    *This should be very quick.*

2.  **Next, run `process.py` to generate the final dataset:**
    ```bash
    python process.py
    ```
    *This will take a significant amount of time as it fetches each problem one by one with a delay. A progress bar will show the status.*

Once complete, you will find the `leetcode_algorithms_processed.json` file in your project directory.

---

## Output Data Structure

The final `leetcode_algorithms_processed.json` file will be an array of JSON objects, with each object structured like this:

```json
[
    {
        "id": "1",
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
        "url": "[https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/)"
    },
    {
        "id": "2",
        "title": "Add Two Numbers",
        "difficulty": "Medium",
        "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.",
        "url": "[https://leetcode.com/problems/add-two-numbers/](https://leetcode.com/problems/add-two-numbers/)"
    }
]
```

---

## Customization Guide

You can easily adapt the scripts to your specific needs.

### Fetching Different Problem Categories

By default, `fetch.py` gets "algorithms". You can change this to **"database"**, **"shell"**, or **"all"**.

-   **File to edit:** `fetch.py`
-   **What to change:** Modify the `LEETCODE_ALGORITHMS_URL` variable.

    ```python
    # To get only database problems:
    LEETCODE_ALGORITHMS_URL = "[https://leetcode.com/api/problems/database/](https://leetcode.com/api/problems/database/)"

    # To get all problems of all types:
    LEETCODE_ALGORITHMS_URL = "[https://leetcode.com/api/problems/all/](https://leetcode.com/api/problems/all/)"
    ```

### Fetching More (or Different) Details

By default, `process.py` fetches the ID, title, content, and difficulty. You can get much more data, such as topic tags or code snippets.

-   **File to edit:** `process.py`
-   **What to change:** Modify the `GRAPHQL_QUERY` string. Add or remove fields as needed.

    ```python
    # Example: Also fetch topic tags and available code snippets
    GRAPHQL_QUERY = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        content
        difficulty
        # --- Add new fields below ---
        topicTags {
          name
          slug
        }
        codeSnippets {
          lang
          langSlug
          code
        }
      }
    }
    """
    ```
    *Remember to also update the final JSON object in the `process_and_fetch_details` function to include this new data.*

---

## ⚖️ Disclaimer

This project is intended for **educational and personal use only**. The data scraped is the intellectual property of LeetCode. Please be respectful of their terms of service.

-   **Do not use this for any commercial purposes.**
-   **Do not spam their servers.** The script includes a respectful delay between requests by default. Please do not remove or significantly lower this delay.
