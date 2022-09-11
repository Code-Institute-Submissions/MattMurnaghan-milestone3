""" - Milestone 3 -
Author: Matthew Murnaghan
Date: 12/09/2022

This program is created to manipulate and update numerical data
stored within a google sheet using the gspread and google-auth
APIs.
"""
import plotext as pt
import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
sales = SHEET.worksheet('sales')


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

