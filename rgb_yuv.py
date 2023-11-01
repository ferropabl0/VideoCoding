import numpy as np
import ffmpeg
import cv2


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
                opt = input('Press 1 for scanning a single block, 0 for the whole image\n')
                filepath = 'barça.jpg'
                w_size = 8
                # The width and height of this image are multiples of 8,
                # which will make the scanning easier
                img = cv2.imread(filepath)
                width = img.shape[1]
                height = img.shape[0]
                yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                y_values = yuv_img[:, :, 0]     # We will scan the Y values

                if opt == '0':
                    count = 1
                    for r in range(0, height, w_size):
                        for c in range(0, width, w_size):
                            cur_window = y_values[r:r+w_size, c:c+w_size]
                            cur_window = np.array(cur_window).flatten()
                            print('Block ', count)
                            self.serpentine(cur_window)
                            count += 1
                elif opt == '1':
                    print('Enter the bottom-left pixel coordinates\nMax row:', height-w_size,
                          'Max column:', width-w_size)
                    ver = int(input('Row: '))
                    hor = int(input('Column: '))
                    cur_window = y_values[ver:ver + w_size, hor:hor + w_size]
                    cur_window = np.array(cur_window).flatten()
                    self.serpentine(cur_window)
                else:
                    print('Invalid option')

            elif exercise == '4':
                image_name = 'messi.jpg'
                print('Compressed b/w', image_name, '\n')
                self.compress_bw(image_name)

            elif exercise == '5':
                print('Run-length encoding')
                bit_str = input('Enter a string of bits: ')
                self.run_length(bit_str)

            elif exercise.upper() == 'EXIT':
                print('See you soon!')
                return
            else:
                print('Invalid input, please try again.')

    @staticmethod
    def rgb_yuv(rgb):
        matrix = [[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]]
        yuv = np.matmul(matrix, rgb)
        print('YUV values: ', yuv)
        return yuv
    # Reference: https://www.cs.sfu.ca/mmbook/programming_assignments/additional_notes/rgb_yuv_note/RGB-YUV.pdf

    @staticmethod
    def yuv_rgb(yuv):
        matrix = [[1.0, 0.0, 1.13983], [1.0, -0.39465, -0.58060], [1.0, 2.03211, 0.0]]
        rgb = np.matmul(matrix, yuv)
        print('RGB values: ', rgb)
        return rgb

    @staticmethod
    def resize_img(img):
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

    @staticmethod
    def serpentine(block):     # Expected 8x8 block
        print('Original block:', block)
        scan = [1, 2, 9, 17, 10, 3, 4, 11, 18, 25, 33, 26, 19, 12, 5, 6, 13, 20, 27, 34, 41, 49, 42, 35, 28, 21, 14,
                7, 8, 15, 22, 29, 36, 43, 50, 57, 58, 51, 44, 37, 30, 23, 16, 24, 31, 38, 45, 52, 59, 60, 53, 46, 39,
                32, 40, 47, 54, 61, 62, 55, 48, 56, 63, 64]     # Coefficients order

        scanned_block = [[0 for _ in range(8)] for _ in range(8)]
        i = 0
        j = 0
        for el in scan:
            scanned_block[j][i] = block[el-1]
            if i == 7:
                i = 0
                j += 1
            else:
                i += 1
        print('Scanned block: ', scanned_block)

        return

    @staticmethod
    def compress_bw(img):
        (
            ffmpeg
            .input(img)
            .filter('format', 'gray')
            .output('output_bw_messi.jpg')
            .run()
        )
        img = cv2.imread('output_bw_messi.jpg')
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, 1]
        cv2.imwrite('output_compressed_bw_messi.jpg', img, compression_params)
        # We can see how the grayscale image was heavily compressed,
        # and the image quality is much worse. Pixels in the same area
        # have now the same values, and it looks really unnatural
        return

    @staticmethod
    def run_length(bits):
        encoded = []
        count = 1
        for i in range(1, len(bits)):
            if bits[i] == bits[i - 1]:
                count += 1
            else:
                encoded.append((bits[i - 1], count))
                count = 1
        encoded.append((bits[-1], count))
        print(encoded)
        return


if __name__ == '__main__':

    practice = Practice1()

    practice.launch()
