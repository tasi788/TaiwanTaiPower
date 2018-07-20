import requests
url = 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.txt'

def run():
	r = requests.get(url)
	r.encoding = 'utf-8'
	array = r.text.replace('\r', '').split('\n')
	msg = ''
	def process(text):
		text = text.replace('"', '')
		text = text.replace('",', '')
		text = text.replace(',', '')
		return float(text)

	#今日預估淨尖峰供電能力
	getmsg_reserve_supply = process(array[4])

	#今日預估尖峰負載
	getmsg_reserve_load = process(array[3])

	#今日預估尖峰備轉容量率
	getmsg_reserve = ((getmsg_reserve_supply-getmsg_reserve_load)/getmsg_reserve_load)*100
	#print('尖峰備轉容量率：',round(getmsg_reserve, 2))
	msg += '尖峰備轉容量率：{}%\n'.format(round(getmsg_reserve, 2))

	#目前用電量千瓦
	getmsg_reserve_loaded = process(array[2])

	#今日預估尖峰備轉容量
	getmsg_reserve_cap = (getmsg_reserve_supply-getmsg_reserve_load)

	if getmsg_reserve >= 10.00:
		msg += '供電充裕，系統供電餘裕充足。\n'
	elif getmsg_reserve < 10.00 and getmsg_reserve > 6:
		msg += '供電吃緊，系統供電餘裕緊澀。\n'
	elif getmsg_reserve <= 6.00 and getmsg_reserve_cap > 900.0:
		msg += '供電警戒，系統限電機率增加。\n'
	elif getmsg_reserve <= 6.00 and getmsg_reserve_cap <= 900.0 and getmsg_reserve_cap > 500.0:
		msg += '90萬瓩以下，限電警戒。\n'
	elif getmsg_reserve <= 6.00 and getmsg_reserve_cap <= 500.0:
		msg += '50萬瓩以下，限電警戒。\n'

	#目前用電
	getmsg_reserve_useage = process(array[2])
	nowuseage = (getmsg_reserve_useage/getmsg_reserve_supply)*100

	msg +='目前用電量：{now}萬瓩\n使用率：{useage}%'.format(now=getmsg_reserve_loaded,useage=round(nowuseage,2))
	return msg
