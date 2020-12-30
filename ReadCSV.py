# Luis Ortiz #000855626

import csv
from HashTable import HashTable

"""
Open Package File and read contents from it.
O(n)
"""
with open("WGUPS Package File.csv", newline='', encoding='utf-8-sig') as csvFile:
    reader = csv.reader(csvFile)
    packages_table = HashTable()  # Instance of the HashTable Class
    truck1 = []
    truck2 = []
    truck3 = []
    MAX_TRUCK_SIZE = 16

    # Insert data from the Package File into the Hash Table instance in key-value pairs.
    # O(n)
    for row in reader:
        package_ID_value = row[0]
        address_value = row[1]
        city_value = row[2]
        state_value = row[3]
        zip_value = row[4]
        delivery_deadline_value = row[5]
        weight_value = row[6]
        note_value = row[7]
        delivery_status = "at hub"
        delivered_time = ""
        package_data = [package_ID_value, address_value, city_value, state_value, zip_value, delivery_deadline_value,
                        weight_value, note_value, delivery_status, delivered_time]
        key = package_ID_value
        value = package_data

        # Statements that determine how to load the packages into the Trucks. The Data Structure from here creates a
        # nested list for quick lookup.

        # If a package has a delivery deadline, load that package into either Truck 1 or 2 according to the note in the package.
        if delivery_deadline_value != "EOD":
            if "Must" in note_value:
                truck1.append(value)
            elif "Delay" in note_value:
                truck2.append(value)
            else:
                truck1.append(value)

        # If a package does not have a delivery deadline, load the package into Truck 2 if there's a constraint,
        # to Truck 3 until it is full or if the package has the wrong address, or to Truck 1 if Truck 2 has more packages.
        if delivery_deadline_value == "EOD":
            if "Can only be on truck 2" in note_value:
                truck2.append(value)
            elif "Delay" in note_value:
                truck2.append(value)
            elif "Wrong" in note_value:
                value[1] = "410 S State St"
                value[2] = "Salt Lake City"
                value[3] = "UT"
                value[4] = "84111"
                truck3.append(value)
            elif len(truck3) < MAX_TRUCK_SIZE:
                truck3.append(value)
            elif len(truck2) < len(truck1):
                truck2.append(value)
            else:
                truck1.append(value)

        # Insert full package into the Hash Table.
        packages_table.add_update(key, value)


    # Function used to optimze Trucks. Compare the packages' addresses from Truck1/Truck2 against Truck3. As long as
    # the package does not have a Wrong Address listed, add to Truck 1 or Truck 2 whatever package that is being
    # delivered to the same address by Truck 1 or Truck 2.
    # O(n^2)
    def optimize_truck(truck):
        for i in truck:
            for j in truck3:
                if "Wrong" not in j[6]:
                    if i[0] == j[0]:
                        if len(truck) < MAX_TRUCK_SIZE:
                            truck.append(j)
                            truck3.remove(j)

    # Get Packages from Truck 1. O(1)
    def get_truck1():
        return truck1

    # Get Packages from Truck 2. O(1)
    def get_truck2():
        return truck2

    # Get Packages from Truck 3. O(1)
    def get_truck3():
        return truck3

    # Get the Hash Table with all the Packages. O(1)
    def get_hash_table():
        return packages_table

    # Call the optimize function to optimize Trucks 1 and 2.
    optimize_truck(truck1)
    optimize_truck(truck2)
