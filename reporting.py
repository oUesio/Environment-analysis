
def daily_average(data, monitoring_station, pollutant):
    """
    Calculates the daily averages of the data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: List of daily averages
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hours = len(table)
    d_averages = []
    total = 0
    for h in range (1, hours):
        if table[h][pol_index].replace('.', '').isdigit(): #checks if the value is a number
            total += float(table[h][pol_index])
        if h % 24 == 0:
            d_averages.append(round(total / 24, 2)) #appends average of a day and rounds to 2dp
            total = 0
    return d_averages

def daily_median(data, monitoring_station, pollutant):
    """
    Calculates the daily medians of the data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: List of daily medians
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hours = len(table)
    d_medians = []
    all_hours = []
    for h in range (1, hours):
        if table[h][pol_index].replace('.', '').isdigit():
            all_hours.append(float(table[h][pol_index]))
        else:
            all_hours.append(0.0) #appends 0.0 when the value is 'No data'
        if h % 24 == 0:
            all_hours.sort()
            d_medians.append(round((all_hours[12] + all_hours[13]) / 2, 2)) #appends the median of a day and rounds to 2dp
            all_hours = []
    return d_medians

def hourly_average(data, monitoring_station, pollutant):
    """
    Calculates the hourly averages of the data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: List of hourly averages
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hours = len(table)
    h_total = [0 for _ in range (24)]
    for h in range (1, hours):
        if table[h][pol_index].replace('.', '').isdigit():
            h_total[int(table[h][1][:2]) - 1] += float(table[h][pol_index]) #adds the value to the hour of the day 
    return [round(t / 365, 2) for t in h_total]

def monthly_average(data, monitoring_station, pollutant):
    """
    Calculates the monthly averages of the data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: List of monthly averages
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hours = len(table)
    m_average = []
    total = 0
    month = 1
    for h in range (1, hours):
        if int(table[h][0][5:7]) != month:
            if month == 2:
                if int(table[1][0][:4]) % 4 == 0: #checks if it is a leap year
                    m_average.append(round(total / 29 / 24, 2))
                else:
                    m_average.append(round(total / 28 / 24, 2))
            elif month in [1,3,5,7,8,10,12]: #checks for months with 31 days
                m_average.append(round(total / 31 / 24, 2))
            else:
                m_average.append(round(total / 30 / 24, 2))
            total = 0
            month += 1 #increments when the data moves onto the nex month
        if table[h][pol_index].replace('.', '').isdigit():
            total += float(table[h][pol_index])
    m_average.append(round(total / 31 / 24, 2)) #calculates for December
    return m_average

def peak_hour_date(data, date, monitoring_station,pollutant):
    """
    Finds the peak hour date of the data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        date (str): The date
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: The hour and the pollution level
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hour_date = []
    for row in table:
        if row[0] == date:
            if row[pol_index].replace('.', '').isdigit():
                hour_date.append([row[1], float(row[pol_index])])
            else:
                hour_date.append([row[1], 0.0])
    hour_date.sort(key=lambda x: x[1])
    return hour_date[-1]

def count_missing_data(data, monitoring_station, pollutant):
    """
    Counts the missing data for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        int: Number of missing data
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    count = 0
    for row in table:
        if row[pol_index] == 'No data':
            count += 1
    return count

def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """
    Fills the missing data with a new value for the monitoring station and pollutant

    Args:
        data (dict): Dictionary of data grouped into monitoring stations
        new_value (float): Value to replace missing data
        monitoring_station (str): Name of monitoring station
        pollutant (str): Name of pollutant

    Returns:
        list: New data for monitoring station
    """
    table = data[monitoring_station]
    pol_index = list(table[0]).index(pollutant)
    hours = len(table)
    for h in range (1, hours):
        if table[h][pol_index] == 'No data':
            table[h][pol_index] = new_value
    return table
            