# codecs
import numpy as np

class Codec():
    
    def __init__(self):
        self.name = 'binary'
        # self.delimiter = '00100011' # a hash symbol '#'
        self.delimiter = '00000011' # a hash symbol ETX (end of text)

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            binary.append(byte)
            if byte == self.delimiter:
                break
        text = ''
        for byte in binary:
            text += chr(int(byte,2))       
        return text 

class CaesarCypher(Codec):

    def __init__(self, shift=3):
        super(CaesarCypher, self).__init__()
        self.name = 'caesar'
        self.delimiter = format((ord('#')+shift)%256, "08b")
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        if type(text) == str:
            return ''.join([format((ord(i)+self.shift)%self.chars, "08b") for i in text])
        else:
            print('Format error')
    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    def decode(self, data):
        binary = []
        for i in range(0, len(data), 8):
            byte = data[i: i + 8]
            if byte == self.delimiter:
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr((int(byte, 2) - self.shift) % self.chars) # undo the shifting
        return text

    # a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    
    def __init__(self):
        super(HuffmanCodes, self).__init__()
        self.nodes = None
        self.name = 'huffman'
        self.codes_set = {} # store the codes of each char
        self.delimiter = '#' # the delimiter

    # make a Huffman Tree    
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
            
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq+right.freq, left.symbol+right.symbol,
                        left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val):
        next_val = val + node.code
        if(node.left):
            self.traverse_tree(node.left, next_val)
        if(node.right):
            self.traverse_tree(node.right, next_val)
        if(not node.left and not node.right):
            # print(f"{node.symbol}->{next_val}") # this is for debugging
            self.codes_set[str(node.symbol)] = next_val # use a dict to store the codes of each char

    # convert text into binary form
    def encode(self, text):
        if type(text) == str:
            # if self.nodes is None, then make a tree
            if self.nodes is None:
                # first count the frequency of each character
                data = {}
                for i in text:
                    if i in data.keys():
                        data[i] += 1
                    else:
                        data[i] = 1
                self.nodes = self.make_tree(data)
                # then traverse it to find codes
                self.traverse_tree(self.nodes[0], '')
            return ''.join([self.codes_set[i] for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        text = ''
        fake_root = self.nodes[0]
        for i in data:
            if i == '0':
                fake_root = fake_root.left # traverse the left-child tree
            elif i == '1':
                fake_root = fake_root.right # traverse the right-child tree
            if fake_root.left is None and fake_root.right is None: # reach the leaf node, then record the char
                if fake_root.symbol == self.delimiter:
                    break
                text += fake_root.symbol
                fake_root = self.nodes[0]  # return to the root of the tree and start a new traversing
        return text

# driver program for codec classes
if __name__ == '__main__':
    text = 'Casino Royale 10:30 Order martini'
    print('Original:', text)

    c = Codec()
    binary = c.encode(text)
    print('Binary:',binary)
    data = c.decode(binary)
    print('Text:',data)

    cc = CaesarCypher()
    binary = cc.encode(text)
    print('Binary:',binary)
    data = cc.decode(binary)
    print('Text:',data)

    h = HuffmanCodes()
    binary = h.encode(text)
    print('Binary:',binary)
    data = h.decode(binary)
    print('Text:',data)  
