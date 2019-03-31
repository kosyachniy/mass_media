import time

import requests

from func.vk_group import read, send, prev
from photo import paste


RESOURCES = ['Instagram', 'СМИ', 'СНО', 'Кураторы']


while True:
	try:
		new_message = read()

	except:
		print('Ошибка чтения!')
		time.sleep(5)

	else:
		for i in new_message:
			if i[1] in RESOURCES:
				print('{:50}'.format(i[1]), end='	')

				res = prev(i[0])
				if res:
					image = []
					for url in res[2]:
						image.append(url.split('/')[-1].split('.')[0] + '.jpg')

						with open('data/' + image[-1], 'wb') as file:
							file.write(requests.get(url).content)

						image[-1] = paste(image[-1], res[1], RESOURCES.index(i[1])+2)

					try:
						send(i[0], '', image)
						print('✔')

					except:
						print('❌')
						time.sleep(1)
				
				else:
					send(i[0], 'Не вижу картинок')
			
			else:
				send(i[0], 'Куда?', keyboard=[['СМИ', 'Instagram'], ['СНО', 'Кураторы']])

	time.sleep(1)