if __name__ == '__main__':
    def plural(str):
        dic=['a','e','i','o','u']
        if str[-1]=='s'or str[-1]=='x' or str[-1]=='z' or (str[-1]=='h' and(str[-2]=='s'or str[-2]=='c')):
            str+='es'
        elif str[-1]=='y' and str[-2] not in dic:
             str=str[:-1]+'ies'
        else:
            str+='s'
        return str 
    str1=str(input())
    print(plural(str1))