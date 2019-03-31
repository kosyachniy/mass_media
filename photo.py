import sys

from PIL import Image, ImageFont, ImageDraw


def mass_media_old(template, background, text, width, height):
	canvas = Image.new('RGBA', template.size, (255, 255, 255, 255))
	background = background.resize((int(width * 0.9), int(height * 0.85)), Image.ANTIALIAS)

	canvas.paste(background, (int(width * 0.1), 0))
	canvas.paste(template, (0, 0), template)

	# Заголовок

	draw = ImageDraw.Draw(canvas)

	font = ImageFont.truetype('fonts/FS Joey Pro.otf', 60)
	text_w, text_h = draw.textsize(text, font=font)
	draw.text(((1.12 * width - text_w) // 2, int(0.87 * height)), text, font=font, fill='#ed2c2d')

	return canvas

def instagram(template, background, text, width, height):
	text = text.upper()

	background.paste(template, (0, 0), template)

	# Заголовок

	draw = ImageDraw.Draw(background)

	font = ImageFont.truetype('fonts/GOST Type A.ttf', int(0.092 * height))
	text_w, text_h = draw.textsize(text, font=font)
	draw.text(((width - text_w) // 2, int(0.906 * height)), text, font=font, fill='#fff')

	return background

def mass_media_wylsa(template, background, text, width, height):
	background.paste(template, (0, 0), template)

	draw = ImageDraw.Draw(background)

	# Категория

	first, last = text.find('#'), text.rfind('#')

	tag = text[first+1:] if first == last else text[first+1:last]
	tag = tag.title().strip()

	font = ImageFont.truetype('fonts/Roboto Medium.ttf', 72)
	text_w, text_h = draw.textsize(tag, font=font)
	draw.text((157, height - 383), tag, font=font, fill='#fff')

	# Время

	if first != last:
		tim = text[last+1:].lower().strip()

		font = ImageFont.truetype('fonts/Arial.ttf', 58)
		draw.text((194 + text_w, height - 369), '•', font=font, fill='#fff')

		font = ImageFont.truetype('fonts/Roboto Normal.ttf', 65)
		draw.text((246 + text_w, height - 377), tim, font=font, fill='#fff')

	# Заголовок

	font = ImageFont.truetype('fonts/Roboto Medium.ttf', 95)
	text_w, text_h = draw.textsize(text[:first], font=font)
	draw.text((157, height - 260), text[:first].strip(), font=font, fill='#fff')

	# Рамка

	canvas = Image.new('RGBA', (template.size[0] + 160, template.size[1] + 80), (255, 255, 255, 255))
	canvas.paste(background, (80, 40))

	return canvas

def ssc_posts(template, background, text, width, height):
	texts = text.strip().split('#')

	draw = ImageDraw.Draw(template)
	font = ImageFont.truetype('fonts/Segoe.ttf', 103)

	# Текст

	text_main = texts[0]

	if '\n' not in text_main:
		text_len = len(text_main)
		if text_len > 20:
			text_main = text_main.split(' ')

			mid = 0
			count = 0
			for i, el in enumerate(text_main):
				count += len(el) + 1

				if count > text_len // 2:
					mid = i + 1
					break

			text_main = ' '.join(text_main[:mid]) + '\n' + ' '.join(text_main[mid:])
		
		else:
			text_main = '\n' + text_main

	for i, el in enumerate(text_main.split('\n')):
		el = el.strip()

		text_w, text_h = draw.textsize(el, font=font)
		center = (2500 - 130 - 780 - text_w) // 2
		draw.text((780 + center, 50 + i * 125), el, font=font, fill='#505050')
	
	# Дополнительно

	text_sec = texts[1].strip()

	if len(texts) > 1:
		text_w, text_h = draw.textsize(text_sec, font=font)
		center = (2500 - 130 - 780 - text_w) // 2
		draw.text((780 + center, 355), text_sec, font=font, fill='#0084bd')

	#

	return template

def ssc_forms(template, background, text, width, height):
	pass

def curators():
	pass

PROCESS = (mass_media_old, instagram, mass_media_wylsa, ssc_posts, ssc_forms, curators)


def paste(image='re.jpg', text='Рандомный заголовок! #Мероприятия #11 декабря', style=3):
	style = int(style)

	template = Image.open('templates/{}.png'.format(style), 'r') # f'templates/{style}.png'

	tmp_width, tmp_height = template.size
	tmp_ratio = tmp_width / tmp_height

	if image:
		background = Image.open('data/{}'.format(image), 'r') # f'data/{image}'

		bck_width, bck_height = background.size
		bck_ratio = bck_width / bck_height

		if tmp_ratio > bck_ratio:
			margin = (bck_height - bck_width / tmp_ratio) // 2
			background = background.resize(template.size, Image.ANTIALIAS, (0, margin, bck_width, bck_height-margin))
		elif tmp_ratio < bck_ratio:
			margin = (bck_width - bck_height * tmp_ratio) // 2
			background = background.resize(template.size, Image.ANTIALIAS, (margin, 0, bck_width-margin, bck_height))
	
	else:
		background = None

	canvas = PROCESS[style-1](template, background, text, tmp_width, tmp_height)

	if image:
		name = 'results/' + image[:image.rfind('.')] + '.png'
	else:
		name = 'results/re.png'

	canvas.save(name)

	return name


if __name__ == '__main__':
	paste(*sys.argv[1:])