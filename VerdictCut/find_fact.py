import re
import json

def find_fact(judgement, break_line='\r\n'):
    fact = extract_fact(judgement, break_line= break_line)
    fact_dict = geteachParagraph(fact, break_line= break_line)
    return fact_dict

# 讀取裁判(judgement)全文
def loadData():
    judgement = []
    with open('./real_law/dump200.json','r',encoding='utf-8') as f:
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
def extract_fact(judgement, break_line='\r\n'):
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
    fact = re.search(rgs, judgement)
    reason = re.search(rgl, judgement)
    if fact == None:
        fact = re.search(rgs2, judgement)
    if reason == None:
        reason = re.search(rgl2, judgement)
    for each in red:
        if reason == None:
            reason = re.search(each, judgement)
    if reason!= None and fact!= None:
        fact_end = fact.end()
        reason_start = reason.start()
        try:
            if fact_end > reason_start:
                fs = fail2find(judgement, fact, rgl2_list)
            else:
                fs = judgement[fact.end():reason.start()]
        except:
            fs = ''
    else:
        fs = ''
    return fs

# 取得事實各段落
def geteachParagraph(fact, break_line='\r\n'):

    reg_break_line = break_line.replace('\r', '\\\r')
    reg_break_line = reg_break_line.replace('\n', '\\\n')

    paragraph_dict = { 
        1 : [ ('一、|壹、'), ('二、', '貳、', reg_break_line+'二') ],
        2 : [ ('二、|貳、'), ('三、', '參、', reg_break_line+'三') ],
        3 : [ ('三、|參、'), ('四、', '肆、', reg_break_line+'四') ],
        4 : [ ('四、|肆、'), ('五、', '伍、', reg_break_line+'五') ],
        5 : [ ('五、|伍、'), ('六、', '陸、', reg_break_line+'六') ],
        6 : [ ('六、|陸、'), ('七、', '柒、', reg_break_line+'七') ],
        7 : [ ('七、|柒、'), ('八、', '捌、', reg_break_line+'八') ],
        8 : [ ('八、|捌、'), ('九、', '玖、', reg_break_line+'九') ],
        9 : [ ('九、|玖、'), ('十、', '拾、', reg_break_line+'十') ],
        10: [ ('十、|拾、'), ('十一、', '拾壹、', reg_break_line+'十一') ]
        }

    fact_dict = {}
    fact_dict[0] = fact
    for i in paragraph_dict:

        start_list = paragraph_dict[i][0]
        stop_list = paragraph_dict[i][1]

        first = re.search(start_list, fact)
        for each in stop_list:
            stop = re.search(each, fact)
            if stop != None:
                stop_length = len(each)
                break
        if first == None:
            fact_dict[i] = fact
        elif stop == None:
            fact_dict[i] = fact[first.start():]
            break
        else:
            fact_dict[i] = fact[first.start():stop.end()-stop_length]
        # print(fact_dict[i])
    return fact_dict


if __name__ == "__main__":

    data = loadData()

    # i = 0
    # print(data[i])
    # print('============')
    # print(extract_fact(data[i]))
    # print('============')
    # print(geteachParagraph(extract_fact(data[i])))

    all_fact_dict = {}
    for i in range(len(data)):
        fact_dict = geteachParagraph(extract_fact(data[i]))
        all_fact_dict[i] = fact_dict

    # dump 事實每個段落
    # with open('./fact_dict200.json','w',encoding='utf-8') as f:
    #     json.dump(all_fact_dict, f, ensure_ascii=False)


    # 輸出 txt 檔
    # for i in range(len(all_fact_dict)):
    #     for j in range(len(all_fact_dict[i])):
    #         with open('./fact_dict200.txt', 'a', encoding='utf-8') as f:
    #             f.write(str(i) +': ' + '\n' + str(j) + ': ' + all_fact_dict[i][j])


    # 計算空值
    # count = 0
    # null_list = []
    # for key, value in all_fact_dict.items():
    #     if len(value) >= 10:
    #         null_list.append(key)
    #         count = count + 1

    # # print('沒抓到的：'+ str(null_list))
    # print('沒抓到的篇數：' + str(count))