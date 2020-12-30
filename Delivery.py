# Luis Ortiz #000855626

import csv
import datetime
from ReadCSV import get_truck1, get_truck2, get_truck3, get_hash_table

# Open Addresses File, read contents from it and store the data in a Addresses list.
# O(1)
with open("Addresses.csv", newline='', encoding='utf-8-sig') as addressesFile:
    addressesReader = csv.reader(addressesFile)
    addresses = list(addressesReader)

# Open Distance Table File, read contents from it and store the data in a Distances list.
# O(1)
with open("WGUPS Distance Table.csv", newline='', encoding='utf-8-sig') as distancesFile:
    distancesReader = csv.reader(distancesFile)
    distances = list(distancesReader)

truck1 = get_truck1()
truck2 = get_truck2()
truck3 = get_truck3()
driver1_start_time = datetime.timedelta(hours=8, minutes=0, seconds=00)  # Driver 1 starts at 8:00 AM
driver2_start_time = datetime.timedelta(hours=9, minutes=5, seconds=00)  # Driver 2 starts at 9:05 AM
HUB = addresses[0][0]  # Starting Point / Hub
speed = 18  # Trucks' Average Speed per hour.

# Given an address, find and return the index where that address is in the Addresses list.
# O(1)
def find_in_addresses(address):
    address_to_list = [address]
    if address_to_list in addresses:
        return addresses.index(address_to_list)

# Given 2 addresses, find and return the distance between them by using their index within the Distances List.
# O(1)
def find_in_distances(address1, address2):
    return distances[address1][address2]


# Get Driver 1's start time. O(1)
def get_driver1_start_time():
    return driver1_start_time


# Get Driver 2's start time. O(1)
def get_driver2_start_time():
    return driver2_start_time


# Get Driver 1's return time from first trip. O(1)
def get_driver1_return_time():
    return driver1_return_time


# This function calculates how much time passes when delivering a package according to the miles traveled.
# O(1)
def calculate_time_of_delivery(miles):
    miles_per_minute = speed / 60
    time_passed = round((miles / miles_per_minute), 2)
    string_time = str(time_passed).split(".")
    result = string_time[0] + ":" + str(round(float(string_time[1]) * 0.6))
    formatted_time = datetime.datetime.strptime(result, "%M:%S")
    return formatted_time - datetime.datetime(1900, 1, 1)

# This function finds if there are any delivery deadlines left in the packages from a Truck.
# O(n)
def find_any_delivery_deadline(truck):
    answer = False
    for i in truck:
        if "EOD" not in i[5]:
            answer = True
            break
    return answer


""" GREEDY ALGORITHM 

My sorting algorithm uses a greedy style and it is divided in 2 methods: find_closest_distance and travel_using_shortest_path.

    The first function (find_closest_distance) takes 2 parameters: a truck full of packages and a beginning location.
Additionally, it will return a list of values: the closest distance, the current address of the truck and the overall
package value to be removed later on.

    The second function (travel_using_shortest_path) takes 3 parameters: a truck, a start point (which will always be
the HUB), and the start time of the driver. It will return a list of 2 values: the total amount of miles traveled from
the start point (HUB) until the truck is back at the HUB, and the miles that are in between the Truck's last delivery
address and the HUB.

The way this greedy algorithm works is the following:
At the start of the simulation, the second function calls the first function in order to calculate what the route is 
going to be. Once it knows this route, it will calculate the total amount of miles travel, it will update the package's
status to "Delivered" and it will calculate the time spent between each delivery. Since the second function iterates
through all of the packages in a given truck, it needs to remove whatever package that has been delivered. In order to 
do so, a copy of the original list of packages in a truck is created, and using the data returned from the first
function, it can safely remove a package from the copy (which will not alter the original values). Finally, once all
the packages are delivered and their information is updated, the second function will return the total amount of miles
traveled, and also how many miles are in between the Truck's last delivery address and the HUB (which will be used to 
determine the minimum amount of miles that could be reached).


Since both functions have a Time - Space Complexity of O(n), this Greedy Algorithm has an overall Time - Space
Complexity of O(n^2)
"""
def find_closest_distance_between_packages(truck, beginning):

    # It starts by creating a variable that assumes that the closest distance (in Miles) to the beginning location is
    # 50. Another variable is created to hold the beginning location, this is done due to the fact that the truck's
    # current location will change everytime it delivers a package. It then assigns the index of the current location
    # to the start_index variable. It sets the priority time to 11:59 AM and creates a variable that will hold a
    # boolean value to check if there are more packages with delivery deadlines.
    closest_distance = 50.0
    current_address = beginning
    start_index = find_in_addresses(current_address)
    priority_time = "11:59 AM"
    more_priorities = find_any_delivery_deadline(truck)

    # This function iterates through all packages of the provided truck, comparing all of the miles between the
    # current location and all of the possible destination from the truck. This is done through a set of constraints.
    # O(n)
    for i in truck:
        destination_index = find_in_addresses(i[1])
        if find_in_distances(destination_index, start_index) == '':
            miles_in_between = float(find_in_distances(start_index, destination_index))
        else:
            miles_in_between = float(find_in_distances(destination_index, start_index))

        # If there is a package which has the same address as the truck's current address, it delivers that package
        # regardless of time priorities.
        if start_index == destination_index:
            priority_time = i[5]
            closest_distance = miles_in_between
            current_address = i[1]
            item_to_delete = i
            package_data = [closest_distance, current_address, item_to_delete]
            return package_data

        # However, if it finds a package that has a delivery deadline, it checks whether or not the deadline is in
        # the morning (AM) or the afternoon (PM). Since the delivery times will be set in a 24 hour format,
        # it adds 12 hours to the delivery deadlines that are in the afternoon (PM).
        if i[5] != "EOD":
            package_hour_deadline = ""
            package_minute_deadline = ""
            if i[5][-2] == "A":
                package_hour_deadline = i[5][0:-6]
                package_minute_deadline = i[5][-5:-3]
            elif i[5][-2] == "P":
                package_hour_deadline = str(int(i[5][0:-6]) + 12)
                package_minute_deadline = i[5][-5:-3]

            # If there is a package that has a sooner delivery deadline, it prioritizes the delivery of that specific
            # package.
            if int(package_hour_deadline) < int(priority_time[0:-6]):
                priority_time = i[5]
                closest_distance = miles_in_between
                current_address = i[1]
                item_to_delete = i
            elif int(package_hour_deadline) == int(priority_time[0:-6]):
                if int(package_minute_deadline) < int(priority_time[-5:-3]):
                    priority_time = i[5]
                    closest_distance = miles_in_between
                    current_address = i[1]
                    item_to_delete = i

                # If it finds 2 packages with the same delivery deadline, it prioritizes whichever package has the least
                # amount of miles to travel.
                elif int(package_minute_deadline) == int(priority_time[-5:-3]):
                    if closest_distance > miles_in_between:
                        closest_distance = miles_in_between
                        current_address = i[1]
                        item_to_delete = i
                        priority_time = i[5]

        # If it cannot find a package that has to be delivered earlier, it selects the closest distance to
        # travel based on the least amount of miles.
        elif not more_priorities:
            if closest_distance > miles_in_between:
                closest_distance = miles_in_between
                current_address = i[1]
                item_to_delete = i

    # Finally, it gathers all of the data that will be used and puts it in a list. It then returns that list.
    package_data = [closest_distance, current_address, item_to_delete]
    return package_data


