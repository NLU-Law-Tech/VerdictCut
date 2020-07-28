from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os

class get_units_list():
    def __init__(self, ckip_data_path = '/tf/itri/ckiptagger/data'):
        self.ws = WS(ckip_data_path)
        self.pos = POS(ckip_data_path)
        self.ner = NER(ckip_data_path)
        # self.dictionary = construct_dictionary(self.__load_custom_dict(custom_dict_path))
    
    # def __load_custom_dict(self,custom_dict_path):         
    #     # load all file under path         
    #     dicts = os.listdir(custom_dict_path)         
    #     word_to_weight = {}         
    #     for dic in dicts:             
    #         with open(custom_dict_path + '/' + dic, 'r', encoding='utf-8') as f:                 
    #             while(True):                     
    #                 line = f.readline()                     
    #                 if(len(line)==0):                         
    #                     break                     
    #                 line_split = line.split()                     
    #                 word = line_split[0]                    
    #                 try:                         
    #                     word_weight = line_split[1]                     
    #                 except:                         
    #                     word_weight = 1                     
    #                 word_to_weight.update({word:word_weight})        
    #     return word_to_weight
    

       
    def parse(self,org_sentence):
        org_sentence_list = [org_sentence]
        org_list = []
        
        word_sentence_list = self.ws(org_sentence_list)
        pos_sentence_list = self.pos(word_sentence_list)
        entity_sentence_list = self.ner(word_sentence_list, pos_sentence_list)
        for word in list(entity_sentence_list[0]):
            if word[2]=='ORG':
                org_list.append(word[3])
        return org_list
        # for i, sentence in enumerate(org_sentence):
        #     for word in list(entity_sentence[0]):
        #         if word[2]=='ORG':
        #             org_list.append(word[3])
        #     return org_list
           
if __name__ == "__main__":
    units_list = get_units_list()

    sen = "\r\n    級毒品海洛因及第二級毒品甲基安非他命予劉旗坪、劉清明\r\n    ，共3 次。\r\n  (二)劉旗坪意圖營利，分別基於販賣第一級毒品海洛因、第二級\r\n    毒品甲基安非他命之犯意，於如附表二編號1 至6 所示之時\r\n    間、地點，各以如附表二編號1 至6 所示之方式、價額及數\r\n    量，分別販賣第一級毒品海洛因、第二級毒品甲基安非他命\r\n    予邱華光、羅永新、鍾沅融及劉良發，共6 次。\r\n  (三)劉旗坪另與林裕峯( 由本院另行審結) 共同意圖營利，基於\r\n    販賣第二級毒品甲"
    print(units_list.parse(sen))
  
    
    # units_list = []
    # return units_list