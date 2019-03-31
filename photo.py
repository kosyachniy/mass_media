import sys

from PIL import Image

from templates import PROCESS


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