import re
import json

def find_fact(judgement):
    return 0

# 讀取裁判(judgement)全文
def loadData():
    judgement = []
    with open('./law.json','r',encoding='utf-8') as f:
        for line in f.readlines():
            doc = json.loads(line)
            jud = doc['judgement']
            judgement.append(jud)
    return judgement

# 找不到事實的結尾，再比對看看
def fail2find(text, fact, rgl2_list):
    secondchance = ''
    secondchance = text[fact.start():]
    for each in rgl2_list:
        evidence = re.search(each ,secondchance)
        if evidence != None:
            break
    fs = secondchance[:evidence.start()]
    return fs

# 提取事實部分
def extract_fact(text, break_line='\r\n'):
    '''
    input: 整個判決書文本(judgement欄位)
    output:	從判決書全文擷取出"事實"的部分
    '''
    reg_break_line = break_line.replace('\r','\\\r')
    reg_break_line = reg_break_line.replace('\n','\\\n')

    rgs2 = '\\s{3}犯罪事實及理由|、犯罪事實|\\s{3}犯罪事實|犯罪事實：|理\\s*由'
    rgl2 = reg_break_line + '\\s*證\\s*據|。證據| 證據|、((前項|上揭)犯罪事實|證據)'
    rgl2_list = ['。證據',' 證據','、((前項|上揭)犯罪事實|證據)',reg_break_line +'\\s*證\\s*據','中\\s+華\\s+民\\s+國']
    rgs = '\\s(犯罪)?事\\s*實\\s*' + reg_break_line
    rgl = '\\s理\\s*由\\s*' + reg_break_line
    red = ['據上論.','中　　華　　民　　國','中\\s+華\\s+民\\s+國']
    fs = ''
    fact = re.search(rgs, text)
    reason = re.search(rgl, text)
    if fact == None:
        fact = re.search(rgs2, text)
    if reason == None:
        reason = re.search(rgl2, text)
    for each in red:
        if reason == None:
            reason = re.search(each, text)
    if reason!= None and fact!= None:
        fact_end = fact.end()
        reason_start = reason.start()
        try:
            if fact_end > reason_start:
                fs = fail2find(text, fact, rgl2_list)
            else:
                fs = text[fact.end():reason.start()]
        except:
            fs = ''
    else:
        fs = ''
    return fs

# 擷取事實第一段
def getFirstparagraph(first_fact, break_line='\r\n'):

    reg_break_line = break_line.replace('\r','\\\r')
    reg_break_line = reg_break_line.replace('\n','\\\n')

    start_list = '一、|壹、'
    stop_list =['二、', '貳、', reg_break_line+'二', '、證據']
    stop_length = 0

    first = re.search(start_list, first_fact)
    for each in stop_list:
        stop = re.search(each, first_fact)
        if stop != None:
            stop_length = len(each)
            break
    if first == None or stop == None:
        return first_fact
    else:    
        return first_fact[first.start():stop.end()-stop_length]

if __name__ == "__main__":

    data = loadData()

    # i = 13947
    # print(data[i])
    # print('============')
    # print(extract_fact(data[i]))
    # print('============')
    # print(getFirstparagraph(extract_fact(data[i])))

    fact_dict = {}
    for i, fact in enumerate(data):
        fact_dict.setdefault(i, extract_fact(fact))


    # # 輸出 txt 檔
    # for i in range(len(fact_dict)):
    #     # print(str(i) +': ' + fact_dict[i] + '\n')
    #     with open('./fact.txt','a',encoding='utf-8') as f:
    #         f.write(str(i) +': ' + fact_dict[i] + '\n')

    fact_firstparagraph = {}
    for index, (j, first_fact) in enumerate(fact_dict.items()):
        fact_firstparagraph.setdefault(index, getFirstparagraph(first_fact))

    # # 輸出 txt 檔
    # for i in range(len(fact_firstparagraph)):
    #     # print(str(i) +': ' + fact_firstparagraph[i] + '\n')
    #     with open('./fact_firstparagraph.txt','a',encoding='utf-8') as f:
    #         f.write(str(i) +': ' + fact_firstparagraph[i] + '\n')

    # 計算空值
    count = 0
    null_list = []
    for key, value in fact_firstparagraph.items():
        if value.strip() == '':
            null_list.append(key)
            count = count + 1

    print('沒抓到的：'+ str(null_list))
    print('沒抓到的篇數：' + str(count))

    short_count = 0
    short_list = []
    for key, value in fact_firstparagraph.items():
        if len(value) <= 50:
            short_count = short_count + 1
            short_list.append(key)
    
    # print('長度<50：'+ str(short_list))
    print('長度<50的篇數：' + str(short_count))