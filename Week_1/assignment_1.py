## Steps to Solve the Winnipeg Transit Assignment

# Step 1: Sign Up for the API Key
# - Go to the Winnipeg Transit API website and sign up to get API key.
# - The API key is a unique code that will be used to access Winnipeg Transit data.

# Step 2: Define the Distance Range
# - Use the API key to make a request for live transit information.
# - Example: To get data about a specific area, use the following URL format:
#   https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}
# - The data will be returned in JSON format if added ".json" to the path.

# Step 3: Get Stop Schedules
# - Once you have the stops, you can retrieve the schedule for each stop.
# - Use the stop number you retrieved earlier to get the schedule using the API.
# - Example: https://api.winnipegtransit.com/v3/stops/STOP_NUMBER/schedule.json?api-key=YOUR-API-KEY
# - This will give you the upcoming bus or transit schedules for the selected stop.


'''
This program finds nearby transit stops based on user-specified
latitude, longitude, and distance, allowing users to view scheduled
and actual arrival times for selected routes.
Author: Mandeep
Created: 2024-08-26
Updated: 2024-08-27
'''

# This is delaying the request (async)
from requests import get

# The imports for bonus part
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore, Style

# Required Vaiables
# 49.90107199622515, -97.14183211390886
# 49.895, -97.138
API_KEY = "GWCBU5pFSy6HORe80t9C"
lon = -97.09
lat = 49.91
distance = 200

# URL to get available stops
url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

# Try Retrieving the data in JSON format using the URL
# and storing data as Dictionary
try:
    resp_stops = get(url_stops).json()

    if resp_stops['stops'] == None:
        raise ValueError("No stops found in the specified area.")

    # printing the stop number and names using data from
    # resp_stops dictionary
    for stop in resp_stops['stops'] :
        print(f"Stop Number: {stop['key']}, Stop Name: {stop['name']}")

    # Prompting the user to input the stop number
    # he is interested in
    user_input = input("Enter the Stop Number: ")
# url_schedule = f"https://api.winnipegtransit.com/v3/stops/{user_input}/schedule.json?max-results-per-route=2&api-key={API_KEY}"

    # Customizing the URL to get schedule for the stop
    try:
        # Customizing the URL to get schedule for the stop
        url_schedule = f"https://api.winnipegtransit.com/v3/stops/{user_input}/schedule.json?max-results-per-route=2&api-key={API_KEY}"
        res_url_schedule = get(url_schedule).json()
        # extracting data from res_url_schedule and storing it in
        # route_schedules variable
        route_schedules = res_url_schedule["stop-schedule"]["route-schedules"]

        # printing routes name and number

        for route_schedule in route_schedules:
            print("============================================")
            print(f"Route: {route_schedule['route']['name']}\n")

            # Diving deep into the nested dictionary to get information
            # about route_stop
            for route_stop in route_schedule['scheduled-stops'] :
                # Getting the schedule arrival time
                scheduled_arrival = parse(route_stop['times']['arrival']['scheduled'])
                # Getting schedule estimated time
                estimated_arrival = parse(route_stop['times']['arrival']['estimated'])

                # fixing the console to get my color coded output
                just_fix_windows_console()

                # Color Coding output in Green if bus is on time
                if scheduled_arrival == estimated_arrival :
                    print(Fore.GREEN + f"Scheduled Arrival: {scheduled_arrival}")
                    print(Fore.GREEN + f"Estimated Arrival: {estimated_arrival}\n")

                # Color Coding output in Blue if bus is early
                elif scheduled_arrival > estimated_arrival :
                    print(Fore.BLUE + f"Scheduled Arrival: {scheduled_arrival}")
                    print(Fore.BLUE + f"Estimated Arrival: {estimated_arrival}\n")

                # Color Coding output in Red if bus is late
                else :
                    print(Fore.RED + f"Scheduled Arrival: {scheduled_arrival}")
                    print(Fore.RED + f"Estimated Arrival: {estimated_arrival}\n")
                print(Style.RESET_ALL)
    except ValueError as E:
            print(f"The stop {user_input} is not in the provided list.\n")
except ValueError as e:
    print(f"Error: {e}")






