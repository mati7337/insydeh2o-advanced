import sys

password_types = {
    "admin": 0x231000,
    "user": 0x231800
}

password_encoding = {
    0x02: "1",
    0x03: "2",
    0x04: "3",
    0x05: "4",
    0x06: "5",
    0x07: "6",
    0x08: "7",
    0x09: "8",
    0x0a: "9",
    0x0b: "0",

    0x10: "q",
    0x11: "w",
    0x12: "e",
    0x13: "r",
    0x14: "t",
    0x15: "y",
    0x16: "u",
    0x17: "i",
    0x18: "o",
    0x19: "p",

    0x1e: "a",
    0x1f: "s",
    0x20: "d",
    0x21: "f",
    0x22: "g",
    0x23: "h",
    0x24: "j",
    0x25: "k",
    0x26: "l",

    0x2c: "z",
    0x2d: "x",
    0x2e: "c",
    0x2f: "v",
    0x30: "b",
    0x31: "n",
    0x32: "m",
}

def read_password(data, offset):
    output = {}

    password_len = data[offset]
    if password_len == 0xff:
        return False # No password

    password_encoded = []
    for i in range(password_len):
        password_encoded.append(data[offset + 1 + i])

    output["encoded"] = password_encoded
    output["decoded"] = []

    for i in output["encoded"]:
        output["decoded"].append(password_encoding.get(i, "?"))

    output["idk_last_byte"] = data[offset + password_len + 1]

    return output

def print_password(password, debug=False):
    if debug:
        print("Debug info:")
        tmp_hex = []
        for i in password["encoded"]:
            tmp_hex.append(hex(i))
            print(f"Encoded: {', '.join(tmp_hex)}")
        print("Last byte", hex(password["idk_last_byte"]))
        print()
    print(f"Password: {''.join(password['decoded'])}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f" {sys.argv[1]} BIOS_DUMP [PASSWORD_TYPE]")
        print("Available password types:")
        print(f"  {', '.join(password_types.keys())}")

    with open(sys.argv[1], "rb") as fl:
        data = fl.read()

    if len(sys.argv) < 3:
        password_to_read = password_types.keys()
    else:
        password_to_read = sys.argv[2]

    try:
        for i in password_to_read:
            print(f"=== {i} ===")
            password = read_password(data, password_types[i.lower()])
            if password:
                print_password(password, debug=False)
            else:
                print("No password")
            print()
    except IndexError:
        print(f"Invalid password type selected: {sys.argv[2]}")
        print("Available password types:")
        print(f"  {', '.join(password_types.keys())}")

