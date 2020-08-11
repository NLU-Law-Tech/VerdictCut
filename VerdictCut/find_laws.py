# coding=UTF-8
import json
import re


# 找附錄法條
def find_laws(judgement, break_line='\r\n'):
    appendix_law_list = get_appendix_law_list()
    table_list = get_table_list()
    all_laws_list = get_all_laws_list()
    law_paragraph = extract_law_paragraph(
        judgement, appendix_law_list, table_list)
    law_paragraph_list = law_paragraph.split(break_line)
    laws_list = []
    for data_text in (law_paragraph_list):
        for law in all_laws_list:
            if law in data_text:
                # print(key,regex_law(law,data_text))
                processed_law = clean_data(
                    regex_law(law, data_text), break_line)
                if processed_law in laws_list:
                    continue
                else:
                    laws_list.append(processed_law)
    # 如果中華民國刑法已經找到,就刪除刑法的部分
    # 保留含有細項的法條
    laws_list_copy = laws_list.copy()
    for law_c in laws_list_copy:
        for law in laws_list:
            if law_c == law:
                continue
            else:
                if law in law_c and len(law_c) > len(law):
                    laws_list.remove(law)
    return laws_list


def regex_law(law, text):
    # 先找"款"  找到就把款後面的字去掉
    regx_text = "條例"
    result = ""
    if regx_text in law:
        law_posistion = re.search(regx_text, text)
        # 開頭
        # temp_opening=text[:law_posistion.end()]
        # 以執掌法條當開頭
        temp_opening = law
        # 結尾
        temp_text = text[law_posistion.end():]
        result = extract_SPA(temp_text)
        return temp_opening+result
    else:
        # 先去掉款項條後面的文字或符號
        temp_text = extract_SPA(text)
        # 以執掌法條當開頭
        law_posistion = re.search(law, text)
        result = temp_text[law_posistion.start():]
        return result


def extract_SPA(text):
    rgs_list = ["款", "項", "條"]
    end = 0
    for rgs in rgs_list:
        position = re.search(rgs, text)
        if position != None:
            end = position.start()
            break
    if end != 0:
        return text[:end+1]
    else:
        return text
# 取出附錄法條的段落


def extract_law_paragraph(text, appendix_law_list, table_list):
   # 初始化起始跟結束位置
    start = 0
    end = 0
    # 初始化result
    result = ""
    # 初始化存放附錄法條字的位置字典
    appendix_law_position_dict = {}
    key = ""
    # 找到含有"附錄法條"的位置，可能會找到不只一個位置
    for appendix_law in appendix_law_list:
        # 有找到才做下去
        law_text_position = re.search(appendix_law, text)
        if law_text_position != None:
            # 因為要找附錄法條的尾
            # 有找到就跳
            start = law_text_position.end()
            break
    # 再找附表的位置
    for table in table_list:
        for law_text_position in re.finditer(table, text):
            if law_text_position.start() > start:
                end = law_text_position.start()
                break
        if end != 0:
            break
    # 假設都有找到
    if (start < end):
        if (start != 0) and (end != 0):
            result = text[start:end]
        elif (start != 0) and (end == 0):
            result = text[start:]
        else:
            result = ""
        # 如果連start 都是 0  就不用找了
    else:
        if start == 0:
            result = ""
        else:
            result = text[start:]
    return result


def get_appendix_law_list():
    appendix_law_list = ["\s*附\s*錄\s*本\s*案\s*論\s*罪\s*科\s*刑\s*依\s*據\s*之\s*法\s*條",
                         "\s*附\s*錄\s*本\s*件\s*判\s*決\s*論\s*罪\s*科\s*刑\s*法\s*條\s*：",
                         "\s*附\s*本\s*件\s*論\s*罪\s*科\s*刑\s*依\s*據\s*之\s*法\s*條",
                         "\s*附\s*錄\s*本\s*判\s*決\s*論\s*罪\s*科\s*刑\s*之\s*法\s*條",
                         "\s*附\s*錄\s*本\s*案\s*論\s*罪\s*科\s*刑\s*之\s*法\s*條\s*：",
                         "\s*附\s*錄\s*：\s*本\s*案\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*本\s*判\s*決\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*本\s*罪\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*本\s*判\s*決\s*論\s*罪\s*之\s*法\s*條",
                         "\s*附\s*錄\s*本\s*案\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*論\s*罪\s*科\s*刑\s*依\s*據\s*之\s*法\s*條",
                         "\s*附\s*錄\s*本\s*案\s*處\s*罰\s*實\s*體\s*法\s*條",
                         "\s*附\s*錄\s*：\s*本\s*判\s*決\s*論\s*罪\s*科\s*刑",
                         "\s*本\s*案\s*論\s*罪\s*科\s*刑\s*主\s*要\s*法\s*條",
                         "\s*附\s*錄\s*：\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*本\s*判\s*決\s*所\s*引\s*法\s*條",
                         "\s*附\s*錄\s*：\s*本\s*案\s*論\s*罪\s*科\s*刑",
                         "\s*附\s*錄\s*本\s*案\s*所\s*犯\s*法\s*條",
                         "\s*附\s*錄\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*本\s*件\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*本\s*案\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*本\s*案\s*論\s*罪\s*法\s*條",
                         "\s*附\s*錄\s*本\s*件\s*判\s*決\s*論\s*罪",
                         "\s*附\s*錄\s*本\s*件\s*論\s*罪\s*科\s*刑",
                         "\s*論\s*罪\s*科\s*刑\s*依\s*據\s*法\s*條",
                         "\s*附\s*錄\s*本\s*判\s*決\s*論\s*罪",
                         "\s*附\s*記\s*論\s*罪\s*之\s*法\s*條",
                         "\s*科\s*刑\s*法\s*條\s*之\s*依\s*據",
                         "\s*附\s*錄\s*所\s*犯\s*法\s*條",
                         "\s*附\s*錄\s*本\s*案\s*論\s*罪",
                         "\s*論\s*罪\s*科\s*刑\s*法\s*條",
                         "\s*附\s*錄\s*犯\s*罪\s*科\s*刑",
                         "\s*附\s*錄\s*本\s*案\s*法\s*條",
                         "\s*論\s*罪\s*之\s*法\s*條",
                         "\s*參\s*考\s*法\s*條\s*：",
                         "\s*處\s*罰\s*條\s*文\s*：",
                         "\s*所\s*犯\s*法\s*條",
                         "\s*附\s*錄\s*法\s*條",
                         "\s*附\s*錄\s*論\s*罪",
                         "\s*論\s*罪\s*法\s*條",
                         "\s*附\s*錄\s*條\s*文",
                         "\s*附\s*錄\s*法\s*條",
                         "\s*附\s*錄\s*:",
                         "\s*附\s*錄"
                         ]

    return appendix_law_list


