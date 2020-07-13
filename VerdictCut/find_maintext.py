# -*-coding:UTF-8 -*-
import json
import re

def find_maintext(judgement, break_line='\r\n'):
    main_text = extract_main_text(judgement, break_line)
    return main_text

# 提取主文
def extract_main_text(text, break_line='\r\n'):
    # input: 整個判決書文本(judgement欄位)
    # output:	從判決書全文擷取出"主文"的部分

    # 要找主文和事實的條件
    reg_break_line = break_line.replace('\r','\\\r')
    reg_break_line = reg_break_line.replace('\n','\\\n')

    rgs1 = "\\s主\\s*文\\s*" + reg_break_line + "|\\s本\\s*文\\s*" + reg_break_line + "|\\s*主\\s*文\\s*"
    rgs12 = "、主文|\\s{3}主文|主文：|、主\\s*文|主\\s*文："
    rgs2 = reg_break_line + "\\s*事\\s*實\\s*及\\s*理\\s*由|" + reg_break_line + "\\s*事\\s*實\\s*及\\s*裡\\s*由|\\s(犯罪)?事\\s*實\\s*" + reg_break_line + "|、犯罪事實|\\s{3}犯罪事實|犯罪事實：|理\\s*由"
    # 找尋主文的位置
    main = re.search(rgs1, text)
    fact = ""
    if main == None:
        main = re.search(rgs12, text)

    if main != None:
        # 找尋事實的位置
        main_berfore = text[:main.end()]    # 抓取主文前面的字串
        main_after = text[main.end():]      # 抓取主文後面的字串
        while(1):
            fact = re.search(rgs2, main_after)  # 從主文之後的位置來提取事實的位置
            if fact != None:
                if main_after[fact.start()-1: fact.start()] == "當":        # 無正當理由
                    main_berfore = main_berfore + main_after[:fact.start()+2]
                    main_after = main_after[fact.start()+2:]
                else:
                    break
            else:
                break

    # 藉由主文和事實的位置來提取主文
    if main!= None and fact!= None:
        # 如果主文的結束位置大於事實的開始位置，代表抓錯了
        if main.end() > (fact.start() + len(main_berfore)):
            print("失敗:" + "-----")
            print(text)
            print(main)
            print(fact)

            return ""
        else:
            main_text = text[main.end():(fact.start()+len(main_berfore))]       # 提取主文
            main_text = dealwith_useless_character(main_text)                       # 處理無關於主文的字元
            # print(main_berfore)
            # print(main)
            # print(fact)

            return main_text
    else:
        print("失敗:" + "-----")
        print(text)
        print(main)
        print(fact)

        return ""

# 處理無關於主文的字元
def dealwith_useless_character(text, break_line='\r\n'):
    if text[0:1] == "：":
        text = text[1:]

    
    if text.rfind("。") != (len(text)-1):
        start = text.rfind("。" + break_line)
        if start != -1:
            # 避免選到中間的"。\r\n"
            if (len(text) - start) < 20:
                text = text[:start+1]
                return text

    return text

# 移除主文中的無用字元
def remove_character(data):
    data = data.replace(" ", "")
    data = data.replace("　", "")
    data = data.replace("\r", "")
    data = data.replace("\n", "")

    return data

def load_data():
    docs = []
    with open('./law.json','r', encoding='utf-8') as f:
        for line in f.readlines():
            doc = json.loads(line)
            docs.append(doc)

    return docs
    
# 將字典存檔，字典快速保存與讀取，參考網站:https://blog.csdn.net/u012155582/article/details/78077180
def save_json(filepath, dict):
    f = open(filepath, 'w', encoding='UTF-8')
    json.dump(dict, f, ensure_ascii=False)
    f.close()

if __name__ == "__main__":
    all_data = load_data()      # 載入Law.Verdict_2019_200_0702.json
    count = 0
    main_text_dict = {}         

    for data in all_data:
        count = count + 1
        main_text = extract_main_text(data["judgement"])     # 提取主文
        main_text_dict[str(count)] = {}
        main_text_dict[str(count)]["主文"] = main_text
        main_text_dict[str(count)]["judgement"] = remove_character(data["judgement"])

    print("共" + str(count) + "筆")
    save_json("main_text_dict.json", main_text_dict)        # 將字典存檔
