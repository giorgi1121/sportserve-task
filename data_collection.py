import time

import pandas as pd
import requests

from util import get_csv_filepath

API_URL = "https://random-data-api.com/api/v2/users?size={batch_size}&response_type=json"
MAX_RETRIES = 5
INITIAL_DELAY = 0.5  # Starting delay for exponential backoff


def fetch_users_sync(url, delay=INITIAL_DELAY):
    """Fetch users synchronously, handling rate limits with exponential backoff."""
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Rate limited
            delay = min(delay * 2, 10)
            print(
                f"Rate limited. Retrying in {delay:.2f}s (Attempt {attempt}/{MAX_RETRIES})..."
            )
            time.sleep(delay)
        else:
            print(f"Error fetching data: Status code {response.status_code}")
            return []
    print("Max retries reached. Skipping request.")
    return []


def fetch_random_users(total=1000, batch_size=100):
    """Fetch users synchronously, handling API rate limits."""
    users = []
    num_batches = total // batch_size
    url = API_URL.format(batch_size=batch_size)

    for i in range(num_batches):
        batch_users = fetch_users_sync(url)
        users.extend(batch_users)
        print(f"Fetched batch {i + 1}/{num_batches} with {len(batch_users)} users.")

    print(f"Total users fetched: {len(users)}")
    return users


def save_users_to_csv(users, filename="random_users.csv"):
    """Normalize nested JSON and save to CSV."""
    df = pd.json_normalize(users)
    users_csv_path = get_csv_filepath(filename)
    df.to_csv(users_csv_path, index=False)
    print(f"Saved {len(df)} users to {filename}")


if __name__ == "__main__":
    users = fetch_random_users(total=1000, batch_size=100)
    save_users_to_csv(users)
