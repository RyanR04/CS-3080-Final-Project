from datetime import datetime as dt 
import requests
import calendar as cd

#Get the url for the API
BASE_URL1 = "https://api.openweathermap.org/data/2.5/weather?"

BASE_URL2 = "https://api.openweathermap.org/data/2.5/forecast?"

#The Key for the API
API_KEY = "de845e805a9b50f6b70f941e46d62ad6"

#This gets the City 
CITY = input("Enter any City: ")

#This is for the request
url1 = BASE_URL1 + "appid=" + API_KEY + "&q=" + CITY

#This is for the request
url2 = BASE_URL2 + "appid=" + API_KEY + "&q=" + CITY


data2 = requests.get(url2).json()

def Get_Weather_Data():
    Current_City = requests.get(url1).json()

    City_Temp = Current_City['main']['temp']
    City_Feels_Temp = Current_City['main']['feels_like']
    City_Max = Current_City['main']['temp_max']
    City_Min = Current_City['main']['temp_min']
    City_Humidity = Current_City['main']['humidity']
    City_Description = Current_City['weather'][0]['description']
    City_Wind = Current_City['wind']['speed']
    Current_Icon = Current_City['weather'][0]['icon']

    City_Sunrise = Current_City['sys']['sunrise']
    City_Sunset= Current_City['sys']['sunset']

    City_Sunrise = dt.fromtimestamp(City_Sunrise)
    City_Sunset = dt.fromtimestamp(City_Sunset)

    City_Sunrise = City_Sunrise.strftime("%I:%M%p")
    City_Sunset = City_Sunset.strftime("%I:%M%p")
    
    #If Fahrenheight (Do the same for celsius)
    City_Temp = Convert_to_Fah(City_Temp)
    City_Feels_Temp = Convert_to_Fah(City_Feels_Temp)
    City_Max = Convert_to_Fah(City_Max)
    City_Min = Convert_to_Fah(City_Min)
    City_Wind = Convert_MPH(City_Wind)

    print(f"This Will be where the ICON is {Current_Icon}")
    print(f"{City_Description}")
    print(f"Current: {City_Temp}")
    print(f"Max:{City_Max} F, Min : {City_Min} F")
    print(f"Feels Like: {City_Feels_Temp}")
    print(f"{City_Humidity}%")
    print(f"Wind Speed: {City_Wind:.2f} mph")
    print(f"Sunrise: {City_Sunrise}, Sunset: {City_Sunset}")


def Convert_to_Cel(TempC):
    Cel = round(TempC - 273.15)
    return Cel

def Convert_to_Fah(TempF):
    Fah = round((TempF - 273.15) * (9/5) + 32)
    return Fah

def Convert_MPH(Ms):
    mph = Ms * 2.23694
    return mph


def ForeCastInfo(Current_City_F):
    #Stores only needed data
    five_day = {}

    # For each forecast in data2
    for forecast in Current_City_F['list']:
        #Get the date
        date = forecast['dt_txt'].split()[0]
        #If not in five_days intilize the data
        if date not in five_day:
            five_day[date]={
                'high': forecast['main']['temp_max'],
                'low': forecast['main']['temp_min'],
                'icon': forecast['weather'][0]['icon']
            }
        #Else comp current value with the current max and forecasr and update
        else:
            five_day[date]['high'] = max(five_day[date]['high'], forecast['main']['temp_max'])
            five_day[date]['low'] = min(five_day[date]['low'], forecast['main']['temp_min'])

    for key,value in five_day.items():
        five_day[key]['high'] = Convert_to_Fah(five_day[key]['high'])
        five_day[key]['low'] = Convert_to_Fah(five_day[key]['low'])

    for key,value in five_day.items():
        Cdate = dt.strptime(key,"%Y-%m-%d")
        weekday = Cdate.weekday()
        print(cd.day_abbr[weekday])
        print(f"High {five_day[key]['high']} F")
        print(f"Low {five_day[key]['low']} F")
        print("\n")


Get_Weather_Data()
print("\n")
print("\n")
print("Five Day Forcecast")
ForeCastInfo(data2)