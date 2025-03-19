import psycopg2

import settings
from data_collection import fetch_random_users, save_users_to_csv
from database import (
    create_tables,
    fetch_users,
    load_normalized_data,
    most_common_properties,
)
from user_similarity import find_similar_users
from visualization import visualize_common_properties, visualize_groups


def main():
    """
    Main function to execute the following tasks:
    1. Fetch random users, save them to a CSV file, and load the data into a database.
    2. Query the database to analyze user similarities and build groups.
    3. Visualize the results.
    """

    # Part 1: Data Collection and Database Setup
    print("Fetching random users...")
    users = fetch_random_users(total=1000, batch_size=100)
    save_users_to_csv(users, filename="random_users.csv")

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        create_tables(conn)
        load_normalized_data(conn, "random_users.csv")
        common_props = most_common_properties(conn)
        print("Most Common Properties:", common_props)

        # Part 2: Similarity Analysis
        users_df = fetch_users(conn)
    except Exception as e:
        print(f"Database error: {e}")
        return
    finally:
        if conn:
            conn.close()

    pair_df, strong_groups, weak_groups = find_similar_users(users_df)

    # Part 3: Visualization
    visualize_groups(strong_groups, weak_groups)
    visualize_common_properties(common_props)


if __name__ == "__main__":
    main()
