""" - Milestone 3 -
Author: Matthew Murnaghan
Date: 12/09/2022

This program is created to manipulate and update numerical data
stored within a google sheet using the gspread and google-auth
APIs.
"""
from pprint import pprint
# import numpy as np
# import pandas as pd
# import gspread_pandas
import gspread
import plotext as pt
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('milestone_3_data')
sheet1 = SHEET.worksheet('sheet1')


# class program:
#     def __init__(self, )

def test_plotext():
    """
    Test function to check the output of plotext in the heroku terminal.
    This will be deleted in the final version of the code.
    """
    scale = 0.85
    y_vals = [1, 2, 3, 3, 4, 5, 6, 7, 8]
    x_vals = [1, 2, 3, 3, 4, 5, 6, 7, 8]
    pt.bar(x_vals, y_vals)
    pt.title('TEST')
    pt.plot_size(80 * scale, 24 * scale)
    pt.show()


def remove_duplicates(arr):
    """
    This function returns a list with duplicate values removed.
    """
    res = []
    for item in arr:
        if item not in res:
            res.append(item)
    return res


def main():
    """
    Main function that holds all other function calls.
    """
    # print('This is the main function')
    # all_vals = sheet1.get_all_values()
    column_titles = sheet1.row_values(1)
    program_titles_column = sheet1.col_values(5)
    pprint(column_titles)
    individual_titles = remove_duplicates(program_titles_column)
    # pprint(individual_titles)
    # corrupt_titles = find_corrupt_titles(individual_titles)
    # pprint(corrupt_titles)


# main()
test_plotext()