# coding=UTF-8
import json
import re

def find_laws(judgement):
    print()
    return 0

def extract_law_text(text):
    appendix_law_list = ['附本件論罪科刑依據之法條', '附錄本案論罪科刑法條', '附錄本案所犯法條', '附錄本判決論罪科刑法條', '附錄：本案論罪科刑法條', '附錄法條', '附錄論罪科刑法條', '附錄：論罪科刑法條', '本件論罪科刑法條', '本案論罪科刑法條', '附錄所犯法條', '附錄本判決論罪之法條', '附錄本案論罪法條', '附錄本判決論罪科刑之法條', '附錄本案論罪科刑依據之法條', '所犯法條', '附錄本罪論罪科刑法條', '附錄本判決論罪', '附錄本案論罪', '附錄本件判決論罪', '附錄論罪', '論罪科刑法條', '附錄本判決所引法條', '附記論罪之法條', '論罪法條', '論罪之法條', '附錄本件論罪科刑', '附論罪科刑依據之法條', '附錄本案處罰實體法條', '附錄：本判決論罪科刑', '附錄犯罪科刑', '附錄本案法條', '附錄條文', '處罰條文：', '附錄：本案論罪科刑', '本案論罪科刑主要法條', '論罪科刑依據法條', '科刑法條之依據', '參考法條：', '附錄']
    tabled_list=["附表"]
    start=0
    end=0
    fs=""
    for law in (appendix_law_list):
        if re.search(law, text) == None:
            continue
        law_text_position = re.search(law, text)
        start=law_text_position.end()
        count=len(re.findall(law,text))
        fs=text
        while count >0:
            fs=fs[start:]
            next_law_text_position = re.search(law, fs)
            if next_law_text_position==None:
                break
            start=next_law_text_position.end()
            count-=1
        if start !=0:
            break
    for table in tabled_list:
        law_text_position=re.search(table, fs)
        if law_text_position!=None:
            end=law_text_position.start()
            fs=fs[:end]
            break
    if (start==0):
        return ""
    elif(start !=0 and end!=0):
        return fs
    # 沒有找到附表
    elif(start !=0 and end ==0):
        return fs
    else:
        return text[start:]

if __name__ == "__main__":
    docs = []
    with open('./law.json','r',encoding='utf-8') as f:
        for line in f.readlines():
            doc = json.loads(line)      
            docs.append(doc)

    law_text={}

    for i,doc in enumerate(docs):
        text=doc["judgement"]
        fs = extract_law_text(text)
        law_text[i]=fs