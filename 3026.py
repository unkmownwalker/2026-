if __name__ == '__main__':
    num=input()
    nums=list(num)
    total=0
    n=len(nums)
    for i in range(0,n):
        if int(nums[n-1-i]):
            total+=2**(i)
    print(total)
        
        