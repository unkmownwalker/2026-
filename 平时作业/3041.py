if __name__ == '__main__':
    str=input()
    chars=list(str)
    n=len(chars)
    max=0
    num=1
    for i in range(1,n):
        if chars[i]>=chars[i-1]:
            num+=1
        else:
            num=1
        if num>max:
            max=num
    print(max)        
    