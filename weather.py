import requests
from bs4 import BeautifulSoup
import pandas as pd


page = requests.get("https://forecast.weather.gov/MapClick.php?lat=44.979&lon=-93.2649#.XbIBbq97lhE")

soup = BeautifulSoup(page.content, 'html.parser')

seven_day = soup.find(id='seven-day-forecast')

forecast_items = seven_day.find_all(class_='tombstone-container')


periods = [pt.get_text() for pt in seven_day.select(".tombstone-container .period-name")]
short_descs = [desc.get_text() for desc in seven_day.select(".tombstone-container .short-desc")]
temps = [temp.get_text() for temp in seven_day.select(".tombstone-container .temp")]
imgs = [d['title'] for d in seven_day.select(".tombstone-container img")]

#this makes the weather into a dataframe
weather = pd.DataFrame({
    'period': periods,
    'short_desc': short_descs,
    'temp': temps,
    'des': imgs
    })

#extracting temp as int we can work with
temp_nums = weather['temp'].str.extract("(\d+)")
weather["temp_num"] = temp_nums.astype('int')

#this is just going to print the mean temp for the next 5 days
print('The average temp for the next 5 days is ' + str(weather['temp_num'].mean()))




#this function gives me the full 5 day forcast
def forecast_week():
    forcast_list = []
    for i in forecast_items:
        period = i.find(class_="period-name").get_text()
        short_desc = i.find(class_="short-desc").get_text()
        temp = i.find(class_="temp").get_text()
        img = i.find('img')
        desc = img['title']
        forcast_list.append((period,short_desc,temp,desc))
    for i in forcast_list:
        print(i[0])
        print(i[1])
        print(i[2])
        print(i[3])
        print('\n')


