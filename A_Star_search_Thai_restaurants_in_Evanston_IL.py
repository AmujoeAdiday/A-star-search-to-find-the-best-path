
import re
from math import cos, sqrt, sin, atan2,radians

def read_file():
    with open(file_name) as f:
        lines = [line.rstrip("\n") for line in f]
    return lines

def store_locations():
    latitude = []
    longitude = []
    for i in range(len(read_file())):
        latitude.append(read_file()[i].split(", ")[1])
        longitude.append(read_file()[i].split(", ")[2])
    return latitude, longitude

def pair_latitude_longitude():
    lat_list, long_list = store_locations()
    pair_x_y = []
    for i in range(len(lat_list)):
        pair_x_y.append([float(lat_list[i]), float(long_list[i])])
    return pair_x_y


def place_names():
    place_list = []
    for i in range(len(read_file())):
        place_list.append(read_file()[i].split(", ")[0])
    return place_list


def place_precodes():
    precode_list = []
    num_of_each_word = []

    for i in range(len(place_names())):
        precode_list.append(place_names()[i].split(" "))

    for i in range(len(precode_list)):
        num_of_each_word.append(len(precode_list[i]))

    return precode_list, num_of_each_word


def accumu(lis):
    accum_list = []
    total = 0
    for i in range(len(lis)):
        total += lis[i]
        accum_list.append(total)
    accum_list.insert(0, 0)
    return accum_list


def joinStrings(stringList):
    return ''.join(string for string in stringList)


def place_codes():
    precodes, freq_word = place_precodes()

    freq_word_accumulate = accumu(freq_word)

    codes = []

    for i in range(len(precodes)):
        for k in range(freq_word[i]):
            codes.append(precodes[i][k][0])
            # print(x[i][k][0])

    blended_list = []
    for i in range(len(precodes)):
        blended_list.append(joinStrings(codes[freq_word_accumulate[i]:freq_word_accumulate[i + 1]]))

    final_codes = []
    for i in range(len(blended_list)):
        final_codes.append(re.sub("[^A-Za-z]", "", blended_list[i]))

    return final_codes


def pair_actual_name_and_location():
    return dict(zip(place_names(), pair_latitude_longitude()))


def pair_code_and_actual_name_():
    return dict(zip(place_codes(), place_names()))


def pair_code_and_location():
    return dict(zip(place_codes(), pair_latitude_longitude()))


def declare_how_to_use_program():
    print("\n\nType the abbreviation codes according to places to find the best path travelling between those two.\n")

    abr = "Code"
    res = "Restaurant"

    print(f"{abr:<10}{res}")
    #print("CODE       restaurant")
    print("----------------------------------")
    for key, value in pair_code_and_actual_name_().items():
        print(f"{key:<10}{value}")
        #print(key, " for ", value)
    print("----------------------------------")
    print("\n")

    start = input("Start location ? ").upper()
    while start not in pair_code_and_actual_name_().keys():
        print("You typed the code incorrectly, please try again\n")
        start = input("Start location ? ").upper()

    destination = input("Destination ? ").upper()
    while destination not in pair_code_and_actual_name_().keys():
        print("You typed the code incorrectly, please try again\n")
        destination = input("Destination ? ").upper()

    while destination == start:
        print("destination and start should not be the same location")
        destination = input("Destination ? ").upper()
    print("\n")

    return start, destination


def get_start_place():
    return pair_code_and_actual_name_()[start]


def get_destination_place():
    return pair_code_and_actual_name_()[goal]


def distance_calculation(lat_1, long_1, lat_2, long_2):
    R = 6371
    delta_lat = radians(lat_2-lat_1)
    delta_long = radians(long_2-long_1)

    a = pow(sin(delta_lat / 2), 2) + cos(radians(lat_1)) * cos(radians(lat_2)) * pow(
        sin(delta_long / 2), 2)

    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))
    # its in km, but it doesn't matter in which unit when it comes to comparison


def location_with_its_closely_connection():
    location_list = []
    location_connection_list = []
    for i in range(len(read_file())):
        location_list.append(read_file()[i].split(", ")[0])
        location_connection_list.append(read_file()[i].split(", ")[3:])

    return dict(zip(location_list, location_connection_list))


def edges_with_location_name():
    edge_list = []
    for keys, values in location_with_its_closely_connection().items():
        for v in values:
            edge_list.append([keys, v])
    return edge_list


def edges_with_its_location():
    list_2 = []
    for i in edges_with_location_name():
        for j in i:
            for k, v in pair_actual_name_and_location().items():
                if j == k:
                    j = v
                    list_2.append(j)
    n = 2
    out = [list_2[k:k + n] for k in range(0, len(list_2), n)]
    return out


