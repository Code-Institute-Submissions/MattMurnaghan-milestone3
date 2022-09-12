def find_corrupt_titles(arr):
    """
    This function finds corrupted title names in a supplied list.
    """
    corrupt_titles = [item for item in arr if "€" in item]
    return corrupt_titles