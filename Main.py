# Luis Ortiz #000855626

from ReadCSV import get_truck1, get_truck2, get_truck3, get_hash_table
from Delivery import start_delivery, get_driver1_start_time, get_driver2_start_time, get_driver1_return_time

# Given a package and a time, this function finds if the package is in route or at the hub.
# O(1)
def find_status_at_time(package, time):
    # If the package is in truck 1 and the time requested falls after driver 1's start time,
    # update the package's status to In Route and return that updated value.
    if package in get_truck1() and int(time) > int(str(get_driver1_start_time()).replace(":", "")):
        package[8] = "in Route"
        package[9] = ""
        return package

    # If the package is in truck 2 and the time requested falls after driver 2's start time,
    # update the package's status to In Route and return that updated value.
    elif package in get_truck2() and int(time) > int(str(get_driver2_start_time()).replace(":", "")):
        package[8] = "in Route"
        package[9] = ""
        return package

    # If the package is in truck 3 and the time requested falls after driver 1's return time from first
    # trip, update the package's status to In Route and return that updated value.
    elif package in get_truck3() and int(time) > int(str(get_driver1_return_time()).replace(":", "")):
        package[8] = "in Route"
        package[9] = ""
        return package

    # If none of the conditions are met, that means the package has not left the HUB yet. Update the
    # package's status to At Hub and return that updated package.
    else:
        package[8] = "at the Hub"
        package[9] = ""
        return package


# Starts the delivery simulation.
# O(n^2)
start_delivery()

print("\n\nHello, welcome to WGUSPS!\n")
print("Type \"ID\" if you want to know if a package has been delivered at a given time.")
print("Type \"ALL\" if you want to look up all packages at a given time.")
print("Type \"EXIT\" if you want to exit the program.\n")


request = ""

# Loop to keep the program running.
# O(n^2)
while request.upper() != "EXIT":
    try:
        request = input()

        # If ID is selected, ask for a time to check if the package has been delivered or not by that specific time.
        if request.upper() == "ID":
            package_id = input("Please enter the Package ID\n")
            value = get_hash_table().get(package_id)   # Hold a copy of the list with all the data to avoid changing original values.
            time_requested = input("Please enter a time in 24 hr format and include seconds. For example, 8:00:00 (8:00:00 AM) or 13:00:00 (1:00:00 PM).\n")

            # Create variables to hold the requested time and the delivered time without a format.
            # Example: 10:30:00 AM -> 103000
            time_requested_no_format = time_requested.replace(":", "")
            time_delivered_no_format = value[9].replace(":", "")

            # Check that the requested time is not passed 5:00 PM
            # According to how we are handling the time (without a format), the maximum time is 170000 (17:00:00)
            if int(time_requested_no_format) < 170001 and len(time_requested_no_format) >= 5:

                # If the time requested falls after the delivered time, display at what time the package was delivered.
                # Otherwise, display that package has not been delivered yet.
                if int(time_requested_no_format) >= int(time_delivered_no_format):
                    print("Package was delivered at ", value[9])
                else:
                    print("Package has not been delivered yet. It is", find_status_at_time(value, time_requested_no_format)[8])
                break
            else:
                print("Enter a time between 8:00 AM and 5:00 PM (17:00). Make sure to include seconds. Returning to the start of the program...")
                continue

        # If ALL is selected, ask for a time and display all package's data at that point in time.
        elif request.upper() == "ALL":
            time_requested = input(
                "Please enter a time in 24 hr format and include seconds. For example, 8:00:00 (8:00:00 AM) or 13:00:00 (1:00:00 PM).\n")

            # Create variable to hold the requested time without a format.
            # Example: 10:30:00 AM -> 103000
            time_requested_no_format = time_requested.replace(":", "")

            # Check that the requested time is not passed 5:00 PM
            # According to how we are handling the time (without a format), the maximum time is 170000 (17:00:00)
            if int(time_requested_no_format) < 170001 and len(time_requested_no_format) >= 5:

                # Loop through all the packages. Assign each package data to the "value" variable. This variable holds
                # the original package data values or it can be updated according to the requested time.
                # O(n)
                for i in range(1, 41):
                    value = get_hash_table().get(str(i))
                    time_delivered_no_format = value[9].replace(":", "")

                    # If the time requested falls after the delivered time, print the original value (which includes
                    # the delivered time.
                    if int(time_requested_no_format) >= int(time_delivered_no_format):
                        print(value)

                    # Find what is the status of all packages at the requested time and print their data.
                    else:
                        print(find_status_at_time(value, time_requested_no_format))

                break

            else:
                print("Enter a time between 8:00 AM and 5:00 PM (17:00). Make sure to include seconds. Returning to the start of the program...")
                continue

        else:
            print("Please type \"ID,\" \"ALL\" or \"EXIT.\" ")
            continue


    except ValueError:
        print("Input Error. Returning to the start of the program...")
        continue
