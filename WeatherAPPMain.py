# Ryan Rupakheti
# Final Project
# 7/19/2026

#Import Needed Libraires and Class
import tkinter as tk
from tkinter import messagebox
from datetime import datetime as dt 
import requests
import calendar as cd
from PIL import Image, ImageTk
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


#File to open API key and read the key
with open("API_Info","r") as file:
    API_KEY = file.readline().strip()

BASE_URL1 = "https://api.openweathermap.org/data/2.5/weather?"
BASE_URL2 = "https://api.openweathermap.org/data/2.5/forecast?" 

# GUI Class for GUI functionality
class AppGUI():

    #Check if searched is already clicked
    Already_Clicked = 0
    City_Units = "metric"
    City_Input = ""

    #Intial Frame Setup
    def __init__(self):

        #Intializing GUI and adding demensions
        self.BG = "#2E94F4"
        self.root = tk.Tk()
        self.root.geometry("800x800")
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
        self.SaveB = tk.Button(self.ButtonGrid, text="Save",command=self.Save_City)
        self.HomeB = tk.Button(self.ButtonGrid, text="Home",command=self.HomePage)
        self.ConvertB = tk.Button(self.ButtonGrid, text="Convert to Fahrenheight",command=self.Convert)

        # Position them in one row
        self.HomeB.grid(row=0, column=0, sticky="ew", padx=5)
        self.SaveB.grid(row=0, column=1, sticky="ew", padx=5)
        self.ConvertB.grid(row=0, column=2, sticky="ew", padx=5)

        #Do not display intially
        self.ButtonGrid.forget()

        #Intro Label Use as Initial Prompt
        self.Intro_Label = tk.Label(self.root,text="Type a city to get weather and click search",font=("Arial",18),bg=self.BG)
        self.Intro_Label.pack(pady=10)

        #TextBox used to Get City
        self.textbox = tk.Text(self.root,height=1,font=("Arial",16))
        self.textbox.pack(padx=5,pady=5)

        #Serach button that displays information
        self.Search_B = tk.Button(self.root,text="Search",font=("Arial",18),command=self.Display_Info,bg=self.BG)
        self.Search_B.pack()

        #Making grid
        self.ForeCastGrid = tk.Frame(self.root,bg="white")
        #Makit it a 5 x 5
        for i in range(5):
            self.ForeCastGrid.columnconfigure(i,weight=1)
        #Forgetting it currently
        self.ForeCastGrid.forget()

        #SavedCity list to store cities
        self.SavedCity = []
        #Check if file exist if empty nothing store and made if not display
        try:
            with open("CityButtons.txt","r") as f:
              self.SavedCity = f.readline()
              self.SavedCity = self.SavedCity.split(",")
        except FileNotFoundError:
            messagebox.showerror("No File",'File not found')
           
        # List for all city button objects
        self.CityButton = []

        #Display prev stored cities
        self.SavedButtons()

        #This runs the GUI
        self.root.mainloop()

    #Get City Info
    def Display_Info(self,City=None):

        #Check if new city or saved city is given
        if City == None:
            #Get City
            self.City_Input = self.textbox.get("1.0",tk.END).strip()
            self.textbox.delete("1.0", tk.END)
        else:
            self.City_Input = City

        #Create two threads to get data
        with ThreadPoolExecutor() as executor:
            Dweather = executor.submit(Get_Weather_Data,self.City_Input,self.City_Units)
            Fweather = executor.submit(Get_ForeCast,self.City_Input,self.City_Units)

        #If cannot get data go to home
        try:
            #Get all Data For Labels
            Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W,City_Country,DCity_Icon,DCity_Sunrise,DCity_Sunset = Dweather.result()
        except KeyError:
            self.HomePage()
            messagebox.showerror("No City","Please enter a valid city")
            return
            
        # Remove Intro_Label for now
        self.Intro_Label.forget()

        #Put Button Frame on Top
        self.ButtonGrid.pack(before=self.textbox)

        #Forget city widgets when on page
        for widgets in self.CityButton:
            widgets.forget()
            
        #Send them to update labels which will check and chnage them
        self.Update_Labels(Daily_T,Daily_FeelT,Daily_Max,Daily_Min,Daily_H,Daily_Des,Daily_W,City_Country,self.City_Input,DCity_Icon,DCity_Sunrise,DCity_Sunset)

        #Check if i can get forecast if not go to home
        try:
            #Call Forcast with city and the units
            Five_Day = Fweather.result()
        except KeyError:
            messagebox.showerror("No City","Please enter a valid city")
            return
            

        #Display the 5 day forecast
        self.DisplayForeCast(Five_Day,self.City_Units)

        #If city not saved change button
        if self.City_Input in self.SavedCity:
            self.SaveB.config(text="Remove",command=self.Remove_City)
        else:
            self.SaveB.config(text="Save",command=self.Save_City)
        
        #Display forecast grid
        self.ForeCastGrid.pack(pady=10, fill="x")

    #Used to update and get new output
    def Update_Labels(self,UDaily_T,UDaily_FeelT,UDaily_Max,UDaily_Min,UDaily_H,UDaily_Des,UDaily_W,UCity_Country,UCity_Input,UCity_Icon,UCity_Sunrise,UCity_Sunset):

        #If metric use metric symbols
        if self.City_Units == "metric":
            self.ConvertB.config(text="Convert to Fahrenheight")
            SymbolT = "°C"
            SymbolM = "M/S"
        #Else imperial
        elif self.City_Units == "imperial":
            self.ConvertB.config(text="Convert to Celsius")
            SymbolT = "°F"
            SymbolM = "MPH"

        #Get the icon and put it in format for label later
        Icon_URL = f"https://openweathermap.org/img/wn/{UCity_Icon}@2x.png"

        response = requests.get(Icon_URL)

        image = Image.open(BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        
        #If Already Clicked was 0
        if self.Already_Clicked == 0:

            #Create all labels for display

            self.CityLabel = tk.Label(self.root,text=f"{UCity_Input},{UCity_Country}",bg=self.BG,font=("Arial",30),fg="black")
            self.CityLabel.pack()

            self.IconLabel = tk.Label(self.root,bg=self.BG,image=photo)
            self.IconLabel.image = photo
            self.IconLabel.pack()
        
            self.DesL = tk.Label(self.root,bg=self.BG,text=f"{UDaily_Des}",fg="black")
            self.DesL.pack()
        
            self.TempL = tk.Label(self.root,bg=self.BG,text=f"{UDaily_T}{SymbolT}",fg="black",font=("Arial",25))
            self.TempL.pack()
                    
            self.TempMML = tk.Label(self.root,bg=self.BG,text=f"Max: {UDaily_Max}{SymbolT}  Min: {UDaily_Min}{SymbolT}",fg="black",font=("Arial",20))
            self.TempMML.pack()
                    
            self.FeelL = tk.Label(self.root,bg=self.BG,text=f"Feels Like: {UDaily_FeelT}{SymbolT}",fg="black",font=("Arial",20))
            self.FeelL.pack()
                    
            self.HumL = tk.Label(self.root,bg=self.BG,text=f"Humidity: {UDaily_H}%",fg="black",font=("Arial",20))
            self.HumL.pack()
                    
            self.WinL = tk.Label(self.root,bg=self.BG,text=f"Wind Speed: {UDaily_W} {SymbolM}",fg="black",font=("Arial",20))
            self.WinL.pack()

            self.SunRS = tk.Label(self.root,bg=self.BG,text=f"Sunrise: {UCity_Sunrise}  Sunset: {UCity_Sunset}",fg="black",font=("Arial",20))
            self.SunRS.pack()
        else: 
            #Else config it to new City Value
            self.CityLabel.config(text=f"{UCity_Input},{UCity_Country}")
            self.CityLabel.pack()
            self.IconLabel.config(image=photo)
            self.IconLabel.image = photo
            self.IconLabel.pack()
            self.DesL.config(text=f"{UDaily_Des}")
            self.DesL.pack()
            self.TempL.config(text=f"{UDaily_T}{SymbolT}")
            self.TempL.pack()
            self.TempMML.config(text=f"Max: {UDaily_Max}{SymbolT}   Min: {UDaily_Min}{SymbolT}")
            self.TempMML.pack()
            self.FeelL.config(text=f"Feels Like: {UDaily_FeelT}{SymbolT}")
            self.FeelL.pack()
            self.HumL.config(text=f"Humidity: {UDaily_H} %")
            self.HumL.pack()
            self.WinL.config(text=f"Wind Speed: {UDaily_W} {SymbolM}")
            self.WinL.pack()
            self.SunRS.config(text=f"Sunrise: {UCity_Sunrise}  Sunset: {UCity_Sunset}")
            self.SunRS.pack()

        #Increment the Already Clicked Class Var
        self.Already_Clicked += 1

    # Convert function that changes the units for display
    def Convert(self):

        #First get new units
        self.City_Units = self.Convert_Units(self.City_Units)

        #Make two threads for forecast and display in threapool
        with ThreadPoolExecutor() as executor:
            CDweather = executor.submit(Get_Weather_Data,self.City_Input,self.City_Units)
            CFweather = executor.submit(Get_ForeCast,self.City_Input,self.City_Units)

        
        #Get all Data For Labels
        CDaily_T,CDaily_FeelT,CDaily_Max,CDaily_Min,CDaily_H,CDaily_Des,CDaily_W,CCity_Country,CCity_Icon,CCity_Sunrise,CCity_Sunset = CDweather.result()

        #Send them to update labels which will check and chnage them
        self.Update_Labels(CDaily_T,CDaily_FeelT,CDaily_Max,CDaily_Min,CDaily_H,CDaily_Des,CDaily_W,CCity_Country,self.City_Input,CCity_Icon,CCity_Sunrise,CCity_Sunset)

        #get all data for forecast
        CFive_Day = CFweather.result()

        #Display it for forecast
        self.DisplayForeCast(CFive_Day,self.City_Units)

    #Used by Convert to find conversion metric
    def Convert_Units(self,Units_G):
        if Units_G == "imperial":
            return "metric"
        else:
           return "imperial"

    #This displays the 5-day forecast by passing its dict and units
    def DisplayForeCast(self,Five_Day,FUnits):

        #If imperial put F else C
        if FUnits == "imperial":
            Symbol = "°F"
        else:
            Symbol = "°C"

        #Column counter to fill out grid
        column = 0

        # Loop through dictionary (I know key is not needed but could be for future chnage)
        for key, val in Five_Day.items():

            #Get the icon and put it in proper format
            Icon_URL = f"https://openweathermap.org/img/wn/{val['icon']}@2x.png"

            response = requests.get(Icon_URL)

            image = Image.open(BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)

            #Make label and add days on it
            DayLabel = tk.Label(self.ForeCastGrid, text=val['day'],bg="white",fg="black")

            #Then label for icon and add all icons
            IconLabel = tk.Label(self.ForeCastGrid,image=photo,bg="white")
            IconLabel.image = photo

            #Labels that has all High and Low temps
            HighLabel = tk.Label(self.ForeCastGrid, text=f"{val['high']}{Symbol}",bg="white",fg="black")
            LowLabel = tk.Label(self.ForeCastGrid, text=f"{val['low']}{Symbol}",bg="white",fg="black")

            #From each specifc row on grid fill out the column
            DayLabel.grid(row=0, column=column)
            IconLabel.grid(row=1, column=column)
            HighLabel.grid(row=2, column=column)
            LowLabel.grid(row=3, column=column)

            #Increment to stop overwrite
            column += 1

    #Adds city to list and txt file
    def Save_City(self):

        if self.City_Input not in self.SavedCity:
            self.SavedCity.append(self.City_Input)

        if self.City_Input in self.SavedCity:
            self.SaveB.config(text="Remove",command=self.Remove_City) 

        self.UpdateFile()


    #Removes city from list and txt file 
    def Remove_City(self):

        if self.City_Input in self.SavedCity:
            self.SavedCity.remove(self.City_Input)
            self.SaveB.config(text="Save",command=self.Save_City)

        self.UpdateFile()

    #Used by save and remove to write to file has excpetion handling in case it is gone
    def UpdateFile(self):
        try:
            with open("CityButtons.txt","w") as f:
                f.write(",".join(self.SavedCity))
        except FileNotFoundError:
            messagebox.showerror("No File","File not Found")
            return
        
    #Home page function for display
    def HomePage(self):

        # Clear the forcast grid fist anf then forget
        for widget in self.ForeCastGrid.winfo_children():
            widget.destroy()
        self.ForeCastGrid.forget()

        #Forget weather info label
        self.ButtonGrid.forget()
        self.CityLabel.forget()
        self.IconLabel.forget()
        self.DesL.forget()
        self.TempL.forget()
        self.TempMML.forget()
        self.FeelL.forget()
        self.HumL.forget()
        self.WinL.forget()
        self.SunRS.forget()

        #Dstroy old widgets so we dont repeat new ones
        for widgets in self.CityButton:
            widgets.destroy()
        #Clear the button from the cities saved list
        self.CityButton.clear()

        #Bring back intro label
        self.Intro_Label.pack(before=self.textbox)

        #Make new citysaved buttons
        self.SavedButtons()

    #This cretes the current widgets fro the saved ciites on home page
    def SavedButtons(self):
        #Create widgets based on list
        for i in self.SavedCity:
            if i != "":
                CButton = tk.Button(self.root,text=i,command= lambda city = i: self.Display_Info(city))
                CButton.pack(fill="x", padx=10, pady=2)
                self.CityButton.append(CButton)

     
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



def Get_ForeCast(CityF,FUnit):
    #Create API url for data
    url2 = BASE_URL2 + "appid=" + API_KEY + "&q=" + CityF + "&units=" + FUnit

    #Pull and put on JSON file
    Five_Day_F = requests.get(url2).json()

    #Stores only needed data
    five_day = {}
    
    # For each forecast in Five_Day_F
    for forecast in Five_Day_F['list']:
        # Get the date
        date = forecast['dt_txt'].split()[0]
        #If not in five_days intilize the data
        if date not in five_day:
            five_day[date]={
                'high': round(forecast['main']['temp_max']),
                'low': round(forecast['main']['temp_min']),
                'icon': forecast['weather'][0]['icon']
            }
        #Else comp current value with the current max and forecasr and update
        else:
            five_day[date]['high'] = round(max(five_day[date]['high'], forecast['main']['temp_max']))
            five_day[date]['low'] = round(min(five_day[date]['low'], forecast['main']['temp_min']))
    
    #This creates the day key by converting date string to day value  
    for key,value in five_day.items():
        Cdate = dt.strptime(key,"%Y-%m-%d")
        weekday = Cdate.weekday()
        five_day[key]["day"] = cd.day_abbr[weekday]

    #Return the needed dictionary 
    return five_day

#Main  fucntion to run GUI
def main():

    AppGUI()
 
if __name__ == "__main__":
    main()