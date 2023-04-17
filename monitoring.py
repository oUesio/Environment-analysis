import requests
import datetime

def get_live_data_from_api(site_code, species_code, start_date, end_date):
    """
    Gets the data from the api

    Args:
        site_code (str): The site code
        species_code (str): The species code
        start_date (str): Starting date for the range
        end_date (str): End date for the range

    Returns:
        dictionary: The api data
    """
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()

def check_times():
    """
    Checks the starting and end times for wrong formats and if the end time is later than starting

    Returns:
        str, str: Starting and end times
    """
    start = ''
    end = ''
    valid_start = False
    valid_end = False
    valid_times = False
    while not valid_times:
        while not valid_start:
            start = input('Enter Start Date (YYYY-MM-DD): ')
            try:
                datetime.datetime.strptime(start, '%Y-%m-%d')
                valid_start = True
            except:
                print ('Incorrect format')
        while not valid_end:
            end = input('Enter End Date (YYYY-MM-DD): ')
            try:
                datetime.datetime.strptime(end, '%Y-%m-%d')
                valid_end = True
            except:
                print ('Incorrect format')
        if datetime.datetime.strptime(start, '%Y-%m-%d') < datetime.datetime.strptime(end, '%Y-%m-%d'):
            valid_times = True
        else:
            valid_start = False
            valid_end = False
            print ('End Date is before Start Date')
    return start, end

def pollutant_for_range_of_dates(site, spec, start, end):
    """
    Converts the api data into a format which can be used and writes into text file

    Args:
        site (str): The site code
        spec (str): The species code
        start (str): Starting date for the range
        end (str): End date for the range

    Returns:
        list: The dates, times and pollution levels from the api data
    """
    date_pol = []
    try:
        data = get_live_data_from_api(site, spec, start, end)
        with open(site+'_'+spec+'_'+start+'_'+end+'.txt', 'w') as f:
            f.write('date,time,'+spec+'\n')
            for d in data['RawAQData']['Data']:
                val = d['@Value']
                if val == "":
                    val = 'No data'
                date_pol.append(d['@MeasurementDateGMT'].split(' ')+[val])
                f.write('{0},{1}\n'.format(d['@MeasurementDateGMT'].replace(' ', ','), val))
                print ('{0}     {1}'.format(d['@MeasurementDateGMT'], val))            
    except:
        print ('Invalid Site code or Species code')
    return date_pol


def merge(left, right, order):
    """
    Sorts the two lists

    Args:
        left (list): Left half of list
        right (list): Right half of list
        order (str): Order the data is to be sorted in

    Returns:
        list: The lists merged and sorted 
    """
    new = []
    new_left = left
    new_right = right
    while len(new_left) > 0 and len(new_right) > 0:
        if order.lower() == 'desc':
            if float(left[0][2]) > float(right[0][2]):
                new.append(new_left.pop(0))
            else:
                new.append(new_right.pop(0))
        else:
            if float(left[0][2]) < float(right[0][2]):
                new.append(new_left.pop(0))
            else:
                new.append(new_right.pop(0))
    return new + new_left + new_right
    
def sort_data(data, order):
    """
    Sorts the data in an order chosen by user

    Args:
        data (list): The data from pollutant_for_range_of_dates
        order (str): Order the data should be sorted in

    Returns:
        list: The sorted data
    """
    if len(data) < 2:
        return data
    else:
        half = len(data) // 2
        return merge(sort_data(data[:half], order), sort_data(data[half:], order), order)

def compare_sites(sites, pol, start, end):
    """
    Compares multiple sites for a certain range of dates and pollutant

    Args:
        sites (list): Sites codes
        pol (str): The species code
        start (str): Starting date for the range
        end (str): End date for the range

    Returns:
        str: Message on what site had the largest pollution level for the range or Error message because of invalid site and species code entered
    """
    sites_data = []
    try:
        for s in sites:
            data = get_live_data_from_api(s,pol,start,end)
            p = []
            for x in data['RawAQData']['Data']:
                if x['@Value'] == '':
                    p.append(0)
                else:
                    p.append(float(x['@Value']))
            sites_data.append({'site': s, 'largest': max(p)})
        largest = max(sites_data, key=lambda x:x['largest'])
        return 'The highest recorded pollution of {} is at site {} of value {} between {} and {}'.format(pol, largest['site'], largest['largest'], start, end)
    except:
        return 'Invalid Site code or Species code'

def list_species_and_site_codes():
    """
    Lists all the site codes in London and species code
    """
    print ('=======Site Codes=======')
    site_info = requests.get('http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json').json()
    print ('Code'.ljust(10)+'Name'.ljust(50)+'Type')
    print ('-'*100)
    for s in site_info['Sites']['Site']:
        print (''.join([s[list(s.keys())[x+2]].ljust((x)*40+10) for x in range(3)]))
    print()
    print ('=======Species Codes=======')
    species_info = requests.get('http://api.erg.ic.ac.uk/AirQuality/Information/Species/Json').json()
    print ('Code'.ljust(12)+'Name'.ljust(24)+'Description')
    print ('-'*100)
    for s in species_info['AirQualitySpecies']['Species']:
        print (''.join([s[list(s.keys())[x]].ljust((x+1)*12) for x in range(3)]))