def travel_using_shortest_path(truck, start_point, current_time):

    # This function starts by creating a global variable that will hold the time of return after all packages are
    # delivered, a total of miles traveled, a copy of the truck's packages (to avoid removing from the original values)
    # and a delivered time that will hold the latest delivered time.
    global time_after_return
    total = 0
    copy = truck.copy()
    delivered_time = current_time

    # It iterates through all of the truck's packages, calling the first function (find_closest_distance) each time
    # to determine the least amount of miles to travel between deliveries.
    # O(n)
    for i in range(len(copy)):
        package_data = find_closest_distance_between_packages(copy, start_point)

        # Once it knows the miles it has to travel, it adds them up.
        miles = float(package_data[0])
        total += miles

        # Once a package has been delivered, the truck's start point is updated to the latest delivery address.
        start_point = package_data[1]

        # Updates the delivered package status.
        truck[truck.index(package_data[2])][8] = "Delivered"

        # Calculates how much time passed until the delivery was done and updates the package delivery time value.
        time_spent = calculate_time_of_delivery(miles)
        delivered_time = delivered_time + time_spent
        truck[truck.index(package_data[2])][9] = str(delivered_time)

        # Updates the hash table with the latest package's data.
        get_hash_table().add_update(package_data[2][0], truck[truck.index(package_data[2])])

        # Removes the already delivered package from the copy (to avoid delivery to the same address twice)
        copy.remove(package_data[2])

    # Once all packages are delivered, it calculates how many miles it has to travel from the truck's latest location
    # to the HUB.
    miles_to_HUB = float(find_in_distances(find_in_addresses(start_point), find_in_addresses(HUB)))
    total += miles_to_HUB
    delivered_time = delivered_time + calculate_time_of_delivery(miles_to_HUB)
    start_point = HUB
    time_after_return = delivered_time
    return [total, miles_to_HUB]


# This function starts the delivery simulation by calling the greedy algorithms for truck 1, 2 and 3.
# It also prints the total miles traveled, as well as the total miles traveled excluding the miles to bring truck 3
# and truck 2 back to the HUB.
# O(n^2)
def start_delivery():
    global driver1_return_time
    print("Starting Delivery Simulation...")
    print("There are ", len(truck1), " packages in Truck 1")
    print("There are ", len(truck2), " packages in Truck 2")
    print("There are ", len(truck3), " packages in Truck 3")
    miles_from_truck1 = travel_using_shortest_path(truck1, HUB, driver1_start_time)
    driver1_return_time = time_after_return
    miles_from_truck3 = travel_using_shortest_path(truck3, HUB, time_after_return)
    miles_from_truck2 = travel_using_shortest_path(truck2, HUB, driver2_start_time)
    print("All packages have been delivered!")
    print("Total miles traveled having all trucks return to the HUB:")
    print(miles_from_truck1[0] + miles_from_truck3[0] + miles_from_truck2[0])
    print("Total miles traveled with only one truck returning to the HUB:")
    print(round(miles_from_truck1[0] + miles_from_truck2[0] - miles_from_truck2[1] + miles_from_truck3[0] - miles_from_truck3[1], 2),)

