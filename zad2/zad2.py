import argparse
import ast
import json
from PIL import Image
from PIL import ImageDraw


def color_to_rgb(color, palette):
    if color[0] == '(':
        print("lit:", ast.literal_eval(color))
        return ast.literal_eval(color)
    elif color[0] == '#':
        return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
    else:
        return color_to_rgb(palette[color], palette)


def create_figures(figures_list, def_color, palette):
    result = []
    for figure in figures_list:
        if 'color' not in figure:
            figure['color'] = def_color
        figure['color'] = color_to_rgb(figure['color'], palette)
        result.append(create_figure(figure))
    return result


def create_figure(figure):
    if figure['type'] == 'point':
        return Point(figure['x'], figure['y'], figure['color'])
    elif figure['type'] == 'polygon':
        return Polygon(figure['points'], figure['color'])
    elif figure['type'] == 'rectangle':
        return Rectangle(figure['x'], figure['y'], figure['width'], figure['height'], figure['color'])
    elif figure['type'] == 'square':
        return Square(figure['x'], figure['y'], figure['size'], figure['color'])
    elif figure['type'] == 'circle':
        return Circle(figure['x'], figure['y'], figure['radius'], figure['color'])


class Figure:

    def __init__(self, color):
        self.color = color


    # def print_onto_image(self, image):


class Point(Figure):

    def __init__(self, x, y, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y

    # TODO
    # na pewno! da się lepiej, jakoś statycznie, mieć jeden drawer
    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.point((self.x, self.y), self.color)


class Polygon(Figure):

    def __init__(self, points_list, color):
        Figure.__init__(self, color)
        self.points_list = [point for point in points_list]

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        #powinny być tuple, albo nie listy - points_list
        draw.polygon([tuple(x) for x in self.points_list], self.color)


class Rectangle(Figure):

    def __init__(self, x, y, width, height, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.rectangle([self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2], self.color)


class Square(Figure):

    def __init__(self, x, y, size, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y
        self.size = size

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            [self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2],
            self.color)


class Circle(Figure):

    def __init__(self, x, y, radius, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y
        self.radius = radius

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.ellipse([self.x-self.radius/2, self.y-self.radius/2,self.x+self.radius/2, self.y+self.radius/2], self.color)


class MyImage():

    def __init__(self, screen_info, palette):
        self.__palette = palette
        self.__width = screen_info['width']
        self.__height = screen_info['height']
        self.__bg_color = color_to_rgb(screen_info['bg_color'], self.__palette)
        self.__fg_color = color_to_rgb(screen_info['fg_color'], self.__palette)
        self.image = Image.new("RGB", (self.__width, self.__height), self.__bg_color)
        self.figures_array = []

    def process_figures(self):
        for figure in self.figures_array:
            figure.print_onto_image(self.image)

    def show_self(self):
        self.image.show()

    def save_to_file(self, file_handler):
        #for i in range(300, 500):
        #    for j in range(200, 400):
        #        self.image.putpixel((i, j), (255, 0, 0))
        # w.write_packed(file_handler, self.image_array)
        # color_pixel((255, 0, 0), 1, 1, self.image_array)
        # w.write(file_handler, self.image_array)
        self.image.save(file_handler, format="png")


def init_and_parse():
    parser = argparse.ArgumentParser(description='Get filenames.')
    parser.add_argument('input_file_name')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    return args.input_file_name, args.output


def process_json(input_file):
    input_file_handle = open(input_file)
    data = json.load(input_file_handle)
    print('Screen info:', data['Screen'])
    print('Palette:', data['Palette'])

    return data


if __name__ == "__main__":
    input_file, output_file = init_and_parse()
    print('input:', input_file, 'output: ', output_file)
    data = process_json(input_file)
    img = MyImage(data['Screen'], data['Palette'])
    img.figures_array = create_figures(data['Figures'], data['Screen']['fg_color'], data['Palette'])
    img.process_figures()
    if output_file is not None:
        img.save_to_file(output_file)
    img.show_self()
