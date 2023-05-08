import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

# Connect to MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="opticalenergymeter",
  database="oem"
)

# Create cursor object
mycursor = mydb.cursor()

# Execute query to select all data from sensordata table
mycursor.execute("SELECT * FROM sensordata")

# Fetch all rows from the result set
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
plt.plot(x, y)
plt.xlabel('Timestamp')
plt.ylabel('Message')
plt.title('Sensor Data')
plt.show()