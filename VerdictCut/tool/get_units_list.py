from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import tensorflow as tf
import os

class get_units_list():
    def __init__(self, ckip_data_path = '/tf/itri/ckiptagger/data', disable_cuda = True, memory_limit=1024):
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit)])
            except RuntimeError as e:
                print(e)
        self.ws = WS(ckip_data_path, disable_cuda=disable_cuda)
        self.pos = POS(ckip_data_path, disable_cuda=disable_cuda)
        self.ner = NER(ckip_data_path, disable_cuda=disable_cuda)
        
    def slice_data(self, org_sentence, batch_size,window_size = 200, overlap = 50):
        all_list = []
        pos = 0
        
        org_sentence_list = []
        while( pos + window_size < len(org_sentence)):
            all_list.append(org_sentence[pos:pos+window_size+overlap])
            pos += window_size
            if len(all_list)>batch_size:
                org_sentence_list.append(all_list)
                all_list = []
        all_list.append(org_sentence[len(org_sentence)-window_size-overlap:])
        org_sentence_list.append(all_list)  
        
        # print(org_sentence_list)    
        # print(len(org_sentence_list))
        return org_sentence_list
    
       
    def parse(self,org_sentence, batch_size = 10):
        org_sentence_list = self.slice_data(org_sentence,batch_size)
        org_list = []
        
        for i in range(len(org_sentence_list)):
            word_sentence_list = self.ws(org_sentence_list[i])
            pos_sentence_list = self.pos(word_sentence_list)
            entity_sentence_list = self.ner(word_sentence_list, pos_sentence_list)
            
            for entity_sentence in entity_sentence_list:
                for word in entity_sentence:
                    if word[2]=='ORG':
                        org_list.append(word[3])

        org_list = list(set(org_list))
        return org_list
    
           
if __name__ == "__main__":
    units_list = get_units_list(disable_cuda = False)

    sen = "\r\n    級毒品海洛因及第二級毒品甲基安非他命予劉旗坪、劉清明\r\n    ，共3 次。\r\n  (二)劉旗坪意圖營利，分別基於販賣第一級毒品海洛因、第二級\r\n    毒品甲基安非他命之犯意，於如附表二編號1 至6 所示之時\r\n    間、地點，各以如附表二編號1 至6 所示之方式、價額及數\r\n    量，分別販賣第一級毒品海洛因、第二級毒品甲基安非他命\r\n    予邱華光、羅永新、鍾沅融及劉良發，共6 次。\r\n  (三)劉旗坪另與林裕峯( 由本院另行審結) 共同意圖營利，基於\r\n    販賣第二級毒品甲"
    print(units_list.parse(sen))