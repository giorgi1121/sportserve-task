import pandas as pd


def create_addresses_table(conn):
    """Create the addresses table."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses (
                id SERIAL PRIMARY KEY,
                city TEXT,
                street_name TEXT,
                street_address TEXT,
                zip_code TEXT,
                state TEXT,
                country TEXT,
                latitude FLOAT,
                longitude FLOAT
            );
        """
        )


def create_employment_table(conn):
    """Create the employment table."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employment (
                id SERIAL PRIMARY KEY,
                title TEXT,
                key_skill TEXT
            );
        """
        )


def create_subscriptions_table(conn):
    """Create the subscriptions table."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                plan TEXT,
                status TEXT,
                payment_method TEXT,
                term TEXT
            );
        """
        )


def create_users_table(conn):
    """Create the users table with foreign key references."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                uid UUID UNIQUE,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                email TEXT,
                avatar TEXT,
                gender TEXT,
                phone_number TEXT,
                social_insurance_number TEXT,
                date_of_birth DATE,
                credit_card_number TEXT,
                address_id INT,
                employment_id INT,
                subscription_id INT,
                FOREIGN KEY (address_id) REFERENCES addresses(id),
                FOREIGN KEY (employment_id) REFERENCES employment(id),
                FOREIGN KEY (subscription_id) REFERENCES subscriptions(id)
            );
        """
        )


def create_tables(conn):
    """Create all normalized tables by invoking modular table creation functions."""
    create_addresses_table(conn)
    create_employment_table(conn)
    create_subscriptions_table(conn)
    create_users_table(conn)
    conn.commit()
    print("Tables created successfully.")


def insert_address(cursor, row):
    """Insert an address and return its generated id."""
    query = """
        INSERT INTO addresses (city, street_name, street_address, zip_code, state, country, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(
        query,
        (
            row["address.city"],
            row["address.street_name"],
            row["address.street_address"],
            row["address.zip_code"],
            row["address.state"],
            row["address.country"],
            row["address.coordinates.lat"],
            row["address.coordinates.lng"],
        ),
    )
    return cursor.fetchone()[0]


def insert_employment(cursor, row):
    """Insert employment data and return its generated id."""
    query = """
        INSERT INTO employment (title, key_skill)
        VALUES (%s, %s) RETURNING id;
    """
    cursor.execute(query, (row["employment.title"], row["employment.key_skill"]))
    return cursor.fetchone()[0]


def insert_subscription(cursor, row):
    """Insert subscription data and return its generated id."""
    query = """
        INSERT INTO subscriptions (plan, status, payment_method, term)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(
        query,
        (
            row["subscription.plan"],
            row["subscription.status"],
            row["subscription.payment_method"],
            row["subscription.term"],
        ),
    )
    return cursor.fetchone()[0]


def insert_user(cursor, row, address_id, employment_id, subscription_id):
    """Insert a user record using the given foreign key ids."""
    query = """
        INSERT INTO users (uid, password, first_name, last_name, username, email, avatar, gender,
                           phone_number, social_insurance_number, date_of_birth, credit_card_number,
                           address_id, employment_id, subscription_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(
        query,
        (
            row["uid"],
            row["password"],
            row["first_name"],
            row["last_name"],
            row["username"],
            row["email"],
            row["avatar"],
            row["gender"],
            row["phone_number"],
            row["social_insurance_number"],
            row["date_of_birth"],
            row["credit_card.cc_number"],
            address_id,
            employment_id,
            subscription_id,
        ),
    )


def load_normalized_data(conn, csv_file):
    """Read CSV file and insert normalized data into the database."""
    df = pd.read_csv(csv_file)
    try:
        with conn.cursor() as cursor:
            for index, row in df.iterrows():
                # Insert data into addresses, employment, and subscriptions tables at first
                address_id = insert_address(cursor, row)
                employment_id = insert_employment(cursor, row)
                subscription_id = insert_subscription(cursor, row)
                # Insert user records with foreign key references
                insert_user(cursor, row, address_id, employment_id, subscription_id)
        conn.commit()
        print("Data loaded successfully into normalized tables.")
    except Exception as e:
        conn.rollback()
        print("Error loading data:", e)
