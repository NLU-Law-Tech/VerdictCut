import re
import json

def find_justice(judgement):

    justice = extract_justice(judgement, break_line = '\r\n')    
    return justice

# 讀取裁判(judgement)全文
def loadData():
    judgement = []
    # with open('./law.json','r',encoding='utf-8') as f:
    with open('./real_law/dump20000.json','r',encoding='utf-8') as f:   
        for line in f.readlines():
            doc = json.loads(line)
            jud = doc['judgement']
            judgement.append(jud)
    return judgement

# 只找論罪科刑的部分
def test(judgement):
    fs = ''
    start_list = '論罪科刑'
    end_list = ['中　　華　　民　　國', '中\\s+華\\s+民\\s+國', '據上論斷']
    justice = re.search(start_list, judgement)
    for each in end_list:
        inference = re.search(each,judgement)
        if inference != None:
            break
    if justice != None and inference != None:
        # print(justice.end())
        # print(inference.start())
        fs = judgement[justice.start()-2:inference.start()-2]
    else:
        fs = ''
    return fs

def fail2find(judgement, justice, end_list):
    secondchance = ''
    secondchance = judgement[justice.start():]
    for each in end_list:
        realend = re.search(each ,secondchance)
        if realend != None:
            break
    fs = secondchance[:realend.start()]
    return fs

# 提取疑似論罪科刑的部分
def extract_justice(judgement, break_line = '\r\n'):

    reg_break_line = break_line.replace('\r','\\\r')
    reg_break_line = reg_break_line.replace('\n','\\\n')

    fs = ''
    jfs = '、(論罪科刑|論罪部分)'
    start_list = ['(核被告|是核其)(所為)?', '、查被告行為', '(\\^偵)(經)?查(被告|：|\\w)?', '、(爰|依|按|本院查)']
    end_list = ['據上論(斷)?', '中\\s+華\\s+民\\s+國']

    justice = re.search(jfs, judgement)
    justice_length = len(jfs)
    if justice == None:
        for each in start_list:
            justice = re.search(each, judgement)
            if justice != None:
                justice_length = len(each)
                break

    for each in end_list:
        inference = re.search(each,judgement)
        if inference != None:
            inference_length = len(each)
            break

    if justice != None and inference != None:
        justice_end = justice.end()
        inference_start = inference.start()
        try:
            if justice_end > inference_start:
                fs = fail2find(judgement, justice, end_list)
            else:
                fs = judgement[justice.end()-justice_length:inference.end()-inference_length]
        except :
            fs = ''
    else:
        fs = ''
    return fs

if __name__ == "__main__":

    data = loadData()

    # i = 0
    # print(data[i]+'\n')
    # print('---------只用論罪科刑去找---------\n')
    # print(test(data[i]))
    # print('---------用類似論罪科刑的寫法去找---------\n')
    # print(extract_justice(data[i]))

    justice_dict = {}
    for i, justice in enumerate(data):
        justice_dict.setdefault(i, extract_justice(justice))

    # 計算空值
    # count = 0
    # null_list = []
    # for key, value in justice_dict.items():
    #     if value == '':
    #         null_list.append(key)
    #         count = count + 1
    # print('沒抓到的：'+ str(null_list))
    # print('沒抓到的篇數：' + str(count))