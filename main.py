import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



pulses_per_kWh = 1000
hours_lapse = 1

def update_data(pulses_kWh, lapse):
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

    # Create x and y 
    x = [row[0] for row in data]
    y = [row[1]*(1000/pulses_kWh) for row in data]  

    # Plot graph using Matplotlib

    fig, ax = plt.subplots(figsize=(20, 12))
    ax.plot(x,
            y,
            marker = 'o',
            color = 'blue')

    # Set titles
    ax.set(title = "OpticalEnergyMeter",
        xlabel = "timestamp",
        ylabel = "Energy (Wh)")
    ax.grid()
    
    # format x Axis
    plt.setp(ax.get_xticklabels(), rotation = 90)
    plt.xlim(datetime.now()- timedelta(hours=lapse), datetime.now())

    
    # Save piture
    plt.savefig("plot.png")

    # calculate Total Energy
    total_energy=0
    print("calculating energy for interval= ", datetime.now() - timedelta(hours=lapse),"to", datetime.now())

    for i in range(0, len(x)):
        if (datetime.now() - timedelta(hours=lapse)) <= x[i] <= (datetime.now()):
            print(x[i], y[i])
            total_energy = total_energy + y[i]

    return int(total_energy)


class OEMApp(App):
    def build(self):
        # Build the Layout
        layout = BoxLayout(orientation='vertical')


        # Update data from mysql and create Image
        total_energy = update_data(pulses_per_kWh, hours_lapse)

        # Load Image
        self.img = Image(source="plot.png")

        # create text (energy for the interval)
        self.total_energy_text = Label(text = "Energy used for the shown Interval = >> " + str(total_energy) + " Wh <<", size_hint=(1, .05))

        # create text (last update)
        layout_hor = BoxLayout(orientation='horizontal',size_hint=(1, .05))
        self.last_update=Label(text=str(datetime.now()),size_hint=(0.4, 1))
        layout_hor.add_widget(Label(text="last Updated= ",size_hint=(0.2, 1),halign="right"))
        layout_hor.add_widget(self.last_update)

        # create kWh box
        self.input_p_kWh = TextInput(text=str(pulses_per_kWh),size_hint=(0.25, 1), input_filter = 'float', multiline=False)
        layout_hor.add_widget(Label(text="pulses/kWh= ",size_hint=(0.2, 1), halign="right"))
        layout_hor.add_widget(self.input_p_kWh)

        # create hour box
        self.hours = TextInput(text=str(hours_lapse),size_hint=(0.2, 1),input_filter = 'float', multiline=False)
        layout_hor.add_widget(Label(text="hours= ",size_hint=(0.2, 1), halign="right"))
        layout_hor.add_widget(self.hours)

        # Crete the Manual Update Button and bind Function
        butt=Button(text="refresh",size_hint=(1, .1))
        butt.bind(on_press=self.update_graph) 

        # Add To Layout
        layout.add_widget(self.img)
        layout.add_widget(self.total_energy_text)
        layout.add_widget(layout_hor)
        layout.add_widget(butt)

        # Schedule Auto Update every Second
        Clock.schedule_interval(self.update_graph, 60)

        return layout
    
    def update_graph(self, instance=None):
        try:
            # Update vars
            pulses_per_kWh = int(self.input_p_kWh.text)
            hours_lapse = float(self.hours.text)

            # Update data from mysql and refresh Image
            total_energy = update_data(pulses_per_kWh,hours_lapse)
            
            # update text
            self.last_update.text=str(datetime.now())
            self.total_energy_text.text = "Energy used for the shown Interval = >> " + str(total_energy) + " Wh <<"

            # Reload
            self.img.reload()
        except:
            pass

if __name__ == '__main__':
    OEMApp().run()