if __name__ == '__main__':
    dic=['+','-','*','/','^']
    def count(i,j,k):
        i=int(i)
        j=int(j)
        if k=='+':
            return i+j
        elif k=='-':
            return i-j
        elif k=='*':
            return i*j
        elif k=='/':
            return i/j
        else :
            return i**j
    ss=input().split()
    while len(ss)>1:
        n=len(ss)
        for i in range(0,n):
            if ss[i] in dic:
                ss[i]=count(ss[i-2],ss[i-1],ss[i])
                ss.remove(ss[i-1])
                ss.remove(ss[i-2])
                break
    print(int(ss[0]))
