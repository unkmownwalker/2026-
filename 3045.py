if __name__ == '__main__':
    str=input()
    dic={'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z' }
    sten=[]
    word=''
    chars=str.split(' ')
    for i in chars:
        if i=='':
            if word:
                sten.append(word)
                word=''
        else:
            if i in dic:
                word+=dic[i]
    if word:
        sten.append(word)
    result=sten[0]
    for i in range(1,len(sten)):
        result+=' '+sten[i]
    print(result)