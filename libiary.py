if __name__ == '__main__':
    n=int(input())
    dic={}
    for i in range(0,n):
        key,value=input().split(' ')
        value=int(value)
        if key not in dic:
            dic[key]=value
        else:
            dic[key]+=value
    dic1=sorted(dic.items())
    dic2=sorted(dic1,key=lambda x :x[1],reverse=True)
    if len(dic2)<=3:
        for i in range(0,len(dic2)):
            print(dic2[i][0]+' '+str(dic2[i][1]))
    else:
        for i in range(0,3):
             print(dic2[i][0]+' '+str(dic2[i][1]))