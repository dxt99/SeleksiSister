import hashlib
import hmac
import math
import time
import requests
import json
from base64 import b64encode

def dynamic_truncation(raw_key: hmac.HMAC, length: int) -> str:
    bitstring = bin(int(raw_key.hexdigest(), base=16))
    last_four_bits = bitstring[-4:]
    # >> 0011
    offset = int(last_four_bits, base=2)
    # >> 3
    chosen_32_bits = bitstring[offset * 8 : offset * 8 + 32]
    # >> 01000100011001000111110010101110
    full_totp = str(int(chosen_32_bits, base=2))
    # >> 1147436206
    return full_totp[-length:]
    # >> 436206


def generate_totp(shared_key: str = "seleksister22" + "13520163", length: int = 8):
    now_in_seconds = math.floor(time.time())
    step_in_seconds = 30
    t = math.floor(now_in_seconds / step_in_seconds)
    hash = hmac.new(
        bytes(shared_key, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha256,
    )

    return dynamic_truncation(hash, length)

if __name__ == '__main__':
    action = int(input("checksum/kumpul? (0/1): "))
    if(action == 0):
        #shasum
        inputFile = "partA/13520163.pdf"
        openedFile = open(inputFile, "rb")
        readFile = openedFile.read()
        shaHash = hashlib.sha256(readFile)
        shaHashed = shaHash.hexdigest()
        openedFile.close()
        print("First 5 SHAsum: "+ shaHashed[:5])
    else:
        #data
        body = {
                "fullName" : "Frederik Imanuel Louis",
                "Link"     : "https://drive.google.com/drive/folders/1_x30uA5XYF1EtwvSddlnAGJwzBJ-DgTV?usp=sharing",
                "Message"  : "https://myanimelist.net/manga/55215/Utsuro_no_Hako_to_Zero_no_Maria"
        }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "Basic ",
        }

        
        #otp
        userid = "13520163"
        otp = (generate_totp())
        authToken = b64encode(bytes(userid+":"+otp, 'utf-8')).decode('ascii')
        headers["Authorization"] += authToken

        #request
        url = "http://svr.suggoi.fun:42069/submit/a"
        req = requests.post(url, json=body, headers=headers)
        print(req.status_code)
        print(req.text)