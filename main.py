from func.vk_user import *
from photo import paste

import time


while True:
	try:
		new_message = read()
	except:
		time.sleep(5)
	else:
		for i in new_message:
			if len(i[2]):
				image = []
				for url in i[2]:
					image.append(url.split('/')[-1].split('.')[0] + '.jpg')

					with open('data/' + image[-1], 'wb') as file:
						file.write(requests.get(url).content)

					image[-1] = paste(image[-1], i[1])

				print(i[1])
				send(i[0], i[1], image)

	time.sleep(1)