# Ryan Rupakheti
# Final Porject
# 7/19/2026


#Import Needed Libraires
import tkinter as tk


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
        self.textbox.pack(padx=10,pady=10)

        #This runs the GUI
        self.root.mainloop()


#Main 
def main():

    #Open Gui
    AppGUI()





if __name__ == "__main__":
    main()

