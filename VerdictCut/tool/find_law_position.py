import re
from .find_job_location_position import regularize
from ..find_justice import find_justice

def find_law_position(judgement,law_list, break_line='\r\n'):
    laws_position_dict_list=[]
    for law in law_list:
        laws_position_dict={}
        regex_law=regularize(law)
        law_position=re.search(regex_law,judgement)
        if law_position!=None:
            laws_position_dict["law"]=law
            laws_position_dict["start"]=law_position.start()
            laws_position_dict["end"]=law_position.end()
        else:
            laws_position_dict["law"]=law
            laws_position_dict["start"]=-1
            laws_position_dict["end"]=-1
        laws_position_dict_list.append(laws_position_dict.copy())
    return laws_position_dict_list


if __name__ == "__main__":
    f = open(
        "/root/project/law_data/test1.txt", 'r', newline="", encoding='utf-8')
    judgement = f.read()
    law_list=[]
    kk=find_law_position(judgement,law_list)
