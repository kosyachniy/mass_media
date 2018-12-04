from PIL import Image, ImageFont, ImageDraw 


def mass_media_old(template, background, text, canvas, width, height):
	background = background.resize((int(width * 0.9), int(height * 0.85)), Image.ANTIALIAS)

	canvas.paste(background, (int(width * 0.1), 0))
	canvas.paste(template, (0, 0), template)

	draw = ImageDraw.Draw(canvas)
	font = ImageFont.truetype('fonts/FS_JoeyPro-MediumRegular.otf', 60)

	text_w, text_h = draw.textsize(text, font=font)
	draw.text(((1.12 * width - text_w) // 2, int(0.87 * height)), text, font=font, fill='#ed2c2d')

	return canvas

TEMPLATE = 1
PROCESS = (mass_media_old, )


def paste(image, text, style=TEMPLATE):
	template = Image.open(f'templates/{style}.png', 'r')
	background = Image.open(f'data/{image}', 'r')
	canvas = Image.new('RGBA', template.size, (255, 255, 255, 255))

	width, height = template.size

	canvas = PROCESS[style-1](template, background, text, canvas, width, height)

	name = 'results/' + image[:image.rfind('.')] + '.png'
	canvas.save(name)

	return name


if __name__ == '__main__':
	paste('re.jpg', 'Рандомный заголовок!', 1)