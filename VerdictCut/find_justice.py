# 找判決書論罪科刑的部分
import re
import json

# 讀取裁判(judgement)全文
def loadData():
    judgement = []
    with open('./law.json','r',encoding='utf-8') as f:    
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
def extract_justice(judgement):

    fs = ''
    start_list = ['、論罪科刑', '論罪部分', '、查被告行為', '核被告所為', '是核其所為', '核被告','據上論斷', '、依']
    end_list = ['中　　華　　民　　國', '中\\s+華\\s+民\\s+國', '據上論斷']

    for each in start_list:
        justice = re.search(each, judgement)
        if justice != None:
            break

    for each in end_list:
        inference = re.search(each,judgement)
        if inference != None:
            break

    if justice != None and inference != None:
        try:
            if justice.end() > inference.start():
                fs = fail2find(judgement, justice, end_list)
            else:
                fs = judgement[justice.start()-2:inference.start()-2]
        except :
            fs = ''
    else:
        fs = ''
    return fs

if __name__ == "__main__":
    data = loadData()
    justice_dict = {}
    for i, justice in enumerate(data):
        justice_dict.setdefault(i, extract_justice(justice))

   