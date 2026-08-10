import re

rules={
    '标的证券':r'股票代码\s*[：:]\s*(\d{6}\.(?:SH|SZ|BJ))',
    '换股期限':r'换股期限[：:].*?即\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日.*?至\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'
}

def cv(x):
    if not isinstance(x,tuple):return x
    if len(x)%3:return list(x)
    ans=[]
    for i in range(0,len(x),3):
        y,m,d=x[i:i+3]
        if len(y)!=4 or not y.isdigit() or not m.isdigit() or not d.isdigit():
            return list(x)
        ans.append('%04d-%02d-%02d'%(int(y),int(m),int(d)))
    return ans[0] if len(ans)==1 else ans

def reg_search(text,regex_list):
    ans=[]
    for x in regex_list:
        t={}
        for k,p in x.items():
            if p=='*自定义*':p=rules.get(k)
            if not p:continue
            a=re.findall(p,text,re.I|re.S)
            if not a:continue
            a=[cv(i) for i in a]
            t[k]=a[0] if len(a)==1 else a
        ans.append(t)
    return ans

if __name__=='__main__':
    text = '''标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
    有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
    换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
    之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
    日至 2027 年 6 月 1 日止。'''
    regex_list = [{'标的证券': '*自定义*', '换股期限': '*自定义*'}]
    print(reg_search(text,regex_list))
