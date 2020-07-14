import json
import re
from ..find_roles import find_roles
from ..find_laws import find_laws

def find_name_and_law(judgement,break_line='\r\n'):
    laws_list=find_laws(judgement,break_line=break_line)
    # print(laws_list)
    people_list=find_roles(judgement,break_line=break_line)
    text_list=judgement.split("。")
    name_and_law=[]
    for txt in text_list:
        for person in people_list:
            if person not in txt or person ==" ":
                continue
            else:
                for law in laws_list:
                    if law in txt:
                        if {"name":person,"law":law} not in name_and_law:
                            name_and_law.append({"name":person,"law":law})
    return name_and_law