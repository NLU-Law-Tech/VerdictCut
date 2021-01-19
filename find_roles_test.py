# -*- coding: utf-8 -*-
from VerdictCut import find_roles as verdict_find_roles
import pytest


test_data = [
	#即被告中間是全形空白，後續的被告也是全型空白開頭
	("臺灣高等法院刑事判決　　　　　　　　107年度上訴緝字第2號\r\n上　訴　人\r\n即　被　告　王孟顯\r\n　　　王孟\r\n上列上訴人因貪污治罪條例案件，不服臺灣臺北地方法院85年度\r\n訴字第706 號，中華民國86年7 月23日第一審判決（起訴案號：\r\n臺灣臺北地方法院檢察署84年度偵字第11170 號），提起上訴，\r\n本院判決如下：\r\n    主  文\r\n原判決撤銷。", 
		[{'name': '王孟顯', 'role': '被告'}, {'name': '王孟', 'role': '被告'}]),
	#即被告中間是半形空白
	("臺灣高等法院刑事判決\r\n109年度上更一字第102號\r\n上  訴  人 \r\n即  被  告  謝俊儒\r\n\r\n\r\n指定辯護人  本院公設辯護人陳德仁 \r\n上列上訴人即被告因違反毒品危害防制條例等案件，不服臺灣新竹地方法院107年度訴字第201、804號，中華民國108年1月22日第一審判決（起訴案號：臺灣新竹地方檢察署107年度偵緝字第102、103號），提起上訴，本院判決後，經最高法院撤銷發回更審（109年度台上字第2829號），本院判決如下：\r\n    主  文\r\n原判決關於被告謝俊儒部分撤銷。", 
		[{'name': '謝俊儒', 'role': '被告'}]),
	#沒有被告的判決書
	("aaaaaaaaaa", 
		[]),
	]

@pytest.mark.parametrize("test_input,expected", test_data,
						ids=[
                             "即被告中間是全形空白，後續的被告也是全型空白開頭",
                             "即被告中間是半形空白",
                             "無被告測試",
                         ])
def test1(test_input, expected):
	assert verdict_find_roles(test_input, target_roles=['被告'], break_line='\r\n')==expected
