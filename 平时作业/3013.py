if __name__ == '__main__':
    n=input()
    a=input().split()
    b=input().split()
    for i in b:
        if i not in a:
            a.append(i)
    a.sort()
    for j in a:
        print(int(j),end=' ')
