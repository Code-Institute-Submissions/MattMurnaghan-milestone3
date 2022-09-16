""" - Milestone 3 -
Author: Matthew Murnaghan
Date: 12/09/2022

This program is created to manipulate and update numerical data
stored within a google sheet using the gspread and google-auth
APIs.
"""
from pprint import pprint
import time
import gspread
import plotext as pt
from google.oauth2.service_account import Credentials

COLUMN_TITLES = 1
PROGRAM_TITLES = 5
SCALE = 0.85
IN_DEV = True
NOT_IN_DEV = False


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
    The function provides error handling for incorrect input.
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


def get_user_input(choices, in_development):
    """
    Lists choices passed as a list argument, then requests and
    validates input from user, via the command line. It returns
    the integer value that the user selected minus 1.

    I modified this function
    with an in_development argument to highlight the future features of the
    project.

    By passing a boolean true as the second argument, a modified welcome
    screen is presented to the user, showing what features are currently
    available to them.

    Further development would allow a user to view other fields of information.
    """
    if in_development:
        i = 1
        for choice in choices:
            if i < 10:
                if i == 2:
                    print(f' {i}:  {choice}')
                else:
                    print(f' {i}:  {choice} - Not currently available')
            else:
                print(f'{i}:  {choice} - Not currently available')
            i += 1
        invalid_option = True
        length = len(choices) + 1
        while invalid_option:
            data_option = input('\nPlease enter choice here: ')
            try:
                in_rng = 2
                if int(data_option) and data_option == '2':
                    invalid_option = False
                else:
                    print(f'You selected: {data_option}.')
                    print('Please enter an available choice.\n')
            except ValueError as error:
                print(f'Error: {error}.\nPlease enter an integer option.\n')
        return int(data_option) - 1
    else:
        i = 1
        for choice in choices:
            if i < 10:
                print(f' {i}: {choice}')
            else:
                print(f'{i}: {choice}')
            i += 1
        invalid_option = True
        length = len(choices) + 1
        while invalid_option:
            data_option = input('\nPlease enter choice here: ')
            try:
                in_rng = int(data_option) in range(1, length)
                if int(data_option) and in_rng:
                    invalid_option = False
                else:
                    print(f'You selected: {data_option}. Please enter choice')
                    print(f'between 1 and {length - 1} inclusive:\n')
            except ValueError as error:
                print(f'Error: {error}.\nPlease enter an integer option.\n')
        return int(data_option) - 1


def find_average_rank(titles, data, decimal):
    """
    This function finds the average rank of netflix shows between 2020 and
    2022. It takes a list of titles and a list of ranks as arguments. It
    takes an integer value as the amount of decimal points the user wishes
    to round the rank of each program to.

    The function returns a list holding both a list of lists for each of
    the rankings for the unique program titles and a list of the unique
    program titles themselves.

    This could be refactored in the futures to find the average of any value
    passed as an argument e.g. the viewership score.
    """
    unique_titles = remove_duplicates(titles)
    average_ranks = [[] for i in unique_titles]
    calculated_average = []
    data_count = 0
    for title in titles:
        title_index = unique_titles.index(title)
        average_ranks[title_index].append(int(data[data_count]))
        data_count += 1
    for ranks in average_ranks:
        calculated_average.append(round(sum(ranks)/len(ranks), decimal))
    return [unique_titles, calculated_average]


def sort_titles_and_rank(ranked_titles):
    """
    This function sorts through a list of rankings and sorts the
    assigned titles as well.

    It takes a 2D list, holding the average rankings of the unique
    titles, as well as the unique titles in their own list and sorts
    both arrays according to rank in ascending order.
    """
    titles = ranked_titles[0]
    ranks = ranked_titles[1]
    i = 0
    for i in range(0, len(ranks) - 1):
        for j in range(0, len(ranks) - 1 - i):
            if ranks[j] > ranks[j + 1]:
                ranks[j], ranks[j + 1] = ranks[j + 1], ranks[j]
                titles[j], titles[j + 1] = titles[j + 1], titles[j]
    return [titles, ranks]


