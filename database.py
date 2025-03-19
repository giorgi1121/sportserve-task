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
