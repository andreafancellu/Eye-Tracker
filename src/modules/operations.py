import time

def current_milli_time(starting_time):
    return round((time.time() - starting_time)* 1000)

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

def write_array_file(dataset, path):
    file = open(path, "w")

    for i in range(len(dataset)):
        file.write(str(dataset[i]) + " ")

    file.close()

def save_dataset(dataset, path):
    file = open(path, "w")

    if path == "data\gaze.txt":
        for i in range(len(dataset)):
            file.write(str(dataset[i].get_gaze()) + " ")
            file.write(str(dataset[i].get_time()) + "\n")
        file.close()
    elif path == "data\keys.txt":
        for i in range(len(dataset)):
            file.write(str(dataset[i].get_key()) + " ")
            file.write(str(dataset[i].get_ms()) + "\n")
        file.close()
    elif path == "data\\face.txt":
        for i in range(len(dataset)):
            file.write(str(dataset[i].get_right()) + " ")
            file.write(str(dataset[i].get_left()) + " ")
            file.write(str(dataset[i].get_up()) + " ")
            file.write(str(dataset[i].get_down()) + " ")
            file.write(str(dataset[i].get_time()) + "\n")
        file.close()
    elif path == "data\\face_all.txt":
        for i in range(len(dataset)):
            file.write(str(dataset[i].get_pixel()) + " ")
            file.write(str(dataset[i].get_time()) + "\n")
        file.close()