# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography:
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        # self.delimiter = '#'
        self.delimiter = chr(int('00000011',2))
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        # print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if self.codec is None or self.codec.name is not codec:
            if codec == 'binary':
                self.codec = Codec()
            elif codec == 'caesar':
                self.codec = CaesarCypher()
            elif codec == 'huffman':
                self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter) # the delimiter should be added in, raw code misses this

        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message + self.delimiter
            self.binary = binary
            cv2.imwrite(fileout, self.modify_pixels(image, binary))

    @staticmethod
    def modify_pixels(image, binary):
        image_shape = image.shape
        image = image.ravel()
        for i, code in enumerate(binary):
            last_bit = 1-(image[i]-1)%2 # get the last bit of R(G or B) component of the pixel
            if last_bit == int(code): # the last bit is the same as we need, just skip it
                continue
            else: # the last bit is not the same as we need, so add one.
                if image[i] == 255: # pay attention here, if the bit is 255, we subtract one instead
                    image[i] -= 1
                else:
                    image[i] += 1
        return image.reshape(image_shape)

    def decode(self, filein, codec):
        image = cv2.imread(filein)
        # print(image) # for debugging

        # convert into text
        if codec == 'binary':
            self.codec = Codec()
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec is None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                return
        binary_data = self.extract_binary(image)
        message = self.codec.decode(binary_data)
        # update the data attributes:
        self.text = message + self.delimiter # huffman needs to code delimiter
        self.binary = self.codec.encode(self.text) # just encode the text again to get binary

    @staticmethod
    def extract_binary(image):
        binary = ''
        image = image.ravel()
        for i in image:
            last_bit = 1 - (i - 1) % 2 # get the last bit of R(G or B) component of the pixel
            binary += str(last_bit)
        return binary

    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)

    def txt(self):
        if self.text == '':
            print("The message is not set.")
        else:
            with open('DECODE.txt', 'w', encoding="utf-8") as f:
                f.write(self.text)
            print("Decoded to DECODE.txt!")
            print("Text message:", self.text)
            print("Binary message:", self.binary)

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

