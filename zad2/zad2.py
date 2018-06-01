import argparse
import ast
import json
from PIL import Image
from PIL import ImageDraw


def color_to_rgb(color):
    if color[0] == '(':
        return ast.literal_eval(color)
    elif color[0] == '#':
        return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    else:
        return color


def create_figures(figures_list, def_color):
    result = []
    for figure in figures_list:
        if 'color' not in figure:
            figure['color'] = def_color
        else:
            figure['color'] = color_to_rgb(figure['color'])
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

    def print_onto_image(self, image):
        pass


class Point(Figure):

    def __init__(self, x, y, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.point((self.x, self.y), self.color)


class Polygon(Figure):

    def __init__(self, points_list, color):
        Figure.__init__(self, color)
        self.points_list = [point for point in points_list]

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        # powinny być tuple, albo nie listy - points_list
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
        draw.rectangle(
            [self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2],
            self.color)


class Square(Figure):

    def __init__(self, x, y, size, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y
        self.size = size

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            [self.x - self.size/2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2],
            self.color)


class Circle(Figure):

    def __init__(self, x, y, radius, color):
        Figure.__init__(self, color)
        self.x = x
        self.y = y
        self.radius = radius

    def print_onto_image(self, image):
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            [self.x-self.radius/2, self.y-self.radius/2,self.x+self.radius/2, self.y+self.radius/2],
            self.color)


class MyImage:

    def __init__(self, screen_info, figures):
        self.__width = screen_info['width']
        self.__height = screen_info['height']
        self.__bg_color = screen_info['bg_color']
        self.__fg_color = screen_info['fg_color']
        self.image = Image.new("RGB", (self.__width, self.__height), self.__bg_color)
        self.figures_array = create_figures(figures, self.__fg_color)

    def paint_figures_onto_image(self):
        for figure in self.figures_array:
            figure.print_onto_image(self.image)

    def show_self(self):
        self.image.show()

    def save_to_file(self, filename):
        self.image.save(filename, format="png")


def parse_filenames():
    parser = argparse.ArgumentParser(description='Get filenames.')
    parser.add_argument('input_file_name')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    print('input:', args.input_file_name, '\noutput: ', args.output)
    return args.input_file_name, args.output


def process_json(in_filename):
    with open(in_filename) as in_file_handle:
        json_data = json.load(in_file_handle)
    return json_data['Screen'], json_data['Palette'], json_data['Figures']


def palette_to_rgb(palette):
    for color in palette:
        palette[color] = color_to_rgb(palette[color])


def screen_colors_to_rgb(screen, palette):
    screen['fg_color'] = palette[screen['fg_color']]
    screen['bg_color'] = palette[screen['bg_color']]


if __name__ == "__main__":
    input_filename, output_filename = parse_filenames()
    screen, palette, figures = process_json(input_filename)
    palette_to_rgb(palette)
    screen_colors_to_rgb(screen, palette)
    img = MyImage(screen, figures)
    img.paint_figures_onto_image()
    if output_filename is not None:
        img.save_to_file(output_filename)
    img.show_self()
