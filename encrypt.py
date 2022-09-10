from math import sqrt, floor, ceil


def get_list_width(byte_list_length, divide):
    if floor(sqrt(byte_list_length)) % 2 == 0:
        return int(floor(sqrt(byte_list_length)) / divide)

    elif ceil(sqrt(byte_list_length)) % 2 == 0:
        return int(ceil(sqrt(byte_list_length)) / divide)


def str_to_byte(input_str):
    result = []
    for i in bytearray(input_str, encoding='utf-8'):
        result.append(format(i, '08b'))

    return result


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
    foo = ""
    for byte in byte_list:
        half = len(byte) // 2
        foo += f"{byte[:half]} {byte[half:]} "
        
    return foo.strip().split(" ")

def reverse_bytes(byte_list, direction):
    if direction == "horizontal":
        result = []
        for row in byte_list:
            result.append(row[::-1])

        return result

    elif direction == "verticle":
        return byte_list[::-1]

    return -1

# input_str = input("good luck: ")
input_str = "take the total of the binaries and then square root it and minus one."
input_len = len(input_str)
input_bin = str_to_byte(input_str)
result = []

splitted_result = []

width_segment = get_list_width(input_len, 2)

result = set_array_width(input_bin, input_len, width_segment)

result = check_add_padding(result, width_segment)


for i in result:
    splitted_result.append(split_bytes(i))

# for i in splitted_result:
#     print(i)
print(splitted_result[0])

reverse_result = reverse_bytes(splitted_result, "verticle")
print("-"*64)

print(reverse_result[-1])
print(len(reverse_result))
# for i in reverse_result:
#     print(i)