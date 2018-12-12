from PIL import Image, ImageFont, ImageDraw


def mass_media_old(template, background, text, width, height):
	canvas = Image.new('RGBA', template.size, (255, 255, 255, 255))
	background = background.resize((int(width * 0.9), int(height * 0.85)), Image.ANTIALIAS)

	canvas.paste(background, (int(width * 0.1), 0))
	canvas.paste(template, (0, 0), template)

	draw = ImageDraw.Draw(canvas)
	font = ImageFont.truetype('fonts/FS Joey Pro.otf', 60)

	text_w, text_h = draw.textsize(text, font=font)
	draw.text(((1.12 * width - text_w) // 2, int(0.87 * height)), text, font=font, fill='#ed2c2d')

	return canvas

def instagram(template, background, text, width, height):
	text = text.upper()

	background.paste(template, (0, 0), template)

	draw = ImageDraw.Draw(background)
	font = ImageFont.truetype('fonts/GOST Type A.ttf', int(0.092 * height))

	text_w, text_h = draw.textsize(text, font=font)
	draw.text(((width - text_w) // 2, int(0.906 * height)), text, font=font, fill='#fff')

	return background

def mass_media_wylsa(template, background, text, width, height):
	background.paste(template, (0, 0), template)

	draw = ImageDraw.Draw(background)
	font = ImageFont.truetype('fonts/Roboto Medium.ttf', 62)

	# Тег

	first, last = text.find('#'), text.rfind('#')

	tag = text[first+1:] if first == last else text[first+1:last]
	tag = tag.title().strip()

	text_w, text_h = draw.textsize(tag, font=font)
	draw.text((157, height - 362), tag, font=font, fill='#fff')


	# Время

	if first != last:
		tim = text[last+1:].lower().strip()

		font = ImageFont.truetype('Arial', 48)
		draw.text((202 + text_w, height - 348), '•', font=font, fill='#fff')

		font = ImageFont.truetype('fonts/Roboto Normal.ttf', 55)
		draw.text((242 + text_w, height - 355), tim, font=font, fill='#fff')

	# Основной заголовок

	font = ImageFont.truetype('fonts/Roboto Medium.ttf', 84)

	text_w, text_h = draw.textsize(text[:first], font=font)
	draw.text((157, height - 249), text[:first].strip(), font=font, fill='#fff')

	return background

TEMPLATE = 3
PROCESS = (mass_media_old, instagram, mass_media_wylsa)


def paste(image, text, style=TEMPLATE):
	template = Image.open('templates/{}.png'.format(style), 'r') # f'templates/{style}.png'
	background = Image.open('data/{}'.format(image), 'r') # f'data/{image}'

	tmp_width, tmp_height = template.size
	bck_width, bck_height = background.size
	tmp_ratio = tmp_width / tmp_height
	bck_ratio = bck_width / bck_height

	if tmp_ratio > bck_ratio:
		margin = (bck_height - bck_width / tmp_ratio) // 2
		background = background.resize(template.size, Image.ANTIALIAS, (0, margin, bck_width, bck_height-margin))
	elif tmp_ratio < bck_ratio:
		margin = (bck_width - bck_height * tmp_ratio) // 2
		background = background.resize(template.size, Image.ANTIALIAS, (margin, 0, bck_width-margin, bck_height))

	canvas = PROCESS[style-1](template, background, text, tmp_width, tmp_height)

	name = 'results/' + image[:image.rfind('.')] + '.png'
	canvas.save(name)

	return name


if __name__ == '__main__':
	paste('re.jpg', 'Рандомный заголовок! #Мероприятия #11 декабря')