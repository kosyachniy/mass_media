import json
import time

import vk_api
import requests


with open('keys.json', 'r') as file:
	data = json.loads(file.read())['vk']

	vk = vk_api.VkApi(token=data['token'])


def max_size(lis, name='photo'):
	q = set(lis.keys())
	ma = 0

	if 'sizes' in q:
		for i, el in enumerate(lis['sizes']):
			if el['width'] > lis['sizes'][ma]['width']:
				ma = i

		return lis['sizes'][ma]['url']

	else:
		for t in q:
			if name + '_' in t and int(t[6:]) > ma:
				ma = int(t[6:])

		return lis[name + '_' + str(ma)]


# Отправить сообщение
def send(user, cont, img=[]):
	# Изображения
	for i in range(len(img)):
		if img[i][0:5] != 'photo':
			# Загружаем изображение на сервер
			if img[i].count('/') >= 3: # Если файл из интернета
				with open('re.jpg', 'wb') as file:
					file.write(requests.get(img[i]).content)
				img[i] = 're.jpg'

			# Загружаем изображение в ВК
			url = vk.method('photos.getMessagesUploadServer')['upload_url']

			response = requests.post(url, files={'photo': open(img[i], 'rb')})
			result = json.loads(response.text)

			photo = vk.method('photos.saveMessagesPhoto', {'server': result['server'], 'photo': result['photo'], 'hash': result['hash']})

			img[i] = 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])

	req = {
		'user_id': user,
		'message': cont,
		'attachment': ','.join(img),
	}

	return vk.method('messages.send', req)

# Последние непрочитанные сообщения
def read():
	messages = []
	for i in vk.method('messages.getConversations')['items']:
		if 'unanswered' in i['conversation']:
			messages.append((
				i['conversation']['peer']['id'],
				i['last_message']['text'],
				[max_size(j['photo']) for j in i['last_message']['attachments'] if j['type'] == 'photo'] if 'attachments' in i['last_message'] else [],
			))
	return messages