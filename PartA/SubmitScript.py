import hashlib
import hmac
import time
import requests
from base64 import b32decode, b64encode,  b32encode
import base64
import struct

def hotp(key, counter, digits=8, digest='sha256'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)


def totp(key, time_step=30, digits=8, digest='sha256'):
    return hotp(key, int(time.time() / time_step), digits, digest)

if __name__ == '__main__':
    action = int(input("checksum/kumpul? (0/1): "))
    secret = 'seleksister2213520163'
    secret = b32encode(bytearray(secret,'ascii')).decode('utf-8')
    if(action == 0):
        #shasum
        inputFile = "partA/13520163.pdf"
        openedFile = open(inputFile, "rb")
        readFile = openedFile.read()
        shaHash = hashlib.sha256(readFile)
        shaHashed = shaHash.hexdigest()
        openedFile.close()
        print("First 5 SHAsum: "+ shaHashed[:5])
        secret2 = '12345678901234567890'
        secret2 = b32encode(bytearray(secret2,'ascii')).decode('utf-8')
        print(totp(secret2))
    else:
        #data
        body = {
                "fullName" : "Frederik Imanuel Louis",
                "link"     : "https://drive.google.com/drive/folders/1_x30uA5XYF1EtwvSddlnAGJwzBJ-DgTV?usp=sharing",
                "message"  : "https://myanimelist.net/manga/55215/Utsuro_no_Hako_to_Zero_no_Maria"
        }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "Basic ",
            "Content-Length": "211"
        }

        #otp
        userid = "13520163"
        otp = (totp(secret))
        authToken = b64encode(bytes(userid+":"+otp, 'utf-8')).decode('ascii')
        headers["Authorization"] += authToken
        print(headers["Authorization"])
        #request
        url = "http://svr.suggoi.fun:42069/submit/a"
        req = requests.post(url, json=body, headers=headers)
        print(req.status_code)
        print(req.text)