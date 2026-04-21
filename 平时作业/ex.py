if __name__ == '__main__':
    n=int(input())
    share=[]
    private=[]
    notpri=[]
    for i in range(0,n):
        ex=input().split()
        if i==0:
            share=ex
        else:
            share=[x for x in share if x in ex]
        for j in ex:
            if j in private:
                private.remove(j)
                notpri.append(j)
            if j not in notpri:
                private.append(j)

    if share:
       share.sort()
       for i in share:
           print(i,end=' ')
    else :
        print("None",end=' ')
    print('')
    if private:
       private.sort()
       for j in private:
          print(j,end=' ')
    else:
        print("None")