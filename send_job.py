from writer import PostgresWriter
import argparse
from datetime import datetime
from pprint import pprint
import stomp
from dotenv import load_dotenv
import os

def comma_separated_list(value):
    """
    A custom type function for argparse to handle comma-separated strings
    and return them as a list of stripped strings.
    """
    # Split the string by commas and strip any leading/trailing whitespace from each item.
    return [item.strip() for item in value.split(',')]

def parse_cli_arguments():
    """
    Parses command-line arguments for categories, start date, and end date.
    
    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    # Create the top-level parser. This object will hold all the argument definitions.
    parser = argparse.ArgumentParser(
        description="A script to process data based on categories and a date range.",
        formatter_class=argparse.RawTextHelpFormatter # Use this to format the help text correctly.
    )

    # Add the '--categories' argument.
    # nargs='+' means it expects one or more values. These values will be stored in a list.
    parser.add_argument(
        '--categories',
        type=comma_separated_list,
        required=True,
        help="""\
Specify one or more categories.
Example: --categories sports news
"""
    )
    
    # Add the '--start-date' argument.
    # A single string is expected here.
    parser.add_argument(
        '--start-date',
        type=str,
        required=True,
        help="""\
The start date of the range in YYYY-MM-DD format.
Example: --start-date 2023-01-01
"""
    )

    # Add the '--end-date' argument.
    # Similar to start-date, a single string is expected.
    parser.add_argument(
        '--end-date',
        type=str,
        required=True,
        help="""\
The end date of the range in YYYY-MM-DD format.
Example: --end-date 2023-03-31
"""
    )

    # Parse the arguments from the command line.
    # This function automatically handles validation and displays help messages if needed.
    args = parser.parse_args()

    return args

def validate_dates(start_date_str, end_date_str):
    """
    Validates that the provided date strings are in a valid format and
    that the start date is not after the end date.
    """
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Error: Date format is invalid. Please use YYYY-MM-DD.")
        return None, None

    if start_date > end_date:
        print("Error: The start date cannot be after the end date.")
        return None, None
    
    return start_date, end_date

if __name__ == "__main__":
    load_dotenv()
    arguments = parse_cli_arguments()
    writer = PostgresWriter(os.getenv("db_conn"))    
    conn = stomp.Connection([(os.getenv("stomp_conn_host"), os.getenv("stomp_conn_port"))], heartbeats=(5000,0))    
    conn.connect(os.getenv("stomp_user"),os.getenv("stomp_pw"),wait=True)

    print(arguments)
    rows = writer.retrive_categories(arguments.categories, arguments.start_date+" 00:00:00", arguments.end_date+" 00:00:00", has_webcontent=False)
    print("Retrieved rows:" + str(len(rows)))
    for r in rows:
        conn.send(
            destination='/queue/test',
            body=f"{r[0]},{r[2]}",
            headers={'content-type': 'text/plain', 
                     'persistent': 'true',
                     'delivery-mode': '2',
                     'receipt': 'message-receipt',
                     'activemq.subscriptionName': 'test-subscription'}
        )
    conn.disconnect()