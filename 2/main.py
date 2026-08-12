import re

def fmt(x):
    if not isinstance(x,str):return x
    a=re.fullmatch(r'\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*',x)
    if not a:return x
    return '%04d-%02d-%02d'%(int(a.group(1)),int(a.group(2)),int(a.group(3)))

def reg_search(text,regex_list):
    ans=[]
    for d in regex_list:
        t={}
        for k,p in d.items():
            try:
                a=re.findall(p,text,re.I|re.S)
            except re.error:
                raise ValueError('正则表达式错误:'+p)
            if not a:continue
            b=[]
            for x in a:
                if isinstance(x,tuple):
                    x=x[0] if len(x)==1 else list(x)
                b.append(fmt(x))
            t[k]=b[0] if len(b)==1 else b
        ans.append(t)
    return ans

if __name__=='__main__':
    print('请输入待匹配文本，单独输入 END 结束：')
    a=[]
    while True:
        s=input()
        if s=='END':break
        a.append(s)
    text='\n'.join(a)
    n=int(input('请输入字段数量：'))
    d={}
    for i in range(n):
        k=input('请输入字段名：').strip()
        p=input('请输入正则：').strip()
        d[k]=p
    print(reg_search(text,[d]))
