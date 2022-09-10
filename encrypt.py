import time
start_time = time.time()


from math import sqrt, floor, ceil

def get_list_width(byte_list_length, divide):
    if floor(sqrt(byte_list_length)) % 2 == 0:
        return int(floor(sqrt(byte_list_length)) / divide)

    elif ceil(sqrt(byte_list_length)) % 2 == 0:
        return int(ceil(sqrt(byte_list_length)) / divide)


def str_to_byte(input, type):
    result = []
    if type == "string":
        for i in bytearray(input, encoding="utf8"):
            result.append(format(i, '08b'))

        return result

    elif type == "binary":
        for i in bytearray(input):
            result.append(format(i, '08b'))
        
        return result

    return -1


def set_array_width(byte_list, byte_list_length, list_width):
    result = []
    for i in range(0, byte_list_length, list_width):
        result.append(byte_list[i:i + list_width])

    return result


def check_add_padding(byte_list, list_width):
    if len(byte_list[-1]) != list_width:
        byte_list[-1] += (list_width - len(byte_list[-1])) * ["00000000"]

    return byte_list


def split_bytes(byte_list):
    result = []
    for row in byte_list:
        foo = ""
        for byte in row:
            half = len(byte) // 2
            foo += f"{byte[:half]} {byte[half:]} "
        result.append(foo.strip().split(" "))

    return result


def combine_bytes(byte_list, count):
    result = []
    for row in byte_list:
        foo = ""
        for byte in range(0, len(row), count):
            foo += "".join(row[byte:byte+count]) + " "
        result.append(foo.strip().split(" "))

    return result


def reverse_bytes(byte_list, direction):
    if direction == "horizontal":
        result = []
        for row in byte_list:
            result.append(row[::-1])

        return result

    elif direction == "verticle":
        return byte_list[::-1]

    return -1

def save_encrypted(byte_list, file_name):
    result = bytearray()
    for row in byte_list:
        for byte in row:
            result.append(int(byte, 2))

    with open(file_name, "wb") as file:
        file.write(result)

    return result

# with open("your_face_up_my_meat_jeremy.mp3", "rb") as file:
#     input_str = file.read()
# input_str = input("good luck: ")
input_str = "take the total of the binaries and then square root it and minus one."
input_len = len(input_str)
input_bin = str_to_byte(input_str, "string")
result = []



width_segment = get_list_width(input_len, 2)

result = set_array_width(input_bin, input_len, width_segment)

result = check_add_padding(result, width_segment)

result = split_bytes(result)

reverse_result = reverse_bytes(result, "horizontal")

reverse_result = combine_bytes(reverse_result, 2)

print(reverse_result)

save_encrypted(reverse_result, "hello.txt")

print(f"--- {time.time() - start_time} seconds ---")