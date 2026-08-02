# Ryan Rupakheti
# Final Porject
# 7/19/2026

#Import Needed Libraires and Class
import tkinter as tk
from datetime import datetime as dt 
import requests
import calendar as cd
from PIL import Image, ImageTk
from io import BytesIO


BASE_URL1 = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d04a6beeb2871b7cddacc06477b407b3"



# GUI Class for GUI functionality
class AppGUI():

    #Check if searched is already clicked
    Already_Clicked = 0
    City_Units = "metric"
    City_Input = ""

    #Intial Frame Setup
    def __init__(self):

        #Intializing GUI and adding demensions
        self.BG = "#D3E5F6"
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.config(bg=self.BG)

        #Title
        self.root.title("Weather App")

        #Labels,Textboxes,and Buttons Below
        
        #Setup for 3 x 3 Button Grid
        self.ButtonGrid = tk.Frame(self.root,bg=self.BG)
        self.ButtonGrid.pack(pady=10,fill='x')
        self.ButtonGrid.columnconfigure(0,weight=1)
        self.ButtonGrid.columnconfigure(1,weight=1)
        self.ButtonGrid.columnconfigure(2,weight=1)
       
        
        # Create the buttons
        self.SaveB = tk.Button(self.ButtonGrid, text="Save")
        self.HomeB = tk.Button(self.ButtonGrid, text="Home")
        self.ConvertB = tk.Button(self.ButtonGrid, text="Convert to Fahrenheight",command=self.Convert)

        # Position them in one row
        self.HomeB.grid(row=0, column=0, sticky="ew", padx=5)
        self.SaveB.grid(row=0, column=1, sticky="ew", padx=5)
        self.ConvertB.grid(row=0, column=2, sticky="ew", padx=5)

        #Do not display intially
        self.ButtonGrid.forget()

        #Intro Label Use as Initial Prompt
        self.Intro_Label = tk.Label(self.root,text="Enter a city to get Weather",font=("Arial",18),bg=self.BG)
        self.Intro_Label.pack(pady=10)

        #TextBox used to Get City
        self.textbox = tk.Text(self.root,height=1,font=("Arial",16))
        self.textbox.pack(padx=5,pady=5)

        #Serach button that displays information
        self.Search_B = tk.Button(self.root,text="Search",font=("Arial",18),command=self.Display_Info,bg=self.BG)
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
        self.City_Input = self.textbox.get("1.0",tk.END).strip()
        self.textbox.delete("1.0", tk.END)

        #Get all Data For Labels
        Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W,City_Country,DCity_Icon,DCity_Sunrise,DCity_Sunset = Get_Weather_Data(self.City_Input,self.City_Units)

        #Send them to update labels which will check and chnage them
        self.Update_Labels(Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W,City_Country,self.City_Input,DCity_Icon,DCity_Sunrise,DCity_Sunset)


    def Update_Labels(self,UDaily_T,UDaily_FeelT,UDaily_Max,UDaily_Min,UDaily_H,UDaily_Des,UDaily_W,UCity_Country,UCity_Input,UCity_Icon,UCity_Sunrise,UCity_Sunset):

        if self.City_Units == "metric":
            self.ConvertB.config(text="Convert to Fahrenheight")
            SymbolT = "°C"
            SymbolM = "M/S"
        elif self.City_Units == "imperial":
            self.ConvertB.config(text="Convert to Celsius")
            SymbolT = "°F"
            SymbolM = "MPH"

        Icon_URL = f"https://openweathermap.org/img/wn/{UCity_Icon}@2x.png"

        response = requests.get(Icon_URL)

        image = Image.open(BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        
        #If Already Clicked was 0
        if self.Already_Clicked == 0:
            #Create a CityLabel with text
            self.CityLabel = tk.Label(self.root,text=f"{UCity_Input},{UCity_Country}",bg=self.BG,font=("Arial",20))
            #Pack the label on screen
            self.CityLabel.pack()

            self.IconLabel = tk.Label(self.root,bg=self.BG,image=photo)
            self.IconLabel.image = photo
            self.IconLabel.pack()
        
            self.DesL = tk.Label(self.root,bg=self.BG,text=f"{UDaily_Des}")
            self.DesL.pack()
        
            self.TempL = tk.Label(self.root,bg=self.BG,text=f"{UDaily_T}{SymbolT}")
            self.TempL.pack()
                    
            self.TempMML = tk.Label(self.root,bg=self.BG,text=f"Max: {UDaily_Max}{SymbolT}  Min: {UDaily_Min}{SymbolT}")
            self.TempMML.pack()
                    
            self.FeelL = tk.Label(self.root,bg=self.BG,text=f"Feels Like: {UDaily_FeelT}{SymbolT}")
            self.FeelL.pack()
                    
            self.HumL = tk.Label(self.root,bg=self.BG,text=f"Humidity: {UDaily_H}%")
            self.HumL.pack()
                    
            self.WinL = tk.Label(self.root,bg=self.BG,text=f"Wind Speed: {UDaily_W} {SymbolM}")
            self.WinL.pack()

            self.SunRS = tk.Label(self.root,bg=self.BG,text=f"Sunrise: {UCity_Sunrise}  Sunset: {UCity_Sunset}")
            self.SunRS.pack()
        else: 
            #Else config it to new City Value
            self.CityLabel.config(text=f"{UCity_Input},{UCity_Country}")
            self.IconLabel.config(image=photo)
            self.IconLabel.image = photo
            self.DesL.config(text=f"{UDaily_Des}")
            self.TempL.config(text=f"{UDaily_T}{SymbolT}")
            self.TempMML.config(text=f"Max: {UDaily_Max}{SymbolT}   Min: {UDaily_Min}{SymbolT}")
            self.FeelL.config(text=f"Feels Like: {UDaily_FeelT}{SymbolT}")
            self.HumL.config(text=f"Humidity: {UDaily_H} %")
            self.WinL.config(text=f"Wind Speed: {UDaily_W} {SymbolM}")
            self.SunRS.config(text=f"Sunrise: {UCity_Sunrise}  Sunset: {UCity_Sunset}")

        #Increment the Already Clicked Class Var
        self.Already_Clicked += 1

    def Convert(self):

        self.City_Units = self.Convert_Units(self.City_Units)

        #Get all Data For Labels
        CDaily_T,CDaily_FeelT,CDaily_Max,CDaily_Min,CDaily_H,CDaily_Des,CDaily_W,CCity_Country,CCity_Icon,CCity_Sunrise,CCity_Sunset = Get_Weather_Data(self.City_Input,self.City_Units)

        #Send them to update labels which will check and chnage them
        self.Update_Labels(CDaily_T,CDaily_FeelT,CDaily_Max,CDaily_Min,CDaily_H,CDaily_Des,CDaily_W,CCity_Country,self.City_Input,CCity_Icon,CCity_Sunrise,CCity_Sunset)
        

    def Convert_Units(self,Units_G):
        if Units_G == "imperial":
            return "metric"
        else:
           return "imperial"


#Function to get all needed Weather Data for Display
def Get_Weather_Data(City,CUnit):

    url1 = BASE_URL1 + "appid=" + API_KEY + "&q=" + City + "&units=" + CUnit
  
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
    City_Icon = Current_City['weather'][0]['icon']

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
    return City_Temp,City_Feels_Temp,City_Max,City_Min,City_Humidity,City_Description,City_Wind,Country,City_Icon,City_Sunrise,City_Sunset

#Main 
def main():

    #Open Gui
    AppGUI()

if __name__ == "__main__":
    main()