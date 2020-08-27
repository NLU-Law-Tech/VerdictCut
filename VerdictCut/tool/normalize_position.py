import re

def normalize_position(unnormalization_position, position_list):
    """
    職稱正規化
    """
    _current_len = 0
    _current_position = ''
    for position in position_list:
        re_res = re.search(position, unnormalization_position)
        if (re_res is not None):
            _re_start,_re_end = re_res.span()
            _len = int(_re_end) - int(_re_start)                    
            if(_len > _current_len):
                _current_len = _len                        
                _current_position = position
    
    return _current_position
