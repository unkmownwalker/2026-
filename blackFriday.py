if __name__ == '__main__':
    year=input()
    year=int(year)
    da=[1,3,5,7,8,10,12]
    xi=[4,6,9,11]
    total=0
    days=0
    for i in range(1998,year):
        if (i%4==0 and i%100!=0) or(i%100==0 and i%400==0):
            days+=366
        else:
            days+=365
    day=(4+days%7)%7    #每年的1月1日
    days=12
    for j in range(1,13):
        day=(day+days%7)%7    #一次算一个月的13号
        if day==5:
            total+=1
        if j in da:
            days=31
        elif j in xi:
            days=30
        elif j==2 and ((year%4==0 and year%100!=0) or(year%100==0 and year%400==0)):
            days=29
        else:
            days=28

    print(total)
