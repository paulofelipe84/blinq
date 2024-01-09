#!/usr/bin/env python3
"""
API Data Viewer for Blinq Interview

This script allows the user to fetch data from a specified API endpoint, 
filter the results based on provided parameters, and display the results 
in different formats (list or graph).

Requirements:
- Python 3.x
- Packages: requests, pandas, plotext (Install via `pip install -r requirements.txt`)

Usage:
- Run the script with necessary arguments. Example:
  `python business_names.py --display graph`

Author: Paulo Barbosa
Date: 9-JAN-2023
"""

import requests
import pandas as pd
import plotext as plt
import argparse

def fetch_data(
    registration_date_from,
    registration_date_to, 
    business_name, 
    business_name_similar_to, 
    limit, 
    display_format
):
    """
    Fetch data from the API.

    Args:
    - endpoint (str): The API endpoint URL.
    

    Returns:
    - dict: JSON response from the API.

    Raises:
    - Exception: If the API request fails.
    """
    
    # Parse query
    query = 'SELECT "BN_NAME", "BN_STATUS", "BN_REG_DT", "BN_CANCEL_DT", "BN_RENEW_DT", "BN_STATE_NUM", "BN_STATE_OF_REG", "BN_ABN" from "55ad4b1c-5eeb-44ea-8b29-d410da431be3" WHERE 1=1'
    
    if registration_date_from:
        query += f""" AND TO_DATE("BN_REG_DT", 'DD/MM/YYYY') >= TO_DATE('{registration_date_from}', 'DD/MM/YYYY')"""

    if registration_date_to:
        query += f""" AND TO_DATE("BN_REG_DT", 'DD/MM/YYYY') <= TO_DATE('{registration_date_to}', 'DD/MM/YYYY')"""

    if business_name:
        query += f""" AND REGEXP_REPLACE(UPPER("BN_NAME"), '^\\s*(.*?)\\s*$', '\\1') = UPPER('{business_name}')"""
    elif business_name_similar_to:
        query += f""" AND REGEXP_REPLACE(UPPER("BN_NAME"), '^\\s*(.*?)\\s*$', '\\1') ILIKE '%{business_name_similar_to}%'"""

    query += f' LIMIT {limit}'

    endpoint = 'https://data.gov.au/data/api/3/action/datastore_search_sql'
    response = requests.get(endpoint, params={"sql": query})
    if response.status_code == 200:
        return response.json()['result']['records']
    else:
        raise Exception(f"Error fetching data: {response.json()}")

def display_data_as_table(data):
    """
    Display data as a list.

    Args:
    - data (list): Data to be displayed.
    """

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame as a table
    print(df.to_markdown(index=False))

def display_data_as_graph(data):
    """
    Display data as a graph.

    Args:
    - data (list): Data to be displayed.
    """
    df = pd.DataFrame(data)

    # Convert 'BN_REG_DT' to datetime
    df['BN_REG_DT'] = pd.to_datetime(df['BN_REG_DT'], dayfirst=True)

    # Group by month/year and count registrations
    df['month_year'] = df['BN_REG_DT'].dt.to_period('M')
    registration_counts = df.groupby('month_year').size()

    # Plotting
    x_values = range(len(registration_counts))  # Numeric x-axis values
    y_values = registration_counts.values

    plt.plot(x_values, y_values)
    plt.title("Business Registration Trend Over Time")
    plt.xlabel("Time (Month-Year)")
    plt.ylabel("Number of Registrations")

    # Setting custom x-axis labels to represent the dates
    x_labels = registration_counts.index.astype(str)
    plt.xticks(x_values, x_labels)
    plt.show()

def main():
    """
    Main function to parse arguments and handle the tool's flow.
    """
    parser = argparse.ArgumentParser(description="API Data Viewer")

    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('--registration_date_from', type=str, help='Initial date (DD/MM/YYYY) of a range of business registration dates.')
    parser.add_argument('--registration_date_to', type=str, help='Final date (DD/MM/YYYY) of a range of business registration dates.')
    group.add_argument('--business_name', type=str, help='Name of the business to be searched (exact match).')
    group.add_argument('--business_name_similar_to', type=str, help='Text for a search on similar business names.')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of records in the results. Default is 10.')
    parser.add_argument('--display_format', type=str, default='table', choices=['table', 'graph'], help='Display format')
    
    args = parser.parse_args()

    try:
        data = fetch_data(
            args.registration_date_from,
            args.registration_date_to,
            args.business_name, 
            args.business_name_similar_to, 
            args.limit, 
            args.display_format
        )

        if args.display_format == 'table':
            display_data_as_table(data)
        elif args.display_format == 'graph':
            display_data_as_graph(data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
