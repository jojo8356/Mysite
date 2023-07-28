def encrypt(msg):
    return " ".join([bin(x).split("0b")[1][::-1] for x in msg.encode("utf-8")])

def decrypt(msg):
    return bytes([int(x[::-1], 2) for x in msg.split(" ")]).decode("utf-8")