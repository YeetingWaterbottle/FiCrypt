from math import sqrt, floor, ceil

input_str = "take the total of the binaries and then square root it and minus one."
input_len = len(input_str)
input_bin = []
result = []

for i in bytearray(input_str, encoding='utf-8'):
    input_bin.append(format(i, '08b'))

width_segment = floor(sqrt(input_len))

if floor(sqrt(input_len)) % 2 == 0:
    width_segment = floor(sqrt(input_len))

elif ceil(sqrt(input_len)) % 2 == 0:
    width_segment = ceil(sqrt(input_len))

for i in range(0, input_len, width_segment):
    result.append(input_bin[i:i + width_segment])

if len(result[-1]) != width_segment:
    result[-1] += (width_segment - len(result[-1])) * ["00000000"]

for i in result:
    print(i)
