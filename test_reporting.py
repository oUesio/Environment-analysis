import pytest
from reporting import *
from numpy import genfromtxt

test_data = {'test_mon': genfromtxt('test_data.csv', delimiter=',', dtype=str)}

def test_daily_average():
    assert daily_average(test_data, 'test_mon', 'no') == [1 for _ in range (365)]
    assert daily_average(test_data, 'test_mon', 'pm10') == [2 for _ in range (365)]
    assert daily_average(test_data, 'test_mon', 'pm25') == [0 for _ in range (365)]

def test_daily_median():
    assert daily_median(test_data, 'test_mon', 'no') == [1 for _ in range (365)]
    assert daily_median(test_data, 'test_mon', 'pm10') == [2 for _ in range (365)]
    assert daily_median(test_data, 'test_mon', 'pm25') == [0 for _ in range (365)]

def test_hourly_average():
    assert hourly_average(test_data, 'test_mon', 'no') == [1 for _ in range (24)]
    assert hourly_average(test_data, 'test_mon', 'pm10') == [2 for _ in range (24)]
    assert hourly_average(test_data, 'test_mon', 'pm25') == [0 for _ in range (24)]

def test_monthly_average():
    assert monthly_average(test_data, 'test_mon', 'no') == [1 for _ in range (12)]
    assert monthly_average(test_data, 'test_mon', 'pm10') == [2 for _ in range (12)]
    assert monthly_average(test_data, 'test_mon', 'pm25') == [0 for _ in range (12)]

def test_peak_hour_date():
    assert peak_hour_date(test_data, '2021-01-01', 'test_mon', 'no') == ['24:00:00', 1.0]
    assert peak_hour_date(test_data, '2021-01-01', 'test_mon', 'pm10') == ['24:00:00', 2.0]
    assert peak_hour_date(test_data, '2021-01-01', 'test_mon', 'pm25') == ['24:00:00', 0.0]

def test_count_missing_data():
    assert count_missing_data(test_data, 'test_mon', 'no') == 0
    assert count_missing_data(test_data, 'test_mon', 'pm10') == 0
    assert count_missing_data(test_data, 'test_mon', 'pm25') == 8760

