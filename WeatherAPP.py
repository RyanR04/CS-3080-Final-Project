# Ryan Rupakheti
# Final Porject
# 7/19/2026

#Import Needed Libraires and Class
import tkinter as tk
from datetime import datetime as dt 
import requests
import calendar as cd


BASE_URL1 = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d04a6beeb2871b7cddacc06477b407b3"

# GUI Class for GUI functionality
class AppGUI():

    #Check if searched is already clicked
    Already_Clicked = 0

    def __init__(self):

        #Intializing GUI and adding demensions
        self.root = tk.Tk()
        self.root.geometry("500x500")

        #Title
        self.root.title("Weather App")

        #Labels,Textboxes,and Buttons Below
        
        #Intro Label Use as Initial Prompt
        self.Intro_Label = tk.Label(self.root,text="Enter a city to get Weather",font=("Arial",18))
        self.Intro_Label.pack(pady=10)

        #TextBox used to Get City
        self.textbox = tk.Text(self.root,height=1,font=("Arial",16))
        self.textbox.pack(padx=5,pady=5)

        self.Search_B = tk.Button(self.root,text="Search",font=("Arial",18),command=self.City_Info)
        self.Search_B.pack()

        #This runs the GUI
        self.root.mainloop()

    #Get City Info
    def City_Info(self):

        #Remove Intro_Label for now
        self.Intro_Label.forget()

        #Get City
        City_Input = self.textbox.get("1.0",tk.END).strip()
        # Then delete whats stored in textbox
        self.textbox.delete("1.0", tk.END)

        #This is for the request
        url1 = BASE_URL1 + "appid=" + API_KEY + "&q=" + City_Input

        #Getting the current Data for said City
        DailyForeCast = requests.get(url1).json()
        #Get Current Country for City
        City_Country = DailyForeCast['sys']['country']

        #Get all Data For Labels
        Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W = Get_Weather_Data(DailyForeCast)

        #If Already Clicked was 0
        if self.Already_Clicked == 0:
            #Create a CityLabel with text
            self.CityLabel = tk.Label(self.root,text=f"{City_Input},{City_Country}",font=("Arial",20))
            #Pack the label on screen
            self.CityLabel.pack()

            self.DesL = tk.Label(self.root,text=f"{Daily_Des}")
            self.DesL.pack()

            self.TempL = tk.Label(self.root,text=f"{Daily_T}")
            self.TempL.pack()
            
            self.TempMML = tk.Label(self.root,text=f"Max: {Daily_Max}   Min: {Daily_Min}")
            self.TempMML.pack()
            
            self.FeelL = tk.Label(self.root,text=f"Feels Like: {Daily_FeelT}")
            self.FeelL.pack()
            
            self.HumL = tk.Label(self.root,text=f"{Daily_H} %")
            self.HumL.pack()
            
            self.WinL = tk.Label(self.root,text=f"{Daily_W}")
            self.WinL.pack()
        else: 
            #Else config it to new City Value
            self.CityLabel.config(text=f"{City_Input},{City_Country}")
            self.DesL.config(text=f"{Daily_Des}")
            self.TempL.config(text=f"{Daily_T}")
            self.TempMML.config(text=f"Max: {Daily_Max}   Min: {Daily_Min}")
            self.FeelL.config(text=f"Feels Like: {Daily_FeelT}")
            self.HumL.config(text=f"{Daily_H} %")
            self.WinL.config(text=f"{Daily_W}")


        #Increment the Already Clicked Class Var
        self.Already_Clicked += 1

def Get_Weather_Data(Current_City):

    #Here we get Basic Daily ForCast Information 
    City_Temp = Current_City['main']['temp']
    City_Feels_Temp = Current_City['main']['feels_like']
    City_Max = Current_City['main']['temp_max']
    City_Min = Current_City['main']['temp_min']
    City_Humidity = Current_City['main']['humidity']
    City_Description = Current_City['weather'][0]['description']
    City_Wind = Current_City['wind']['speed']

    # Get the UNIX vals for Sunris and Sunset
    City_Sunrise = Current_City['sys']['sunrise']
    City_Sunset= Current_City['sys']['sunset']

    #Make it a Date object
    City_Sunrise = dt.fromtimestamp(City_Sunrise)
    City_Sunset = dt.fromtimestamp(City_Sunset)

    #Convert it to string format
    City_Sunrise = City_Sunrise.strftime("%I:%M%p")
    City_Sunset = City_Sunset.strftime("%I:%M%p")

    return City_Temp,City_Feels_Temp,City_Max,City_Min,City_Humidity,City_Description,City_Wind


#Main 
def main():

    #Open Gui
    AppGUI()

if __name__ == "__main__":
    main()



# {'coord': {'lon': 51.4215, 'lat': 35.6944}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 306.88, 'feels_like': 304.43, 'temp_min': 306.88, 'temp_max': 306.88, 'pressure': 1010, 'humidity': 13, 'sea_level': 1010, 'grnd_level': 863}, 'visibility': 10000, 'wind': {'speed': 1.79, 'deg': 180}, 'clouds': {'all': 0}, 'dt': 1785607825, 'sys': {'type': 2, 'id': 47737, 'country': 'IR', 'sunrise': 1785548516, 'sunset': 1785598755}, 'timezone': 12600, 'id': 112931, 'name': 'Tehran', 'cod': 200}