def distance_of_each_edge():
    distance_edge_list = []
    for i in range(len(edges_with_its_location())):
        distance_edge_list.append(
            distance_calculation(edges_with_its_location()[i][0][0], edges_with_its_location()[i][0][1],
                                 edges_with_its_location()[i][1][0], edges_with_its_location()[i][1][1]))
    return distance_edge_list


def pair_of_edge_actual_name_and_its_distance():
    new_list = []
    for i in edges_with_location_name():
        new_list.append(tuple(i))
    return dict(zip(new_list, distance_of_each_edge()))


def path_from_any_node_to_destination():
    destination_place = get_destination_place()
    lat_des = pair_actual_name_and_location()[destination_place][0]
    long_des = pair_actual_name_and_location()[destination_place][1]
    all_path_to_goal_list = []

    for keys, values in pair_actual_name_and_location().items():
        all_path_to_goal_list.append(distance_calculation(values[0], values[1], lat_des, long_des))
    return all_path_to_goal_list


def heuristic_path():
    path_list = []
    for i in range(len(place_names())):
        path_list.append((place_names()[i], pair_code_and_actual_name_()[goal]))
    return path_list


def pair_heuristic_path():
    return dict(zip(heuristic_path(), path_from_any_node_to_destination()))


def match_List_and_Dict(ls, dc):
    Temp_compare_path = {}
    for k,v in dc.items():
        for i in ls:
            if i == k:

                Temp_compare_path[k] = v
    return Temp_compare_path

def blend_temp_paths_and_unexpanded_path(tmp_dc,unexpanded_path,original_dict):
    return {**tmp_dc,**match_List_and_Dict(unexpanded_path,original_dict)}

def return_keys_from_dict(dc):
    lis = []
    for k in dc.keys():

        lis.append(k)
    return lis

def display_path(l):
    for i in range(1, len(l) - 1):
        if l[i][0] != l[i - 1][1]:
            l.remove(l[i])
    path_name = []
    path_name.append(l[0][0])
    for i in range(len(l)):
        path_name.append(l[i][1])

    str = ""
    for i in range(len(path_name) - 1):
        str += path_name[i] + " --> "
    str += path_name[len(path_name) - 1]
    print(str)

def A_star():
    start_node = pair_code_and_actual_name_()[start]
    temp = start_node
    goal_node = pair_code_and_actual_name_()[goal]
    cost_path_function = 0

    all_walk_through_path_list = []
    expanded_path = []
    unexpanded_path = []

    dict_all_paths = pair_of_edge_actual_name_and_its_distance()
    while start_node != goal_node:
        temp_dict = {k: v for k, v in dict_all_paths.items() if k[0] == start_node}
        #print("\nTEMP dict",temp_dict)
        all_walk_through_path_list += return_keys_from_dict(temp_dict)
        #print("ALL walk thorugh path ", all_walk_through_path_list)
        unexpanded_path += set(all_walk_through_path_list) - set(expanded_path)
        #print("UNexpanded path",unexpanded_path)
        To_compare_value_dict = blend_temp_paths_and_unexpanded_path(temp_dict, unexpanded_path,dict_all_paths)

        #print("ALL unexpanded dict,",To_compare_value_dict)
        # add heuristic cost to dictionary value

        for k, v in To_compare_value_dict.items():
            for k2, v2 in pair_heuristic_path().items():
                if k[1] == k2[0] and k2[1] == goal_node:
                    To_compare_value_dict[k] += v2

        new_node = list(To_compare_value_dict.keys())[list(To_compare_value_dict.values()).index(To_compare_value_dict[min(To_compare_value_dict, key=To_compare_value_dict.get)])][
            1]

        cost_path_function += To_compare_value_dict[min(To_compare_value_dict, key=To_compare_value_dict.get)]
        # remove the opposite direction
        # dict_all_paths.pop((new_node, start_node), None)
        start_node = new_node

        expanded_path.append(
            list(To_compare_value_dict.keys())[list(To_compare_value_dict.values()).index(To_compare_value_dict[min(To_compare_value_dict, key=To_compare_value_dict.get)])])



    #print("All expanded node,", expanded_path)
    print("\nSuccessfully found the best path \nfrom **", temp, "** to  **", goal_node, "** is\n")
    display_path(expanded_path)
    print("\n\n")

def help():
    print("\nThis program is to find the best path between Thai restaurants in Evanston, IL")
    print("\n\nMake sure to type only the abbreviation provided of both start and destination of the restaurants accordingly")
    print("For example : \n")

    print("CODE       restaurant")
    print("----------------------------------")
    print("ST         Siam Thai")
    print("BTC        Bangkok Thai Cuisine")
    print("----------------------------------")

    print("If you wish to start from Bangkok Thai Cuisine and stop at Siam Thai")
    print("Please type BTC for start and ST for destination which will be prompted to ask separately each time.\n\n")

file_name = "locations.txt"
start, goal = declare_how_to_use_program()
A_star()















