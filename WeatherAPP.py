# Ryan Rupakheti
# Final Porject
# 7/19/2026

#Import Needed Libraires
import tkinter as tk
import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_Key = "d04a6beeb2871b7cddacc06477b407b3"


# GUI Class for GUI functionality
class AppGUI():

    def __init__(self):

        #Intializing GUI and adding demensions
        self.root = tk.Tk()
        self.root.geometry("500x500")

        #Title
        self.root.title("Weather App")

        #Labels,Textboxes,and Buttons Below
        
        self.Intro_Label = tk.Label(self.root,text="Enter a city to get Weather",font=("Arial",18))
        self.Intro_Label.pack(pady=10)

        self.textbox = tk.Text(self.root,height=1,font=("Arial,16"))
        self.textbox.bind("<KeyPress>",self.display_input)
        self.textbox.pack(padx=10,pady=10)

        #This runs the GUI
        self.root.mainloop()

    
    def display_input(self,event):

        hasUse = 0

        #Checks if Enter has been enter
        if event.keysym == "Return" and event.state == 0:

            #Get City and Country incase there duplicates
            City_Input = self.textbox.get("1.0",tk.END)
            # Then delete whats stored in textbox
            self.textbox.delete("1.0", tk.END)

            #Remove intro label
            self.Intro_Label.forget()
            #New label about current input
            self.CityLabel = tk.Label(self.root,text=f"{City_Input}")
            self.CityLabel.pack()

   
#Main 
def main():

    #Open Gui
    AppGUI()

if __name__ == "__main__":
    main()

