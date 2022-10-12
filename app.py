# import os
import io
from flask import Flask, request, render_template, send_file
from math import sqrt, floor, ceil
import numpy as np
from base64 import b64encode, b64decode
import itertools

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def get_list_width(byte_list_length, divide):
    radicand = sqrt(byte_list_length / divide)
    if floor(radicand) % 2 == 0:
        return floor(radicand)

    else:
        return ceil(radicand)

def convert_base64(string, action):
    if action == "en":
        return b64encode(string.encode()).decode()

    elif action == "de":
        return b64decode(string).decode()


def str_to_byte(input, type, file_name=""):
    result = []
    if type == "string":
        for i in bytearray(input, encoding="utf8"):
            result.append(format(i, "08b"))

    elif type == "binary":
        for i in bytearray(input):
            result.append(format(i, "08b"))

    if file_name != "":
        result.extend(["00000000"] * 8)
        result.extend(str_to_byte(convert_base64(file_name, "en"), "string"))
        result.extend(["00000000"] * 4)
        result.extend(str_to_byte(str(len(file_name)), "string"))

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


def split_bytes(byte_list, list_width):
    result = "".join(list(itertools.chain.from_iterable(byte_list)))

    result = [result[i:i+4] for i in range(0, len(result), 4)]

    return set_array_width(result, len(result), list_width)


def combine_bytes(byte_list, list_width):
    result = "".join(list(itertools.chain.from_iterable(byte_list)))

    result = [result[i:i+8] for i in range(0, len(result), 8)]

    return set_array_width(result, len(result), list_width)


def reverse_bytes(byte_list, direction, index=0):
    if direction == "horizontal":
        if index == 0:
            return np.fliplr(byte_list)
            
        return np.concatenate((byte_list[:, :index], np.fliplr(byte_list[:, index:])), axis=1)


    elif direction == "verticle":
        if index == 0:
            return np.flipud(byte_list)

        return np.concatenate((byte_list[:index], np.flipud(byte_list[index:])), axis=0)

    raise Exception("direction inputted does not match any presets.")


def mirror_bytes(byte_list, width_segment):
    result = "".join(list(itertools.chain.from_iterable(byte_list)))

    result = result.translate(str.maketrans('01', '10'))

    result = [result[i:i+4] for i in range(0, len(result), 4)]

    return set_array_width(result, len(result), width_segment)


def encrypt_bytes(byte_list, password, width_segment):
    password = str_to_byte(password, "string")
    password = split_bytes([password], len(password) * 2)[0]

    for byte in password:
        if byte[0] == "1":
            print("Mirror Bytes")
            byte_list = mirror_bytes(byte_list, width_segment)
        if byte[1] == "1":
            print("Reverse Bytes Horizontally")
            byte_list = reverse_bytes(byte_list, "horizontal")
        if byte[2] == "1":
            print("Reverse Bytes Vertically")
            byte_list = reverse_bytes(byte_list, "verticle")
        if byte[3] == "1":
            if byte[1] == "1":
                print("Reverse Bytes Half Horizontally")
                byte_list = reverse_bytes(byte_list, "horizontal", len(byte_list[0]) // 2)
            if byte[2] == "1":
                print("Reverse Bytes Half Vertically")
                byte_list = reverse_bytes(byte_list, "verticle", len(byte_list) // 2)
    return byte_list


def decrypt_bytes(byte_list, password, width_segment):
    password = str_to_byte(password, "string")
    password = split_bytes([password])[0]

    for byte in password[::-1]:
        if byte[3] == "1":
            if byte[2] == "1":
                print("Reverse Bytes Half Vertically")
                byte_list = reverse_bytes(byte_list, "verticle", len(byte_list) // 2)
            if byte[1] == "1":
                print("Reverse Bytes Half Horizontally")
                byte_list = reverse_bytes(byte_list, "horizontal", len(byte_list[0]) // 2)

        if byte[2] == "1":
            print("Reverse Bytes Vertically")
            byte_list = reverse_bytes(byte_list, "verticle")

        if byte[1] == "1":
            print("Reverse Bytes Horizontally")
            byte_list = reverse_bytes(byte_list, "horizontal")

        if byte[0] == "1":
            print("Mirror Bytes")
            byte_list = mirror_bytes(byte_list, width_segment)

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

    print("to byte")
    if action == "en":
        input_bin = str_to_byte(input_str, "binary", file_name)

    if action == "de":
        input_bin = str_to_byte(input_str, "binary")
    print("dont to byte")

    input_len = len(input_bin)
    result = []

    width_segment = get_list_width(input_len, 2)
    print("to 2d")
    result = set_array_width(input_bin, input_len, width_segment)
    print("done to 2d")

    print("add padd1")
    result = check_add_padding(result, width_segment)
    print("done pad")

    print("split in half")
    result = split_bytes(result, width_segment)
    print("done split in half")

    if action == "en":
        result = encrypt_bytes(result, password, width_segment)

    if action == "de":
        result = decrypt_bytes(result, password, width_segment)

    # print("Combined Back to 8-bit Bytes")
    result = combine_bytes(result, width_segment)

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
