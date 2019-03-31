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
def send(user, cont, img=[], keyboard=None):
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
		'random_id': int(time.time() * 1000000),
		'user_id': user,
		'message': cont,
		'attachment': ','.join(img),
	}

	# Клавиатура
	if keyboard:
		buttons = []
		for j in keyboard:
			line = []
			for i in j:
				line.append({
					'action': {
						'type': 'text',
						'payload': '{\"button\": \"1\"}',
						'label': i,
					},
					'color': 'default',
				})
			buttons.append(line)

		req['keyboard'] = json.dumps({
			'one_time': False,
			'buttons': buttons,
		}, ensure_ascii=False)

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

# Предшествующее значящее сообщение
def prev(user):
	t = True

	for i in vk.method('messages.getHistory', {'user_id': user})['items']:
		if i['from_id'] == user:
			if t:
				t = False
				continue

			return (
				i['from_id'],
				i['text'],
				[max_size(j['photo']) for j in i['attachments'] if j['type'] == 'photo'] if 'attachments' in i else [],
			)