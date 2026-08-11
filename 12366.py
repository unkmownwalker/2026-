import random
def shuwei(i):
    num=0
    while i>=10:
         num+=i%10
         i=int(i/10)
    num+=i
    return num
    
def compare(i,j):
    if shuwei(i)<shuwei(j):
            return True
    elif shuwei(i)==shuwei(j) and i<j:
            return True
    else:
            return False

def quicksort(al,low,high):
      i,j=low,high
      if i>=j:
            return al
      rand = random.randint(low, high)
      a[i],a[rand]=a[rand],a[i]
      key=a[i]
      while i<j:
            while i<j and not compare(al[j],key):
                  j-=1
            al[i]=al[j]
            while i<j and (compare(al[i],key) or al[i]==key) :
                  i+=1
            al[j]=al[i]
            al[i]=key
      quicksort(al,low,i-1)
      quicksort(al,j+1,high)
      
n=input()
m=input()
n,m=int(n),int(m)
a=[]
for i in range(0,n):
    a.append(i+1)
quicksort(a,0,n-1)
print(a[m-1])