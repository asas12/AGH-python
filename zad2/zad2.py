import argparse
#import png
import ast
import json
from PIL import Image

def color_to_rgb(color, palette):
    if color[0] == '(':
        print("lit:", ast.literal_eval(color))
        return ast.literal_eval(color)
    elif color[0] == '#':
        return (int(color[1:3], 16), int(color[3:5], 16),int(color[5:7], 16))
    else:
        return color_to_rgb(palette[color], palette)


def color_pixel(color, x, y, image_array):
    for i in range(3):
        image_array[y][x*3+i] = color[i]


class Figure():

    def __init__(self):
        self.__color = 1


class My_Image():

    def __init__(self, screen_info, palette):
        self.__palette = palette
        self.__width = screen_info['width']
        self.__height = screen_info['height']
        self.__bg_color = color_to_rgb(screen_info['bg_color'], self.__palette)
        self.__fg_color = color_to_rgb(screen_info['fg_color'], self.__palette)
        self.image_array = [[x for i in range(self.__width) for x in self.__bg_color] for i in range(self.__height)]
        self.figures_array = []
        #print(len(self.image_array))
        #self.image_array = [self.__bg_color[0:2] for i in range(self.__width*self.__height)]

    def show_self(self):
        print("TODO! :)")

    def save_to_file(self, file_handler):
        #w = png.Writer(self.__width, self.__height, background=self.__bg_color)
        for i in range(300,500):
           for j in range(200, 400):
                color_pixel((255,0,0), i, j, self.image_array)
        #w.write_packed(file_handler, self.image_array)
        color_pixel((255, 0, 0), 1, 1, self.image_array)
        #w.write(file_handler, self.image_array)



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
    for figure in data['Figures']:
        if figure['type'] == 'point':
            print('Point: x:', figure['x'], 'y', figure['y'])
        else:
            print(figure)
        if 'color' in figure:
            print(color_to_rgb(figure['color'], data['Palette']))
            figure['color'] = color_to_rgb(figure['color'], data['Palette'])
    return data


if __name__ == "__main__":
    #input_file, output_file = init_and_parse()
    #print('input:', input_file, 'output: ', output_file)
    #data = process_json(input_file)
    #img = My_Image(data['Screen'], data['Palette'])
    #output_file_handle = open(output_file, 'wb')
    #img.save_to_file(output_file_handle)
    im = Image.open("ala.png")
    im.show()