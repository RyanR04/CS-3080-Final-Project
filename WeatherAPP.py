# Ryan Rupakheti
# Final Porject
# 7/19/2026

#Import Needed Libraires
import tkinter as tk
import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"


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


    def City_Info(self):


        #Remove Intro_Label for now
        self.Intro_Label.forget()

        #Get City
        City_Input = self.textbox.get("1.0",tk.END).strip()
        # Then delete whats stored in textbox
        self.textbox.delete("1.0", tk.END)

        if self.Already_Clicked == 0:
            self.CityLabel = tk.Label(self.root,text=f"{City_Input}",font=("Arial",20))
            self.CityLabel.pack()
        else: 
            self.CityLabel.config(text=f"{City_Input}")

        self.Already_Clicked += 1



#Main 
def main():

    #Open Gui
    AppGUI()

if __name__ == "__main__":
    main()

