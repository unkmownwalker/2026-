if __name__ == '__main__':
    def sum1(num):
        rs=0
        while num>=10:
            rs+=num%10
            num=int(num/10)
        rs+=num
        return rs
    a,b,c=input().split()
    a=int(a)
    b=int(b)
    c=int(c)
    s=sum1(a)+sum1(b)+sum1(c)
    while s>9:
        s=sum1(s)
    print(s)