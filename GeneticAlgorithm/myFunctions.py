import numpy


def TakeSecond(array):
    return array[1]


def TakeTime(array):
    # time_id is index 2
    return array[2]


# encode chromozome for genetic alg
def encodeNumbers(args):
    encoded = ""
    for number in args:
        if not (type(number) == int or type(number) == numpy.int64):
            print("err")
        formatted = format(number+1, "b")
        if len(formatted) < 16:
            encoded += "0" * (16 - len(formatted)) + formatted
    return int(encoded, 2)


# decode chromozome for genetic alg
def decodeNumber(encoded):
    encoded = format(encoded, "b")
    while len(encoded) % 16 != 0:
        encoded = "0" + encoded
    decoded = []
    while encoded != "":
        myNumber = encoded[0:16]
        decoded.append(int(myNumber, 2)-1)
        encoded = encoded[16:]
    return decoded
