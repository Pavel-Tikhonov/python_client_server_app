import chardet
rawdata = open('test.txt', "rb").read()
result = chardet.detect(rawdata)
charenc = result['encoding']
print(charenc)

with open('test.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line)









