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

    #Intial Frame Setup
    def __init__(self):

        #Intializing GUI and adding demensions
        self.root = tk.Tk()
        self.root.geometry("500x500")

        #Title
        self.root.title("Weather App")

        #Labels,Textboxes,and Buttons Below
        
        #Setup for 3 x 3 Button Grid
        self.ButtonGrid = tk.Frame(self.root)
        self.ButtonGrid.pack(pady=10,fill='x')
        self.ButtonGrid.columnconfigure(0,weight=1)
        self.ButtonGrid.columnconfigure(1,weight=1)
        self.ButtonGrid.columnconfigure(2,weight=1)
        
        # Create the buttons
        self.SaveB = tk.Button(self.ButtonGrid, text="Save")
        self.HomeB = tk.Button(self.ButtonGrid, text="Home")
        self.ConvertB = tk.Button(self.ButtonGrid, text="Convert",)
        
        # Position them in one row
        self.HomeB.grid(row=0, column=0, sticky="ew", padx=5)
        self.SaveB.grid(row=0, column=1, sticky="ew", padx=5)
        self.ConvertB.grid(row=0, column=2, sticky="ew", padx=5)

        #Do not display intially
        self.ButtonGrid.forget()

        #Intro Label Use as Initial Prompt
        self.Intro_Label = tk.Label(self.root,text="Enter a city to get Weather",font=("Arial",18))
        self.Intro_Label.pack(pady=10)

        #TextBox used to Get City
        self.textbox = tk.Text(self.root,height=1,font=("Arial",16))
        self.textbox.pack(padx=5,pady=5)

        #Serach button that displays information
        self.Search_B = tk.Button(self.root,text="Search",font=("Arial",18),command=self.Display_Info)
        self.Search_B.pack()

        #This runs the GUI
        self.root.mainloop()

    #Get City Info
    def Display_Info(self):

        #Remove Intro_Label for now
        self.Intro_Label.forget()

        #Put Button Frame on Top
        self.ButtonGrid.pack(before=self.textbox)

        #Get City
        City_Input = self.textbox.get("1.0",tk.END).strip()
        # Then delete whats stored in textbox
        self.textbox.delete("1.0", tk.END)

        #Get all Data For Labels
        Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W,City_Country = Get_Weather_Data(City_Input)

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
            
            self.HumL = tk.Label(self.root,text=f"Humidity: {Daily_H} %")
            self.HumL.pack()
            
            self.WinL = tk.Label(self.root,text=f"Wind Speed: {Daily_W}")
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



#Function to get all needed Weather Data for Display
def Get_Weather_Data(City):

  
    url1 = BASE_URL1 + "appid=" + API_KEY + "&q=" + City + "&units=" + "metric"
  

    #Get the current info from city url
    Current_City = requests.get(url1).json()

    #Get country it is in
    Country = Current_City['sys']['country']

    #Here we get Basic Daily ForCast Information 
    City_Temp = round(Current_City['main']['temp'])
    City_Feels_Temp = round(Current_City['main']['feels_like'])
    City_Max = round(Current_City['main']['temp_max'])
    City_Min = round(Current_City['main']['temp_min'])
    City_Humidity = Current_City['main']['humidity']
    City_Description = Current_City['weather'][0]['description'].upper()
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

    #Return Needed Information
    return City_Temp,City_Feels_Temp,City_Max,City_Min,City_Humidity,City_Description,City_Wind,Country

#Main 
def main():

    #Open Gui
    AppGUI()

if __name__ == "__main__":
    main()
