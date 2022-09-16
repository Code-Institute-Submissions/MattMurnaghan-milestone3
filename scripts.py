""" - Milestone 3 -
Author: Matthew Murnaghan
Date: 12/09/2022

This set of scripts were used to help sanitise the data set and test the
plotext library. They were not used in the final script.
"""
import plotext as pt


def find_corrupt_titles(arr):
    """
    This function finds corrupted title names in a supplied list.
    """
    corrupt_titles = [item for item in arr if "€" in item]
    return corrupt_titles


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
