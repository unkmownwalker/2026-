if __name__ == '__main__':
    n=int(input())
    days=[]
    names=[]
    for i in range(0,n):
        data=input().split()
        m=int(data[0])
        day={}
        for j in range(0,m):
            name=data[2*j+1]
            t=float(data[2*j+2])
            if name not in day:
                day[name]=t
            else:
                if t>day[name]:
                    day[name]=t
        days.append(day)
    
    for i in range(1,n):
        s1=days[i-1].keys()
        s2=days[i].keys()
        st=s1 & s2
        names=list(set(names) | st)
    names.sort()
    max=0
    for na in names:
        for i in range(0,n):
            if na in days[i] and days[i][na]>max:
                max=days[i][na]
        print(na,end=' ')
    print('')
    print(f"{max:.1f}")