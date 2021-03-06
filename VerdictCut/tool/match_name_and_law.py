import json
import re
import cn2an
from ..find_roles import find_roles
from ..find_laws import find_laws
from ..find_laws import get_all_laws_list
from ..find_justice import find_justice


def match_name_and_law(judgement, name_list, break_line='\r\n'):
    # 找附錄法條
    appendix_laws_list = find_laws(judgement, break_line)
    appendix_laws_list = add_ROC(appendix_laws_list)
    # 找論罪科刑
    justice = clean_text(find_justice(judgement), break_line)

    # 找被告
    people_dict = find_roles(judgement, target_roles=[
                             '被告'], break_line=break_line)
    # name_list = find_name(people_dict)
    # 找執掌法條
    all_laws_list = get_all_laws_list()
    # 從論罪科刑裡面找法條
    text_list = justice.split("。")

    name_and_law = {}
    # init object for each person
    for name in name_list:
        name_and_law[name] = []

    for name in name_list:
        for text in text_list:
            if name in text:
                for law in all_laws_list:
                    # 若有找到法條  把那些第幾項第幾條第幾款都列出來
                    if re.search(law, text) != None:
                        SPA_list = find_SPA(law, text)
                        SPA_list = add_ROC(SPA_list)
                        SPA_list = trans_tai_to_TAI(SPA_list)
                        name_and_law[name].extend(SPA_list)
        # 去除重複
        name_and_law[name] = list(set(name_and_law[name]))

    # 如果只有一個被告跟附錄法條有找到，或者沒抓到論罪科刑
    if (len(name_list) == 1 ) or check_name_and_law(name_list, name_and_law) == False:
        if len(name_list) == 1:
            # 如果只有一個被告 則回傳附錄法條即可
            name_and_law[name] = appendix_laws_list
        else:
            # 兩個被告都犯一樣的罪，導致論罪科刑沒有特別提被告們的名字
            for name in name_list:
                name_and_law[name] = appendix_laws_list
        return name_and_law
    elif check_name_and_law(name_list, name_and_law) and len(appendix_laws_list) == 0:
        return name_and_law

    for name, laws_list in name_and_law.items():
        # 複製
        laws_list_copy = laws_list.copy()
        for law in laws_list:
            # 若在論罪科刑找到的法條沒在附錄法條
            if law not in appendix_laws_list:
                # 去掉款是否有在附錄法條
                del_subpara_law = backspace_SP('第\d*款', law)
                if del_subpara_law not in appendix_laws_list:
                    # 去掉項是否有在附錄法條
                    del_para_law = backspace_SP('第\d*項', law)
                    if del_para_law not in appendix_laws_list:
                        # 換另一種方法找
                        k = 0
                        for appendix_law in appendix_laws_list:
                            # 對每個附錄法條都檢查是否含有剩下條的法
                            if re.search(del_para_law, appendix_law) == None:
                                k += 1
                        # 還是沒有的話就刪除該法條
                        if k == len(appendix_laws_list):
                            laws_list_copy.remove(law)
        name_and_law[name] = laws_list_copy
    return name_and_law


def find_name(people_dict):
    name_list = []
    for index in range(len(people_dict)):
        name_list.append(people_dict[index]["name"])
    return name_list


def find_all_laws_position_from_text(all_laws_list, judgement):
    all_laws_position = {}
    for law in all_laws_list:
        if re.search(law, judgement) != None:
            all_laws_position[law]
    return all_laws_position


# 資料清洗
def clean_text(judgement, break_line='\r\n'):
    # 去空白  去換行符號
    clean_text = re.sub(break_line, "", re.sub(r"\s+", "", judgement))
    return clean_text


def find_SPA(law, text):
    # 先轉把中文數字轉成阿拉伯數字
    # try:
    #     text = cn2an.transform(text,'cn2an')
    # except:
    #     print(text)

    SPA_list = []

    regex_SPA = "第\d*條第\d*項第\d*款"
    regex_PA = "第\d*條第\d*項"
    regex_A = "第\d*條"
    # regex_article = "第.*條"
    # regex_paragraph = "第.*項"
    # regex_subparagraph = "第.*款"
    SPA_list = re.findall(regex_SPA, text)
    PA_list = re.findall(regex_PA, text)
    A_list = re.findall(regex_A, text)

    SPA_list.extend(set(SPA_list))
    SPA_list.extend(set(PA_list))
    SPA_list.extend(set(A_list))
    # if len(SPA_list)==0:

    SPA_list_copy = SPA_list.copy()
    # 保留含有細項的法條
    for SPA_c in SPA_list_copy:
        for SPA in SPA_list:
            if SPA_c == SPA:
                continue
            else:
                if SPA in SPA_c and len(SPA_c) > len(SPA):
                    SPA_list.remove(SPA)
    #　加上法條名稱
    for i in range(len(SPA_list)):
        SPA_list[i] = law+SPA_list[i]
    return SPA_list


def backspace_SP(regex_str, law):
    regex_position = re.search(regex_str, law)
    if regex_position == None:
        return law
    else:
        return law[:regex_position.start()]


def translate(appendix_laws_list, SPA_list):
    # 把論罪科刑找到法條的 "刑法" 寫成 "中華民國刑法"
    # 在 附錄法條是寫成中華民國刑法的條件下
    bool_translate = False
    for appendix_law in appendix_laws_list:
        if re.search('中華民國刑法', appendix_law) != None:
            bool_translate = True
            break
    if bool_translate:
        for i in range(len(SPA_list)):
            if re.search('刑法', SPA_list[i]) != None and re.search('中華民國刑法', SPA_list[i]) == None:
                SPA_list[i] = '中華民國'+SPA_list[i]

    return SPA_list


def check_name_and_law(name_list, name_and_law):
    # 檢查是否有抓到論罪科刑的法條
    bool_value = False
    for name in name_list:
        if len(name_and_law[name]) != 0:
            bool_value = True
            return bool_value
    return bool_value


def add_ROC(law_list):
    # 只要只有寫到刑法第幾條 刑法前面無字元  前面全部加上中華民國
    for i in range(len(law_list)):
        if re.search("^刑法", law_list[i]) != None:
            law_list[i] = "中華民國"+law_list[i]
    return law_list

def trans_tai_to_TAI(law_list):
    # 把台都轉成臺
    for i in range(len(law_list)):
        if "台" in law_list[i]:
            law_list[i]=str(law_list[i]).replace("台","臺")
    
    return law_list
            
