from math import sqrt, floor, ceil

def get_list_width(byte_list_length):
    if floor(sqrt(byte_list_length)) % 2 == 0:
        return floor(sqrt(byte_list_length))
 
    elif ceil(sqrt(byte_list_length)) % 2 == 0:
        return ceil(sqrt(byte_list_length))

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
    result = []
    for row in byte_list:
        for byte in row:
            half = len(byte)//2
            result.append([byte[:half], byte[half:]])

    return result

input_str = "take the total of the binaries and then square root it and minus one."
input_len = len(input_str)
input_bin = str_to_byte(input_str)
result = []

width_segment = get_list_width(input_len)

result = set_array_width(input_bin, input_len, width_segment)

result = check_add_padding(result, width_segment)

result = split_bytes(result)


for i in result:
    print(i)
