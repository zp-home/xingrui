import unittest
from main import reg_search

class TestRegSearch(unittest.TestCase):
    def test_example(self):
        text='''标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。'''
        a=[{'标的证券':r'股票代码\s*[：:]\s*(\d{6}\.(?:SH|SZ|BJ))',
            '换股期限':r'(?:即|至)\s*((?:\d{4})\s*年\s*(?:\d{1,2})\s*月\s*(?:\d{1,2})\s*日)'}]
        b=[{'标的证券':'600900.SH','换股期限':['2023-06-02','2027-06-01']}]
        self.assertEqual(reg_search(text,a),b)

    def test_regex(self):
        text='编号:A-12，编号:B-35'
        a=[{'编号':r'编号[：:]([A-Z]-\d+)'}]
        b=[{'编号':['A-12','B-35']}]
        self.assertEqual(reg_search(text,a),b)

    def test_no_match(self):
        self.assertEqual(reg_search('没有结果',[{'编号':r'编号[：:]([A-Z]-\d+)'}]),[{}])

if __name__=='__main__':
    unittest.main(verbosity=2)