class GoogleSheet():
    """
    This class hides any credentials to access the linked google sheet
    from the global scope. It is called in the main to initiate a connection
    and retrieve the data from netflix_data worksheet saved on my google
    account.
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
        This method requests data from the milestone_3_data spreadsheet and
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
        self.as_of = sheet.col_values(1)[1:]

    def print_column_titles(self):
        """
        Prints titles
        """
        pprint(self.column_titles)

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
        print('What data would you like to view?')
        result = get_user_input(self.column_titles, IN_DEV)
        return result

    def display_data(self, option):
        """
        This method displays the data from the column matching
        the option string passed as an argument.
        """
        rank = 'Rank'
        w_rank = 'Last Week Rank'
        y_rank = 'Year to Date Rank'
        load_stars = ['*',
                      '* *',
                      '* * *',
                      '* * * *',
                      '* * * * *',
                      '* * * *',
                      '* * *',
                      '* *',
                      '*'
                      ]
        selector = self.column_titles[option]
        print(f'you have chosen: {selector}\n')
        if selector is rank or w_rank or y_rank:
            programs_column = self.program_titles_column
            ranks_column = self.worksheet.col_values(option + 1)
            programs = programs_column[1:]
            ranks = ranks_column[1:]

            if selector == rank:
                print('What would you like to see?\n')
                choices = ['Overall rank', 'Rank at a certain time']
                user_choice = get_user_input(choices, NOT_IN_DEV)
                print(f'You have chosen: {choices[user_choice]}')
                if choices[user_choice] == 'Overall rank':
                    print('Please wait while result is calculated...\n')
                    for star in load_stars:
                        time.sleep(0.5)
                        print(star)

                    ranked_titles = find_average_rank(programs, ranks, 4)
                    sorted_ranked_titles = sort_titles_and_rank(ranked_titles)
                    my_title = 'Netflix programs by average ' \
                               'rank (smaller is better)'
                    pt.simple_bar(sorted_ranked_titles[0],
                                  sorted_ranked_titles[1],
                                  width=200,
                                  title=my_title)
                    pt.show()
                if choices[user_choice] == 'Rank at a certain time':
                    has_30_days = ['Apr', 'Jun', 'Sep', 'Nov']
                    y_choices = ['2020', '2021', '2022']
                    m_choices = ['Jan', 'Feb', 'Mar',
                                 'Apr', 'May', 'Jun',
                                 'Jul', 'Aug', 'Sep',
                                 'Oct', 'Nov', 'Dec']
                    d_choices = ['01', '02', '03', '04', '05',
                                 '06', '07', '08', '09', '10',
                                 '11', '12', '13', '14', '15',
                                 '16', '17', '18', '19', '20',
                                 '21', '22', '23', '24', '25',
                                 '26', '27', '28', '29', '30',
                                 '31']
                    invalid_option = True
                    while invalid_option:
                        print('Which year: \n')
                        user_choice_y = get_user_input(y_choices, NOT_IN_DEV)
                        print('Which month: \n')
                        user_choice_m = get_user_input(m_choices, NOT_IN_DEV)
                        print('Which date: \n')
                        if m_choices[user_choice_m] == 'Feb':
                            user_choice_d = get_user_input(d_choices[0:28],
                                                           NOT_IN_DEV)
                        elif m_choices[user_choice_m] in has_30_days:
                            user_choice_d = get_user_input(d_choices[0:30],
                                                           NOT_IN_DEV)
                        else:
                            user_choice_d = get_user_input(d_choices,
                                                           NOT_IN_DEV)
                        user_date = d_choices[user_choice_d] + '/' + \
                            d_choices[user_choice_m] + '/' + \
                            y_choices[user_choice_y]
                        print(f'You selected: {user_date}')
                        if user_date in self.as_of:
                            invalid_option = False
                        else:
                            print(f'Please pick a date between {self.as_of[1]}'
                                  f' and {self.as_of[-1]}')
                    print('Please wait while result is calculated...\n')
                    for star in load_stars:
                        time.sleep(0.5)
                        print(star)
                    as_of_index = self.as_of.index(user_date) + 2
                    titles = self.program_titles_column[
                            as_of_index - 1: as_of_index + 9]
                    ranks = self.worksheet.col_values(2)[
                            as_of_index - 1: as_of_index + 9]
                    for i in range(0, len(ranks)):
                        ranks[i] = int(ranks[i])
                    my_title = 'Netflix programs by rank (smaller is better)'
                    pt.simple_bar(titles, ranks, width=200, title=my_title)
                    pt.show()


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
