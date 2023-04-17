
def sumvalues(values):
    """
    Calculates the sum of a list of values

    Args:
        values (list): List of values

    Returns:
        int: Total sum
    """ 
    total = 0
    for v in values:
        if str(v).replace('.', '').isdigit():
            total += float(v)
        else:
            raise Exception('Non-numerical values present in list')
    return total

def maxvalue(values):
    """
    Finds the max value of a list of values

    Args:
        values (list): List of values

    Returns:
        int: Max value
    """   
    large = values[0]
    for v in values:
        if str(v).replace('.', '').isdigit():
            if float(v) > large:
                large = float(v)
        else:
            raise Exception('Non-numerical values present in list')
    return large

def minvalue(values):
    """
    Finds the min value of a list of values

    Args:
        values (list): List of values

    Returns:
        int: Min value
    """   
    small = values[0]
    for v in values:
        if str(v).replace('.', '').isdigit():
            if float(v) < small:
                small = float(v)
        else:
            raise Exception('Non-numerical values present in list')
    return small

def meanvalue(values):
    """
    Calculates the mean of a list of values

    Args:
        values (list): List of values

    Returns:
        int: Mean of the list
    """   
    total = sumvalues(values)
    return total / len(values)

def countvalue(values,x):
    """
    Counts the number of times a value is in a list

    Args:
        values (list): List of values
        x (float): Value to find

    Returns:
        int: Total number of times
    """ 
    count = 0
    for v in values:
        if str(v) == str(x):
            count += 1
    return count

