import re
import sys

s='{通配符}你好，今天开学了{通配符},你好'
print("s", s)
a1 = re.compile(r'\{.*?\}' )
d = a1.sub('',s)
print("d",d)
a1 = re.compile(r'\{[^}]*\}' )
d = a1.sub('',s)
print("d",d)


li = """<li><a href="/company/detail/tjbaojian.html" target="_blank">天津市宝之健纳米科技发展有限公司</a> <span class="green">www.85781.com/company/detail/tjbaojian.html</span><br />【联系电话】18626971450 【地址】天津市河东区新兆路东站后广场<br /><i class='gray'>宝之健纳米科技企业正以先进的市场经营理念及营销模式，现代化的企业运行机制，迈向以健康用品为核心的健康新领域。我们的理念是尽量了解人们内在的要求，用的最好的材料.....</i><br/><script type='text/javascript'>dispalyad();</script></li>
<li><a href="/company/detail/tjhytd.html" target="_blank">天津市华悦桐达包装机械有限公司</a> <span class="green">www.tjhypack.com</span><br />【联系电话】022-86888059 【地址】天津市北辰区京福公路东侧优谷科技园82-1<br /><i class='gray'>天津市华悦桐达包装机械有限公司成立十余年来一直专业从事全自动包装设备的研发与生产，产品在国内市场占有相当份额并远销国际市场。我DXD系列全自动包装机组占有率在98％.....</i></li>
"""

telAtt = li.split("<br />")[1]
print()
print(telAtt[telAtt.rindex("】")+1:])
print(telAtt[telAtt.index("】")+1:telAtt.rindex("【")])



A1 = "aaa"
A2 = "bbb"
A3 = "ccc"

CONSTANT = 10
Frequency = 0
KeysNum = 0;

def GetKeys():
    keys = ["aaa","bbb","ccc"];
    global KeysMax
    global CONSTANT
    global KeysNum
    global Frequency

    KeysMax= len(keys)
    
    if Frequency < CONSTANT:
        key = keys[KeysNum]
        Frequency += 1
        return key
    else:
        if KeysNum < KeysMax:
            KeysNum += 1
            key = keys[KeysNum]
            Frequency = 1
            return key
        else:
            return None;


for i in range(15):
    print(GetKeys())
    
    
