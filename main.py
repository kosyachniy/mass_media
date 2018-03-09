from func.vk_user import *
from time import sleep
from photo import paste

'''
def parse(text):
	text = text.replace('мы', 'они')

	return text
'''

def max_size(lis):
	q = set(lis.keys())
	ma = 0
	for t in q:
		if 'photo_' in t and int(t[6:]) > ma:
			ma = int(t[6:])
	return lis['photo_' + str(ma)]

while True:
	try:
		new_message = read()
	except:
		sleep(5)
	else:
		for i in new_message:
			image = []
			for j in i[2]:
				url = max_size(j['photo'])
				image.append('data/%d-%d.jpg' % (j['photo']['owner_id'], j['photo']['id']))

				with open(image[-1], 'wb') as file:
					file.write(requests.get(url).content)

				paste(image[-1], i[1])
				image[-1] = image[-1][:-4] + '.png'

			print(i[1])
			send(i[0], i[1], image)

	sleep(1)