def get_table_list():
    # 讀取附表資料
    table_list = ["\s*附\s*表", "\s*附\s*件"]
    return table_list


def get_all_laws_list():
    # 取得法條的名稱
    all_laws_list = ['中華民國刑法', '陸海空軍刑法', '國家機密保護法', '國家情報工作法',
                     '國家安全法', '洗錢防制法', '臺灣地區與大陸地區人民關係條例', '貿易法',
                     '組織犯罪防制條例', '人口販運防制法', '社會秩序維護法', '戰略性高科技貨品輸出入管理辦法',
                     '山坡地保育利用條例', '公司法', '公民投票法', '公職人員選舉罷免法',
                     '水土保持法', '水污染防治法', '水利法', '兒童及少年性交易防制條例',
                     '空氣污染防制法', '金融控股公司法', '律師法', '政府採購法', '毒品危害防制條例',
                     '區域計畫法', '國有財產法', '票券金融管理法', '貪污治罪條例',
                     '都市計畫法', '期貨交易法', '森林法', '稅捐稽徵法', '農田水利會組織通則',
                     '農會法', '農業金融法', '槍砲彈藥刀械管制條例', '漁會法', '銀行法',
                     '廢棄物清理法', '總統副總統選舉罷免法', '懲治走私條例', '藥事法', '證券交易法',
                     '資恐防制法', '畜牧法', '破產法', '商標法', '商業登記法', '光碟管理條例',
                     '個人資料保護法', '健康食品管理法', '妨害國幣懲治條例', '通訊保障及監察法',
                     '化粧品衛生管理條例', '金融資產證券化條例', '食品安全衛生管理法',
                     '動物傳染病防治條例', '多層次傳銷管理法', '商業會計法', '信託業法',
                     '電信法', '動物用藥品管理法', '消費者債務清理條例', '專利師法',
                     '傳染病防治法', '嚴重特殊傳染性肺炎防治及紓困振興特別條例',
                     '農藥管理法', '飼料管理法', '管理外匯條例', '野生動物保育法',
                     '植物防疫檢疫法', '遺產及贈與稅法', '電子支付機構管理條例',
                     '電子票證發行管理條例', '營業秘密法', '信用合作社法', '菸酒管理法',
                     '保險法', '證券投資信託及顧問法', '證券投資人及期貨交易人保護法', '刑法']
    return all_laws_list

# 資料清洗


def clean_data(dirty_law, break_line):
    # 先去空白 再去\r\n
    clean_law = re.sub(break_line, "", re.sub(r"\s+", "", dirty_law))
    return clean_law


#測試用#
if __name__ == "__main__":
    docs = []
    with open('C:/Yao/ITRI/Work/Project/law_judge/data/dump200.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            doc = json.loads(line)
            docs.append(doc)
    break_line = '\r\n'
    law_paragraph_dict = {}
    appendix_law_list = get_appendix_law_list()
    table_list = get_table_list()
    all_laws_list = get_all_laws_list()
    # law_list=find_laws(judgement)
    dicct = {}
    for key in range(len(docs)):
        judgement = docs[key]["judgement"]
        law_list = find_laws(judgement)
        dicct[key] = law_list
    with open("C:/Yao/ITRI/Work/Project/law_judge/law_list_file/law_list_19605.txt", 'w', encoding='utf-8') as f:
        json.dump(dicct, f, ensure_ascii=False)
