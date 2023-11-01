import numpy as np
import ffmpeg
import cv2
import imageio as iio

class Practice1:
    def __init__(self):
        pass

    def launch(self):
        exercise = '0'
        while exercise != 'EXIT':
            exercise = input('Which exercise shall we solve now? Expected integer from 1 to 6, '
                             'EXIT to end the program\n')

            if exercise == '1':
                print('RGB-YUV conversions\n')
                r = float(input('Red value: '))
                g = float(input('Green value: '))
                b = float(input('Blue value: '))
                rgb_color = [r, g, b]
                yuv_color = self.rgb_yuv(rgb_color)
                print('\nBack to RGB!')
                self.yuv_rgb(yuv_color)
            elif exercise == '2':
                image_name = 'messi.jpg'
                print('Resizing image ', image_name, '\n')
                self.resize_img(image_name)
            elif exercise == '3':
                print('Serpentine scan\n')
                filepath = 'barça.jpg'
                w_size = 8
                # The width and height of this image are multiples of 8,
                # which will make the scanning easier
                img = cv2.imread(filepath)
                width = img.shape[0]
                height = img.shape[1]
                yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                y_values = yuv_img[:, :, 0]
                for r in range(0, height-w_size, w_size):
                    for c in range(0, width-w_size, w_size):
                        cur_window = y_values[r:r+w_size, c:c+w_size]
                        cur_window = np.array(cur_window).flatten()
                        self.serpentine(cur_window)
                        print(r, c)
            elif exercise.upper() == 'EXIT':
                print('See you soon!')
                return
            else:
                print('Invalid input, please try again.')

    def rgb_yuv(self, rgb):
        matrix = [[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]]
        yuv = np.matmul(matrix, rgb)
        print('YUV values: ', yuv)
        return yuv
    # Reference: https://www.cs.sfu.ca/mmbook/programming_assignments/additional_notes/rgb_yuv_note/RGB-YUV.pdf

    def yuv_rgb(self, yuv):
        matrix = [[1.0, 0.0, 1.13983], [1.0, -0.39465, -0.58060], [1.0, 2.03211, 0.0]]
        rgb = np.matmul(matrix, yuv)
        print('RGB values: ', rgb)
        return rgb

    def resize_img(self, img):
        output_name = 'output_resized_messi.jpg'
        (
            ffmpeg
            .input(img)
            .filter('scale', width=320, height=-1)
            .output('output_resized_messi.jpg')
            .run()
        )
        print('Resizing completed. Open ', output_name, 'to see results.')
        return

    def serpentine(self, block):     # Expected 8x8 block
        scan = [1, 2, 9, 17, 10, 3, 4, 11, 18, 25, 33, 26, 19, 12, 5, 6, 13, 20, 27, 34, 41, 49, 42, 35, 28, 21, 14,
                7, 8, 15, 22, 29, 36, 43, 50, 57, 58, 51, 44, 37, 30, 23, 16, 24, 31, 38, 45, 52, 59, 60, 53, 46, 39,
                32, 40, 47, 54, 61, 62, 55, 48, 56, 63, 64]     # Coefficients order
        res_block = block
        for el in scan:
            print(block[el-1])
        return

    def compress_bw(self, img):
        (
            ffmpeg
            .input(img)
            .output('output_compressed_messi.jpg', **{'qscale:v=100'})
            .run()
        )
        (
            ffmpeg
            .input('output_compressed_messi.jpg')
            .filter('format', 'gray')
            .output('output_compressed_bw_messi.jpg')
            .run()
        )
        return


if __name__ == '__main__':

    practice = Practice1()

    practice.launch()

    # Task 4
    # image_name = 'messi.jpg'
    # compress_bw(image_name)
