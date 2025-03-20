# Random User Analysis

## Overview
This project fetches random user data from [Random Data API](https://random-data-api.com/documentation), processes and stores it in a PostgreSQL database, analyzes user similarities, and visualizes the results using Matplotlib.

## Features
- Fetches 1000 random users in JSON format.
- Saves user data to a CSV file.
- Loads the data into a PostgreSQL database using a normalized schema.
- Identifies the most common user properties.
- Finds similarities between users using fuzzy matching and geolocation.
- Visualizes results using Matplotlib.

---

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL
- Docker (optional, for running PostgreSQL in a container)


# Development Environment Set Up

## Start project local
### Clone Project to your local environment
```bash
  git clone https://github.com/giorgi1121/sportserve-task.git
```
or with SSH
```bash
  git clone git@github.com:giorgi1121/sportserve-task.git
```

### Create a Virtual Environment

On Linux use commands:
```sh
python -m venv venv
source venv/bin/activate
```

On Windows use commands:
```sh
python -m venv venv
venv\\Scripts\\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Setup Environment Variables
create env directory, copy files from env-pattern dir and fill the
variables with appropriate values.

Create a `.env.dev` file inside the `env/` directory:
```sh
touch env/.env.dev
```
Add the following database configuration:
```sh
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
```

---

## Running the Project
### 1. Start PostgreSQL Database
If you have PostgreSQL installed locally, start it manually. Alternatively, use Docker:
```bash
  docker compose up --build
```

### 2. Run the Script
```sh
python main.py
```

---

## Project Structure
```
sportserve-task/
│── data_collection.py      # Fetches random user data and saves to CSV
│── database.py             # Defines and manages database schema
│── user_similarity.py      # Finds user similarities using fuzzy matching
│── visualization.py        # Generates visual reports using Matplotlib
│── settings.py             # Loads environment variables
│── util.py                 # Manages file paths and output directories
│── main.py                 # Main script orchestrating data processing
│── requirements.txt        # List of dependencies
│── README.md               # Documentation
│── env/.env.dev            # Environment variables (ignored in .gitignore)
│── output_csv/             # Directory for CSV files
│── output_png/             # Directory for visualization images
```

---

## Functionality Details

### **1. Data Collection (`data_collection.py`)**
- Fetches user data from the API.
- Implements exponential backoff for API rate limits.
- Saves data as a CSV file.

### **2. Database Handling (`database.py`)**
- Creates a normalized schema with separate tables for `users`, `addresses`, `employment`, and `subscriptions`.
- Inserts fetched data into the database.
- Queries the most common user properties.

### **3. User Similarity Analysis (`user_similarity.py`)**
- Uses **fuzzy string matching (FuzzyWuzzy)** for name, address, and job similarity.
- Calculates **geographic proximity** using latitude and longitude.
- Identifies **strong** and **weak** user connections.
- Saves similarity results to CSV.

### **4. Visualization (`visualization.py`)**
- Displays the **most common user properties**.
- Generates **bar charts** for **strong vs. weak user groups**.
- Saves images in `output_png/`.

---

## Future Improvements
- Optimize **database indexing** for faster queries.
- Cache Most Common Properties.
- Implement **a web interface** for interactive data visualization.

---
