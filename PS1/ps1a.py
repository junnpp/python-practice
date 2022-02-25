###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Junhyeok Park
# Collaborators:
# Time: 30 min (계속 추가할 것)

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    the_dict = {}
    with open(filename, "r") as f:
        read_data =  f.readlines()

        for i in read_data:
            i = i.strip("\n").split(",")
            the_dict[i[0]] = i[1]

        return the_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = cows.copy()

    # convert the value type of weight from str to int
    for i in cows_copy:
        cows_copy[i] = int(cows_copy[i])

    # initialize trips list
    trips = []

    # loop
    while len(cows_copy) > 0:
        current_weight = 0
        heaviest_weight = 0
        heaviest_cow = ""
        current_trip = []

        # decide the current heaviest
        for i in cows_copy.keys():
            if cows_copy[i] > heaviest_weight:
                heaviest_weight = cows_copy[i]
                heaviest_cow = i

        current_trip.append(heaviest_cow)
        current_weight += heaviest_weight
        del cows_copy[heaviest_cow]

        # looking for other cows that can fit (see all possible cows and pick the heaviest one)
        possible_cows = {}
        for i in cows_copy.keys():
            if cows_copy[i] + current_weight <= 10:
                possible_cows[i] = cows_copy[i]

        # sorting possible cows by weight
        if len(possible_cows) != 0:
            sorted_possible_cows = []
            possible_cows_copy = possible_cows.copy()

            while len(sorted_possible_cows) < len(possible_cows):
                # choose the heaviest among the possible cows that can be fitted
                possible_heaviest_weight = 0

                for i in possible_cows_copy.keys():
                    if possible_cows_copy[i] > possible_heaviest_weight:
                        heaviest = i
                        possible_heaviest_weight = cows_copy[i]

                # remove the current heaviest from the possible cows list
                del possible_cows_copy[heaviest]

                # rearrange the possible cows
                if len(sorted_possible_cows) == 0:
                    sorted_possible_cows.append(heaviest)
                elif possible_cows[heaviest] >= possible_cows[sorted_possible_cows[0]]:
                    sorted_possible_cows.insert(0, heaviest)
                elif possible_cows[heaviest] <= possible_cows[sorted_possible_cows[-1]]:
                    sorted_possible_cows.insert(len(sorted_possible_cows), heaviest)


            for i in sorted_possible_cows:
                if current_weight + cows_copy[i] <= 10:
                    current_trip.append(i)
                    current_weight += cows_copy[i]
                    del cows_copy[i]
                else:
                    break

            trips.append(current_trip)

        else:
            trips.append(current_trip)

    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # initialize copy of the dictionary and trip list that will be returned.
    cows_copy = cows.copy()
    for i in cows_copy:
        cows_copy[i] = int(cows_copy[i])
    trips = []

    # make a list with cow names
    cow_names = []
    for cow in cows_copy.keys():
        cow_names.append(cow)

    # generate every possible trips
    for trip in get_partitions(cow_names):
        below_limit = True

        for current_trip in trip:
            weight = 0

            # calculate current trip weight
            for cow in current_trip:
                weight += cows_copy[cow]

            # break out of the loop if current trip weights beyond the limit
            if weight > limit:
                below_limit = False
                break

        # include a trip that any of each trip does not go beyond limit
        if below_limit:
            trips.append(trip)

    return trips




        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass

if __name__ == "__main__":
    cows = load_cows("ps1_cow_data.txt")
    # print(greedy_cow_transport(cows, 10))

    print(brute_force_cow_transport(cows, 10))

