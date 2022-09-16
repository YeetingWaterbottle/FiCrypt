# import os
import io
from flask import Flask, request, render_template, url_for, redirect, send_file
# from markupsafe import escape

app = Flask(__name__)

# from tqdm import tqdm
# import time
from math import sqrt, floor, ceil

action = "en"
password = ""
# password = "Super Secure!38"
file_name = "input_file.png"


def get_list_width(byte_list_length, divide):
    if floor(sqrt(byte_list_length) / divide) % 2 == 0:
        return floor(sqrt(byte_list_length) / divide)

    elif ceil(sqrt(byte_list_length) / divide) % 2 == 0:
        return ceil(sqrt(byte_list_length) / divide)

    return -1


def str_to_byte(input, type, file_name=""):
    result = []
    if type == "string":
        for i in bytearray(input, encoding="utf8"):
            result.append(format(i, '08b'))

    elif type == "binary":
        for i in bytearray(input):
            result.append(format(i, '08b'))

    if file_name != "":
        result.extend(["00000000"] * 8)
        result.extend(str_to_byte(file_name, 'string'))

    return result


def set_array_width(byte_list, byte_list_length, list_width):
    result = []
    for i in range(0, byte_list_length, list_width):
        result.append(byte_list[i:i + list_width])

    return result


def check_add_padding(
    byte_list,
    list_width,
):
    if len(byte_list[-1]) != list_width:
        byte_list[-1] += (list_width - len(byte_list[-1])) * ["00000000"]

    return byte_list


def add_filename_data(str_bytes, file_name):
    return f"{str_bytes}{'00000000' * 8}{''.join(str_to_byte(file_name, 'string'))}"


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
            foo += "".join(row[byte:byte + count]) + " "
        result.append(foo.strip().split(" "))

    return result


def reverse_bytes(byte_list, direction, index=0):
    if direction == "horizontal":
        result = []
        if index == 0:
            for row in byte_list:
                result.append(row[::-1])
            return result

        for row in byte_list:
            result.append(row[:index] + row[:index - 1:-1])
        return result

    elif direction == "verticle":
        if index == 0:
            return byte_list[::-1]

        return byte_list[:index] + byte_list[:index - 1:-1]

    return -1


def mirror_bytes(byte_list):
    result = []
    for row in byte_list:
        foo = " ".join(row)

        foo = foo.translate(str.maketrans('01', '10'))

        result.append(foo.split(" "))

    return result


def encrypt_bytes(byte_list, password):
    password = str_to_byte(password, "string")
    password = split_bytes([password])[0]

    for byte in password:
        # for byte in tqdm(password):
        if byte[0] == "1":
            byte_list = mirror_bytes(byte_list)
            # print("Mirror Bytes")
        if byte[1] == "1":
            byte_list = reverse_bytes(byte_list, "horizontal")
            # print("Reverse Bytes Horizontally")
        if byte[2] == "1":
            byte_list = reverse_bytes(byte_list, "verticle")
            # print("Reverse Bytes Vertically")
        if byte[3] == "1":
            if byte[1] == "1":
                byte_list = reverse_bytes(byte_list, "horizontal",
                                          len(byte_list[0]) // 2)
                # print("Reverse Bytes Half Horizontally")
            if byte[2] == "1":
                byte_list = reverse_bytes(byte_list, "verticle",
                                          len(byte_list) // 2)
                # print("Reverse Bytes Half Vertically")
    return byte_list


def decrypt_bytes(byte_list, password):
    password = str_to_byte(password, "string")
    password = split_bytes([password])[0]

    for byte in password[::-1]:
        # for byte in tqdm(password[::-1]):
        if byte[3] == "1":
            if byte[2] == "1":
                byte_list = reverse_bytes(byte_list, "verticle",
                                          len(byte_list) // 2)
                # print("Reverse Bytes Half Vertically")
            if byte[1] == "1":
                byte_list = reverse_bytes(byte_list, "horizontal",
                                          len(byte_list[0]) // 2)
                # print("Reverse Bytes Half Horizontally")

        if byte[2] == "1":
            byte_list = reverse_bytes(byte_list, "verticle")
            # print("Reverse Bytes Vertically")

        if byte[1] == "1":
            byte_list = reverse_bytes(byte_list, "horizontal")
            # print("Reverse Bytes Horizontally")

        if byte[0] == "1":
            byte_list = mirror_bytes(byte_list)
            # print("Mirror Bytes")

    return byte_list


def save_bytes(byte_list, action, file_name=""):
    foo = []
    result = bytearray()
    for row in byte_list:
        for byte in row:
            foo.append(byte)

    if action == "de":
        file_name = ""
        reading_name = False
        match = 0
        counter = 0

        for byte in foo[::-1]:
            counter += 1

            if byte != "00000000":
                reading_name = True
                match = 0
                file_name += chr(int(byte, 2))

            if byte == "00000000" and reading_name == True:
                match += 1

            if match >= 8 and reading_name == True:
                break

        file_name = file_name[::-1]

    if action == "en":
        for byte in foo:
            result.append(int(byte, 2))

    if action == "de":
        for byte in foo[:-counter]:
            result.append(int(byte, 2))

    # with open(file_name, "wb") as file:
    #     file.write(result)

    # print(f"Output File Name: {file_name}")

    return result


def print_bytes(byte_list):
    for row in byte_list:
        print(row)


def file_encryption(action, file_input, password):
    if action == "en":
        file_name = file_input.filename

    elif action == "de":
        file_name = "encrypted.enc"

    input_str = file_input.read()

    if action == "en":
        input_bin = str_to_byte(input_str, "binary", file_name)

    if action == "de":
        input_bin = str_to_byte(input_str, "binary")

    input_len = len(input_bin)
    result = []

    width_segment = get_list_width(input_len, 2)

    result = set_array_width(input_bin, input_len, width_segment)

    result = check_add_padding(result, width_segment)

    # print("Original Input Binary")
    # print_bytes(result)

    result = split_bytes(result)

    # password = input("Input Password: ")
    # start_time = time.time()
    # print("Password Set to: " + password)

    if action == "en":
        result = encrypt_bytes(result, password)

    if action == "de":
        result = decrypt_bytes(result, password)

    # print("Combined Back to 8-bit Bytes")
    result = combine_bytes(result, 2)

    # print_bytes(result)

    if action == "en":
        return save_bytes(result, action, "encrypted.enc")
    if action == "de":
        return save_bytes(result, action)

    # print("Encrypted Saved!")

    # print(f"--- Program Ran In {time.time() - start_time} Seconds ---")


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/inspirations")
def inspirations_page():
    return render_template("inspirations.html")


@app.get("/encrypt")
def encrypt_page():
    return render_template("encrypt.html")


@app.post("/encrypt")
def encrypt_file():
    if "file" not in request.files:
        return "Error: No File Part"

    file = request.files["file"]
    password = request.form["file_password"]
    action = request.form["action"]

    if file.filename == "":
        return "Error: No File Selected"

    # print(f'OUTPUT TYPE: {file_encryption("en", file, password)}', flush=True)

    if action == "en":
        read_binary_file = io.BytesIO(file_encryption("en", file, password))

        return send_file(read_binary_file, as_attachment=True, download_name="encrypted.enc")

    if action == "de":
        read_binary_file = io.BytesIO(file_encryption("de", file, password))

        return send_file(read_binary_file, as_attachment=True, download_name="encrypted.done")

    # return redirect(url_for("download_page"))


# @app.route("/download")
# def download_page(file):
#     file_binary = file.read()
#     return render_template("download.html")
