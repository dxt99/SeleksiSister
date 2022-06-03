import random

def calculateRedundant(size):
    i = 0
    while(i**2 < i + size +1):
        i+=1
    return i

def randomBit():
    return chr(ord('0') + random.randint(0,1))

def createRandomHamming(size):
    redundant = calculateRedundant(size)
    power = 0
    ret = ([])
    data = ''
    for i in range(size+redundant):
        if (2**power == i):
            ret.insert(0,'0')
            power+=1
        else:
            temp = randomBit()
            ret.insert(0, temp)
            data = temp + data
    for i in range(redundant):
        num = 2**i
        count = 0
        for j in range(1, size+1):
            if num&j != 0 and ret[len(ret) - j] == '1': 
                count += 1
        if (count%2 == 1):
            ret[len(ret) - num] = '1'
    return (data, ''.join(ret))

if __name__ == '__main__':
    data, hamming = createRandomHamming(26)
    print(data)
    print(hamming)
