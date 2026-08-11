if __name__ == '__main__':
    map=[[0,9,8,7,6,5,4,3],[1,2,3,4,5,6,7,8],[2,3,4,6,7,8,9,6],[4,5,6,7,8,9,0,7],
         [4,3,2,1,6,7,8,9],[5,8,4,9,0,4,3,2],[3,4,6,7,8,4,3,2],[2,4,6,8,9,7,5,3]]
    def sum1(i,j,p,q):
        num=0
        if i==p:
          if j<q:
             for k in range(j,q):
                 num+=map[i-1][k]
          if q<j:
             for k in range(q-1,j-1):
                 num+=map[i-1][k]
        if j==q:
            if i<p:    
              for k in range(i,p):
                 num+=map[k][j-1]
            if p<i:
               for k in range(p-1,i-1):
                 num+=map[k][j-1]
        return num
    n=int(input())
    dot=[]
    tol=0
    for i in range(0,n):
       di=input().split()
       dp=[int (s) for s in di]
       dot.append(dp)
       if i==0:
          tol+=map[dot[0][0]-1][dot[0][1]-1]
       else:
         tol+=sum1(dot[i-1][0],dot[i-1][1],dot[i][0],dot[i][1])
    print(tol)
  