import re

def find_job_location_position(judgement,job_list,location_list, break_line='\r\n'):
    all_data_dict={}
    clean_judgement = re.sub(break_line, "", re.sub(r"\s+", "", judgement))
    judgement_list=re.split("，|。",clean_judgement)
    # 先找有matched的
    matched_location_list=[]
    matched_job_list=[]
    unmatched_location_list=location_list.copy()
    unmatched_job_list=job_list.copy()
    tuple_list=[]
    for paragraph in judgement_list:
        for job in job_list:
            for location in location_list:
                if location in paragraph and job in paragraph:
                    if (location,job) not in tuple_list:
                        tuple_list.append((location,job))
                        matched_location_list.append(location)
                        matched_job_list.append(job)       
                    if location in unmatched_location_list:
                        unmatched_location_list.remove(location)
                    if job in unmatched_job_list:
                        unmatched_job_list.remove(job)
    # 長度要一樣
    assert len(matched_location_list)==len(matched_job_list)

    all_matched_location_list=find_position_dict("location",matched_location_list,judgement)
    all_matched_job_list=find_position_dict("job",matched_job_list,judgement)
    all_matched_pair_list=[]
    for i in range(len(all_matched_location_list)):
        matched_pair_list=[]
        matched_pair_list.append(all_matched_location_list[i])
        matched_pair_list.append(all_matched_job_list[i])
        all_matched_pair_list.append(matched_pair_list.copy())
    all_data_dict["matched"]=all_matched_pair_list

    all_unmatched_location_list=find_position_dict("location",unmatched_location_list,judgement)
    all_unmatched_job_list=find_position_dict("job",unmatched_job_list,judgement)

    all_unmatched_dict={}
    all_unmatched_dict["location"]=all_unmatched_location_list
    all_unmatched_dict["job"]=all_unmatched_job_list
    all_data_dict["unmatched"]=all_unmatched_dict

    return all_data_dict

def regularize(text):
    regex_list="\s*"
    regex_text=""
    for i,token in enumerate(text):
        if i==0:
            regex_text=regex_list+token+regex_list
        else:
            regex_text=regex_text+token+regex_list
        
    return regex_text

def find_position_dict(kind,text_list,judgement):
    if len(text_list)==0:
        return []
    position_dict_list=[]
    for text in text_list:
        text_position_dict={}
        text_position=re.search(regularize(text),judgement)
        if text_position==None:
            continue
        text_position_dict["type"]=kind
        text_position_dict["name"]=text
        text_position_dict["start"]=text_position.start()
        text_position_dict["end"]=text_position.end()
        position_dict_list.append(text_position_dict.copy())
    return position_dict_list

if __name__ == "__main__":
    f = open(
        "/root/project/law_data/5d30de97cbd1c48dc98a329e.txt", 'r', newline="", encoding='utf-8')
    judgement = f.read()
    job_list=["檢察官","公務員","車手","車手頭","監管科人員","青壯年","包括"]
    location_list=["詐欺集團","臺灣臺北地方檢察署","臺灣新竹地方檢察署","政府機關","本院","新竹縣政府警察局","竹北"]
    # 先去空白 再去\r\n
    find_job_location_position(judgement,job_list,location_list)