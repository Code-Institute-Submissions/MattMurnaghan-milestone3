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

COLUMN_TITLES = 1
PROGRAM_TITLES = 5


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


def print_welcome_graphic():
    """
    Prints a welcome graphic to the terminal
    """
    print('*******************************************************')
    print('*               *******           ****                *')
    print('*               ********          ****                *')
    print('*               *********         ****                *')
    print('*               ****  ****        ****                *')
    print('*               ****   ****       ****                *')
    print('*               ****    ****      ****                *')
    print('*               ****     ****     ****                *')
    print('*               ****      ****    ****                *')
    print('*               ****       *****  ****                *')
    print('*               ****        ****  ****                *')
    print('*               ****         *********                *')
    print('*               ****          ********                *')
    print('*               ****           *******                *')
    print('*******************************************************')
    print('*******************************************************')
    print('*                                                     *')
    print('*       Welcome to the Netflix analysis tool!         *')
    print('*                                                     *')
    print('*******************************************************')


def greet_user():
    """
    Gets the users name as input in the form of a string.
    """
    has_numbers = True
    too_long = True
    character_limit = 15

    while has_numbers or too_long:
        user_name = input('Please enter your name here:\t')
        if str.isalpha(user_name):
            has_numbers = False
        if len(user_name) <= character_limit:
            too_long = False
        if has_numbers or too_long:
            print('\nThe username you have entered is invalid.')
            print('Usernames must be no longer than 15 characters')
            print('Usernames must contain only letters.\n')
            has_numbers = True
            too_long = True

    print(f'Welcome {user_name}!\n')
    print('This tool allows you to analyse data collected from')
    print('multiple netflix users over the course of the pandemic.\n')


class GoogleSheet():
    """
    This class hides any credentials to access the sheet from the global scope.
    """
    def __init__(self):
        self.data = None
        self.sheet = None
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]
        self.creds = Credentials.from_service_account_file('creds.json')
        self.scoped_creds = self.creds.with_scopes(self.scope)
        self.gspread_client = gspread.authorize(self.scoped_creds)

    def load_data(self):
        """
        This method requests data from the milestone_3_data worksheet and
        stores it in the object property, self.sheet. It then loads the
        data from the sheet into the self.data property.
        """
        try:
            print('Opening google sheet ...\n')
            self.sheet = self.gspread_client.open('milestone_3_data')
        except ValueError as error:
            print(f'Error opening sheet: {error}')
            exit(0)
        else:
            print('Sheet opened successfully.\n')

        try:
            print('Loading worksheet data ...\n')
            self.data = self.sheet.worksheet('netflix_data')
        except ValueError as error:
            print(f'Error loading worksheet data: {error}')
            exit(0)
        else:
            print('Data loaded successfully.\n')

    def get_data(self):
        """
        Returns the worksheet data when called.
        """
        if self.data is False:
            print('No data to display, please load data first.')
            print(self.data)
        else:
            return self.data


class DataManager():
    """
    This class manages the data returned from the GoogleSheet class.
    All interaction with the sheet is facilitated by different methods
    invoked from the DataManager class.
    """
    def __init__(self, sheet):
        """
        Defines the DataManager class.
        """
        self.worksheet = sheet
        self.column_titles = sheet.row_values(COLUMN_TITLES)
        self.program_titles_column = sheet.col_values(PROGRAM_TITLES)

    def print_column_titles(self):
        """
        Prints titles
        """
        pprint(self.column_titles)

    def remove_duplicates(self):
        """
        This method returns a list with duplicate values removed.
        """
        res = []
        for item in self.program_titles_column:
            if item not in res:
                res.append(item)
        return res

    def print_program_titles(self):
        """
        Prints the program titles to the terminal.
        """
        pprint(remove_duplicates((self.program_titles_column)))
        print(len(remove_duplicates((self.program_titles_column))))

    def get_selection(self):
        """
        This method asks the user to choose from a selection of data to view
        """
        # options = [
        #     'Score',
        #     'Rank',
        #     'Title',
        #     'Type',
        #     'Release Date'
        #     ]
        print('What data would you like to view?')
        i = 1
        for title in self.column_titles:
            if i < 10:
                print(f'{i} : {title}')
            else:
                print(f'{i}: {title}')
            i += 1
        invalid_option = True
        while invalid_option:
            data_option = input('\nPlease enter choice here: ')
            try:
                in_rng = int(data_option) in range(1, len(self.column_titles))
                if int(data_option) and in_rng:
                    invalid_option = False
                else:
                    print(f'You selected: {data_option}. Please enter choice')
                    print('between 1 and 10 inclusive:\n')
            except ValueError as error:
                print(f'Error: {error}.\nPlease enter an integer option.\n')
        print(f'You selected: {self.column_titles[int(data_option) - 1]}')
        return int(data_option) - 1

    def display_data(self, option):
        """
        This method displays the data from the column matching
        the option string passed as an argument.
        """
        RANK = 'Rank'
        W_RANK = 'Last Week Rank'
        Y_RANK = 'Year to Date Rank'

        print('display data')
        selector = self.column_titles[option]
        print(f'you have chosen: {selector}\n')
        i = 1
        if selector is RANK or W_RANK or Y_RANK:
            if selector is RANK:
                print('Would you like to see the overall rank\
                    or a rank at a certain time?')
                choices = ['Overall', 'Certain time']
                for choice in choices:
                    print(f'{i}: {choice}')
                input('Please enter here:')




            programs_column = self.program_titles_column
            ranks_column = self.worksheet.col_values(option)
            programs = programs_column[1:]
            ranks = ranks_column[1:]

            for rank, program in zip(ranks, programs):
                print(f'{program} recieved a rank of {rank}')
                
            # print(self.column_titles)
            print('selector is ' + selector)
            # print(ranks[0])
            # print(len(ranks))
            # print(programs[0])
            # print(len(programs))


def main():
    """
    Main function that holds all other function calls.
    """
    sheet = GoogleSheet()
    sheet.load_data()
    netflix_data = sheet.get_data()
    data_manager = DataManager(netflix_data)
    print_welcome_graphic()
    greet_user()
    data_option = data_manager.get_selection()
    data_manager.display_data(data_option)


main()
