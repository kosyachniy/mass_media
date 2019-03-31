import time

import requests

from func.vk_group import read, send, prev
from photo import paste


RESOURCES = ('Instagram', 'СМИ', 'СНО пост', 'СНО форма', 'Кураторы')
DEMAND = (True, True, False, False, True)


while True:
	try:
		new_message = read()

	except:
		print('Ошибка чтения!')
		time.sleep(5)

	else:
		for i in new_message:
			cond_post = 'пост сно' in i[1].lower()
			cond_form = 'форма сно' in i[1].lower()
			cond = cond_post or cond_form

			if i[1] in RESOURCES or cond:
				print('{:50}'.format(i[1]), end='	')

				if cond:
					res = list(i)

					if cond_post:
						ind = 2
						st = res[1].lower().find('пост сно')
						le = 8
					else:
						ind = 3
						st = res[1].lower().find('форма сно')
						le = 9

					res[1] = res[1][st+le:]

				else:
					ind = RESOURCES.index(i[1])
					res = prev(i[0])

				if res:
					# Нет обязательной картинки
					if DEMAND[ind]:
						if not len(res[2]):
							send(i[0], 'В последнем сообщении нет картинки!')
							continue
					
					# Картинка не нужна
					else:
						res = list(res)
						res[2] = [None]

					# Обработка

					image = []
					for url in res[2]:
						if url:
							image.append(url.split('/')[-1].split('.')[0] + '.jpg')

							with open('data/' + image[-1], 'wb') as file:
								file.write(requests.get(url).content)
						
						else:
							image.append(None)

						image[-1] = paste(image[-1], res[1], ind+2)

					try:
						send(i[0], '', image)
						print('✔')

					except:
						print('❌')
						time.sleep(1)
				
				else:
					send(i[0], 'Чё та не так')
			
			else:
				send(i[0], 'Куда?', keyboard=[['СМИ', 'Instagram'], ['СНО пост', 'СНО форма'], ['Кураторы']])

	time.sleep(1)