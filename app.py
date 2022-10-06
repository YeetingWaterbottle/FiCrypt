# import os
import io
from flask import Flask, request, render_template, send_file
from math import sqrt, floor, ceil
import numpy as np
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def get_list_width(byte_list_length, divide):
    radicand = sqrt(byte_list_length / divide)
    if floor(radicand) % 2 == 0:
        return floor(radicand)

    elif ceil(radicand) % 2 == 0:
        return ceil(radicand)

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

    return [result, file_name]


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

    result = split_bytes(result)


    if action == "en":
        result = encrypt_bytes(result, password)

    if action == "de":
        result = decrypt_bytes(result, password)

    # print("Combined Back to 8-bit Bytes")
    result = combine_bytes(result, 2)

    if action == "en":
        return save_bytes(result, action, "encrypted.enc")
    if action == "de":
        return save_bytes(result, action)

    # print("Encrypted Saved!")


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
    file = request.files["file"]
    if "file" not in request.files:
        return "<h1>Error: No File Part</h1>"

    if file.filename == "":
        return "<h1>Error: No File Selected</h1>"

    password = request.form["file_password"]
    if password == "":
        return "<h1>Error: Password Required</h1>"

    if len(password) > 16:
        return "<h1>Error: Password Length Over Max Characters</h1>"

    action = request.form["action"]
    if action == "de" and file.filename.split(".")[-1] != "enc":
        return "<h1>Error: File Not Encrypted. File Extenshion Needs to Be \".enc\"</h1>"

    if action == "en":
        binary_file = file_encryption("en", file, password)
        return send_file(io.BytesIO(binary_file[0]), as_attachment=True, download_name=binary_file[1])

    if action == "de":
        binary_file = file_encryption("de", file, password)
        return send_file(io.BytesIO(binary_file[0]), as_attachment=True, download_name=binary_file[1])
