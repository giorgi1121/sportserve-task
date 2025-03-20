import os

# Define default directories for CSV and PNG files.
OUTPUT_CSV_DIR = "output_csv"
OUTPUT_PNG_DIR = "output_png"


def create_output_dir(directory):
    """
    Create the directory if it does not exist.

    Parameters:
        directory (str): The directory path.

    Returns:
        str: The directory path.
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def get_output_filepath(filename, directory):
    """
    Construct a full file path in the specified directory.

    Parameters:
        filename (str): The name of the file.
        directory (str): The output directory.

    Returns:
        str: The full file path.
    """
    create_output_dir(directory)
    return os.path.join(directory, filename)


def get_csv_filepath(filename):
    """
    Get a file path for a CSV file in the CSV output directory.

    Parameters:
        filename (str): The CSV file name.

    Returns:
        str: The full CSV file path.
    """
    return get_output_filepath(filename, OUTPUT_CSV_DIR)


def get_png_filepath(filename):
    """
    Get a file path for a PNG file in the PNG output directory.

    Parameters:
        filename (str): The PNG file name.

    Returns:
        str: The full PNG file path.
    """
    return get_output_filepath(filename, OUTPUT_PNG_DIR)
