from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt


x = []

def update_data():
     # Connect to MySQL server
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="opticalenergymeter",
    database="oem"
    )

    # Get data from MySQL database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sensordata")
    rows = mycursor.fetchall()


    # Create empty matrix to store data
    data = []

    # Loop through each row and append timestamp and message to data matrix
    for row in rows:
        try:
            timestamp = datetime.strptime(str(row[2]), '%Y-%m-%d %H:%M:%S')
            message = int(row[1])
            data.append([timestamp, message])

        except:
            print(row,"failed")

    # Create x and y arrays for plotting
    x = [row[0] for row in data]
    y = [row[1] for row in data]

    # Plot graph using Matplotlib
    # Define plot space
    fig, ax = plt.subplots(figsize=(20, 12))

    ax.plot(x, y)
    ax.set(title = "OpticalEnergyMeter",
        xlabel = "timestamp",
        ylabel = "Energy (Wh)")
    plt.savefig("plot.png")

class OEMApp(App):
    def build(self):
        # Build the Layout
        layout = BoxLayout(orientation='vertical')

        # Update data from mysql and create Image
        update_data()

        # Load Image
        self.img = Image(source="plot.png")

        # create text (last update)
        self.last_update=Label(text=str(datetime.now()),size_hint=(1, .05))

        # Crete the Manual Update Button and bind Function
        butt=Button(text="refresh",size_hint=(1, .1))
        butt.bind(on_press=self.update_graph) 

        # Add To Layout
        layout.add_widget(self.img)
        layout.add_widget(self.last_update)
        layout.add_widget(butt)

        # Schedule Auto Update every Second
        Clock.schedule_interval(self.update_graph, 60)

        return layout
    
    def update_graph(self, instance=None):
        # Updat the Data and Graph

        # Update data from mysql and refresh Image
        update_data()
        print(datetime.now())

        # update text
        self.last_update.text=str(datetime.now())

        # Reload
        self.img.reload()

if __name__ == '__main__':
    OEMApp().run()