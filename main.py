from numpy import genfromtxt
from reporting import *
from intelligence import *
from monitoring import *


def main_menu():
    """
    Shows the main options to choose
    """
    exit = False
    while exit == False:
        print ('========================')
        print ('(R)eporting Menu')
        print ('(I)ntelligence Menu')
        print ('(M)onitoring Menu')
        print ('(A)bout')
        print ('(Q)uit')
        print ('========================')
        print ('')
        choice = input("Enter letter of option: ")
        while choice.upper() not in ['R', 'I', 'M', 'A', 'Q']:
            print ('Not a valid choice')
            choice = input("Enter letter of option: ")
        if choice.upper() == 'R':
            reporting_menu()
        elif choice.upper() == 'I':
            intelligence_menu()
        elif choice.upper() == 'M':
            monitoring_menu()
        elif choice.upper() == 'A':
            about()
        else:
            exit = quit()


def reporting_menu():
    """
    Shows options to run functions in reporting.py
    """
    data = {'Harlington': genfromtxt('data/Pollution-London Harlington.csv', delimiter=',', dtype=str),
            'Marylebone Road': genfromtxt('data/Pollution-London Marylebone Road.csv', delimiter=',', dtype=str),
            'N Kensington': genfromtxt('data/Pollution-London N Kensington.csv', delimiter=',', dtype=str)
            }
    print (data)
    exit = False
    while exit == False:
        print ('========================')
        print ('(1) Daily Average')
        print ('(2) Daily Median')
        print ('(3) Hourly Average')
        print ('(4) Monthly Average')
        print ('(5) Peak Hour')
        print ('(6) Count Missing Data')
        print ('(7) Fill Missing Data')
        print ('(8) Exit')
        print ('========================')
        print ('')
        choice = input("Enter number of option: ")
        while choice not in ['1','2','3','4','5','6','7', '8']:
            print ('Not a valid choice')
            choice = input("Enter number of option: ")
        if choice == '8':
            exit = True
            break
        mon_st = input('Enter name of monitoring station: ')
        while mon_st not in ['Harlington', 'Marylebone Road', 'N Kensington']:
            print ('Not a valid monitoring station')
            mon_st = input('Enter name of monitoring station: ')
        pol = input('Enter name of pollutant: ')
        while pol not in ['no', 'pm10', 'pm25']:
            print ('Not a valid pollutant')
            pol = input('Enter name of pollutant: ')
        if choice == '1':
            print (daily_average(data, mon_st, pol))
        elif choice == '2':
            print (daily_median(data, mon_st, pol))
        elif choice == '3':
            print (hourly_average(data, mon_st, pol))
        elif choice == '4':
            print (monthly_average(data, mon_st, pol))
        elif choice == '5':
            valid = False
            date = input('Enter date in format YYYY-MM-DD: ')
            while not valid:
                try:
                    if datetime.datetime.strptime(date, '%Y-%m-%d') <= datetime.datetime.strptime('2021-12-31', '%Y-%m-%d') and datetime.datetime.strptime(date, '%Y-%m-%d') >= datetime.datetime.strptime('2021-01-01', '%Y-%m-%d'):
                        valid = True
                    else:
                        print ('Invalid time')
                        date = input('Enter date in format YYYY-MM-DD: ')
                except:
                    print ('Incorrect format')
                    date = input('Enter date in format YYYY-MM-DD: ')
            
            print (peak_hour_date(data, date, mon_st, pol))
        elif choice == '6':
            print (count_missing_data(data, mon_st, pol))
        elif choice == '7':
            new = input('Enter new value: ')
            new_data = fill_missing_data(data, new, mon_st, pol)
            data[mon_st] = new_data
            print (new_data)

def intelligence_menu():
    """
    Shows options to run functions in intelligence.py
    """
    exit = False
    mark = []
    while exit == False:
        print ('========================')
        print ('(1) Find Red Pixels')
        print ('(2) Find Cyan Pixels')
        print ('(3) Detect Connected Components')
        print ('(4) Detect Connected Components - Sorted')
        print ('(5) Exit')
        print ('========================')
        print ('')
        choice = input("Enter number of option: ")
        while choice not in ['1','2','3','4','5']:
            print ('Not a valid choice')
            choice = input("Enter number of option: ")
        if choice == '1':
            print (find_red_pixels('map.png', upper_threshold=100, lower_threshold=50))
        elif choice == '2':
            print (find_cyan_pixels('map.png', upper_threshold=100, lower_threshold=50))
        elif choice == '3':
            try:
                mark = detect_connected_components('map-red-pixels.jpg')
                print (mark)
            except:
                print ('Needs to run Find Red Pixels first.')
        elif choice == '4':
            if len(mark) != 0:
                detect_connected_components_sorted(mark)
            else:
                print ('Needs to run Detect Connected Components first.')
        else:
            exit = True

def monitoring_menu():
    """
    Shows options to run functions in monitoring.py
    """
    exit = False
    data = []
    while exit == False:
        print ('========================')
        print ('(1) List data for certain pollutant and station for range of dates')
        print ('(2) Sort data')
        print ('(3) Site with highest recorded pollution for range of dates')
        print ('(4) List species and site codes')
        print ('(5) Exit')
        print ('========================')
        print ('')
        choice = input("Enter number of option: ")
        while choice not in ['1','2','3','4','5']:
            print ('Not a valid choice')
            choice = input("Enter number of option: ")
        if choice == '1':
            start, end = check_times()
            site = input('Enter Site code: ')
            spec = input('Enter Species code: ')
            data = pollutant_for_range_of_dates(site, spec, start, end)
        elif choice == '2':
            if len(data) != []:
                order = input('Enter order to sort data (asc/desc): ')
                while order.lower() not in ['asc', 'desc']:
                    order = input('Enter order to sort data (asc/desc): ')
                print (sort_data(data, order))
            else:
                print ('Run (1) first to create data')
        elif choice == '3':
            sites = []
            start, end = check_times()
            pol = input('Enter species code: ')
            num = input('Enter no. of sites to compare: ')
            while not num.isdigit():
                num = input('Enter no. of sites to compare: ')
            for x in range (int(num)):
                sites.append(input('({}) Enter site code: '.format(x+1)))
            print (compare_sites(sites, pol, start, end))
        elif choice == '4':
            list_species_and_site_codes()
        else:
            exit = True

def about():
    """
    The module code and my candidate number
    """
    print ('ECM1400')
    print ('Candidate number: 237313')

def quit():
    """
    Used to end the program
    """
    return True


if __name__ == '__main__':
    main_menu()