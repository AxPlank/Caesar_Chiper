key_dictt = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5,
    'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
    'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15,
    'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
    'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
    'Z': 26
}

def encryption(inputt, interval):
    """
    암호화
    """
    output = interval
    interval = key_dictt[interval]
    for index in inputt:
        temp = ord(index)
        if temp >= 65 and temp <= 90:
            temp += interval
            if temp > 90:
                gap = temp - 90
                temp = 64 + gap
                output += chr(temp)
            else:
                output += chr(temp)
        elif temp >= 97 and temp <= 122:
            temp += interval
            if temp > 122:
                gap = temp - 122
                temp = 96 + gap
                output += chr(temp)
            else:
                output += chr(temp)
        else:
            output += chr(temp)

    return output

def decryption(inputt):
    """
    복호화
    """
    key = inputt[2]
    inputt = inputt[3:len(inputt)-1]
    interval = key_dictt[key]
    output = ''
    for index in inputt:
        temp = ord(index)
        if temp >= 65 and temp <= 90:
            temp -= interval
            if temp < 65:
                gap = 65 - temp
                temp = 91 - gap
                output += chr(temp)
            else:
                output += chr(temp)
        elif temp >= 97 and temp <= 122:
            temp -= interval
            if temp < 97:
                gap = 97 - temp
                temp = 123 - gap
                output += chr(temp)
            else:
                output += chr(temp)
        else:
            output += chr(temp)

    return output