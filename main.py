import time

import requests

from func.vk_group import read, send
from photo import paste


while True:
	try:
		new_message = read()

	except:
		print('Ошибка чтения!')
		time.sleep(5)

	else:
		for i in new_message:
			if len(i[2]):
				image = []
				for url in i[2]:
					image.append(url.split('/')[-1].split('.')[0] + '.jpg')

					with open('data/' + image[-1], 'wb') as file:
						file.write(requests.get(url).content)

					image[-1] = paste(image[-1], i[1], 3 if '#' in i[1] else 2)

				print(i[1])

				try:
					send(i[0], '', image)

				except:
					print('Ошибка отправки!')
					time.sleep(1)

	time.sleep(1)