import heapq

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [Node(symbol, freq) for symbol, freq in frequency.items()]
    heapq.heapify(heap)
    steps = []
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        node = Node(None, lo.freq + hi.freq, lo, hi)
        steps.append(lo.freq + hi.freq)
        heapq.heappush(heap, node)
    return heapq.heappop(heap), steps

def generate_huffman_codes(node, code='', codes={}):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = code
    generate_huffman_codes(node.left, code + '0', codes)
    generate_huffman_codes(node.right, code + '1', codes)
    return codes

def print_huffman_tree(node, level=0, prefix='', suffix=''):
    if node is None:
        return
    if node.char is not None:
        print('   ' * level + prefix + str(node.char) + suffix)
    else:
        print_huffman_tree(node.left, level + 1, prefix='└─L─') 
        print_huffman_tree(node.right, level + 1, prefix='└─R─')

# Замініть значення у словнику freq на свої власні значення.
freq = {
    "A": 0.29,
    "B": 0.15,
    "C": 0.14,
    "D": 0.10,
    "E": 0.10,
    "F": 0.09,
    "G": 0.08,
    "H": 0.04,
    "I": 0.01
}

huff_tree, steps = build_huffman_tree(freq)
print("Step".ljust(10) + "Sum")
for i, step in enumerate(steps):
    print(str(i+1).ljust(10) + str(step))

print("\nHuffman Codes:")
print_huffman_tree(huff_tree)

codes = generate_huffman_codes(huff_tree)
print("\nSymbol".ljust(10) + "Code")
for symbol, code in codes.items():
    print(symbol.ljust(10) + code)
