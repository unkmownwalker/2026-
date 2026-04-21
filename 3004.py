if __name__ == '__main__':
    def invernum(num):
        invern=0
        while num>=10:
            d=num%10
            invern=invern*10+d
            num=int(num/10)
        invern=num+invern*10
        return invern
    a,b=input().split()
    a,b=int(a),int(b)
    sum=invernum(a)+invernum(b)
    print(invernum(sum))