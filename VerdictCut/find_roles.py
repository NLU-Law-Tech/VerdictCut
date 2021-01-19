import json
import re


def find_roles(cj_doc, target_roles=['上訴人', '被告', '選任辯護人'],
               break_line='\r\n', name_length_limit=25, search_rows_limit=100):
    """
    找判決書的人跟此人在判決書中之角色
    cj_doc:str 整篇判決書或部分內容 
    target_roles: 找尋目標角色
    name_length_limit:int 限制找到的名稱長度
    search_rows_limit:int 要搜尋cj_doc的前x列
    """
    _target_roles = ['上訴人', '被告', '選任辯護人']  # do not change this
    role_clean_patterns = ["^即(　| )", " ", "律師$", "（.*）", "\(.*\)"]
    cj_doc_rows = cj_doc.split(break_line)[:search_rows_limit]

    people = []
    encode_reg_role_clean_chars = "|".join(role_clean_patterns)
    last_role_flag = 'undefine'
    last_index = 1
    have_defendant = False
    for index, cj_doc_row in enumerate(cj_doc_rows):
        #有些時候被告前面會有空白，導致解析錯誤
        if re.search(r"被\s*告|上\s*訴\s*人", cj_doc_row):
            cj_doc_row = cj_doc_row.strip()
        #判斷這篇有沒有出現被告，如果沒有則返回特殊訊息
        if re.search(r"被\s*告", cj_doc_row):
            have_defendant = True
        cj_doc_row = re.sub(encode_reg_role_clean_chars, "", cj_doc_row)
        # 找到主文就可以結束了
        if cj_doc_row == "主文":
            break
        cj_doc_row_keep_full_space = cj_doc_row
        cj_doc_row = cj_doc_row.replace("　", "")
        for role in _target_roles:
            encode_reg_roles = r"^"+role
            if(re.match(encode_reg_roles, cj_doc_row)):
                target_name = cj_doc_row.replace(role, "")
                if len(target_name) > name_length_limit or len(target_name) == 0:
                    continue

                # print(role,target_name)
                people.append({"name": target_name, "role": role})
                last_role_flag = role

                last_index = index + 1
                break
            elif(re.match(r"^　+.+$", cj_doc_row_keep_full_space)):
                _role = last_role_flag
                # 濾掉被告雜訊
                if cj_doc_row_keep_full_space[6:7]=="　":
                    break
                target_name = cj_doc_row_keep_full_space.replace("　", "")
                if(last_role_flag != 'undefine'):
                    # print(role,target_name)
                    if len(target_name) > name_length_limit or len(target_name) == 0:
                        continue
                    people.append({"name": target_name, "role": _role})

                last_index = index + 1

                break
    # 過濾，只留要的
    if not have_defendant:
        return "No defendant"

    for person in people[:]:
        if person['role'] not in target_roles:
            people.remove(person)

    return people
