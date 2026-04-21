if __name__ == '__main__':
    def huiwen(str):
        n=len(str)
        for i in range(0,n):
            if str[i]!=str[n-1-i]:
                return False
        return True
    
    sten=input().split()
    num=0
    for str in sten:
        if huiwen(str):
            num+=1
    print(num)