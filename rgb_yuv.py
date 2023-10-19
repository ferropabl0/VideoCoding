import numpy as np
import ffmpeg
import imageio as iio


def rgb_yuv(rgb):
    y = 0.29900*rgb[0] + 0.58700*rgb[1] + 0.11400*rgb[2]    # Reference: https://www.cs.sfu.ca/mmbook/programming_
                                                            # assignments/additional_notes/rgb_yuv_note/RGB-YUV.pdf
    u = 0.492*(rgb[2]-y)
    v = 0.877*(rgb[0]-y)
    yuv = [y, u, v]
    return yuv


def resize_img(img):
    (
        ffmpeg
        .input(img)
        .filter('scale', width=320, height=-1)
        .output('output_resized_messi.jpg')
        .run()
    )
    return

def serpentine(dct_blocks):     # Expected: 64 blocks, 8x8
    scan = [1, 2, 9, 17, 10, 3, 4, 11, 18, 25, 33, 26, 19, 12, 5, 6, 13, 20, 27, 34, 41, 49, 42, 35, 28, 21, 14,
            7, 8, 15, 22, 29, 36, 43, 50, 57, 58, 51, 44, 37, 30, 23, 16, 24, 31, 38, 45, 52, 59, 60, 53, 46, 39,
            32, 40, 47, 54, 61, 62, 55, 48, 56, 63, 64]
    for el in scan:
        print(dct_blocks[el-1])
    return

def compress_bw(img):
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

    # Task 1
    # rgb_color = [255, 255, 255]
    # yuv_color = rgb_yuv(rgb_color)
    # print(yuv_color)

    # Task 2
    # image_name = 'messi.jpg'
    # resize_img(image_name)

    # Task 3
    # blocks = [['000000'], ['000001'], ['000010'], ['000011'], ['000100'], ['000101'], ['000110'], ['000111'],
    #          ['001000'], ['001001'], ['001010'], ['001011'], ['001100'], ['001101'], ['001110'], ['001111'],
    #          ['010000'], ['010001'], ['010010'], ['010011'], ['010100'], ['010101'], ['010110'], ['010111'],
    #          ['011000'], ['011001'], ['011010'], ['011011'], ['011100'], ['011101'], ['011110'], ['011111'],
    #          ['100000'], ['100001'], ['100010'], ['100011'], ['100100'], ['100101'], ['100110'], ['100111'],
    #          ['101000'], ['101001'], ['101010'], ['101011'], ['101100'], ['101101'], ['101110'], ['101111'],
    #          ['110000'], ['110001'], ['110010'], ['110011'], ['110100'], ['110101'], ['110110'], ['110111'],
    #          ['111000'], ['111001'], ['111010'], ['111011'], ['111100'], ['111101'], ['111110'], ['111111']]
    #serpentine(blocks)

    # Task 4
    image_name = 'messi.jpg'
    compress_bw(image_name)

