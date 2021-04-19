"""
Basic Huffman coding demo
"""
from typing import List, Optional
from dataclasses import dataclass

ASCII_MAX = 256


@dataclass
class HuffmanNode:
    """ A node in a Huffman tree. """
    value: Optional[str]
    freq: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None


def construct_frequency_table(string: str) -> List[Optional[HuffmanNode]]:
    """
    Creates a list where the index is the character code and the value is a
    Huffman node for that character.
    :param string: The string to be encoded
    :return: a list of HuffmanNodes
    """
    frequency_table: List[Optional[HuffmanNode]] = [None] * ASCII_MAX

    for char in string:
        node = frequency_table[ord(char)] or HuffmanNode(char, 0)
        node.freq += 1
        frequency_table[ord(char)] = node

    return frequency_table


def construct_huffman_tree(frequency_table: List[HuffmanNode]) -> HuffmanNode:
    """
    Constructs the Huffman tree given a frequency table.
    :param frequency_table: Frequency table
    :return: Root node of the Huffman tree
    """
    queue: List[HuffmanNode] = sorted(
            [node for node in frequency_table if node],
            key=lambda node: node.freq
    )
    node_queue: List[HuffmanNode] = []

    while len(queue) + len(node_queue) > 1:
        first = _popmin(queue, node_queue)
        second = _popmin(queue, node_queue)
        node = HuffmanNode(None, first.freq + second.freq, first, second)
        node_queue.append(node)

    return node_queue[0]


def _popmin(list1: List[HuffmanNode], list2: List[HuffmanNode]) -> HuffmanNode:
    """
    Given two sorted lists with at least 1 combined, returns the minimum node.
    :param list1: The first list
    :param list2: The second list
    :return: The minimum HuffmanNode
    """
    assert len(list1) + len(list2) > 0
    if not list1 or list2 and list2[0].freq < list1[0].freq:
        return list2.pop(0)
    return list1.pop(0)


def construct_dict(
        node: Optional[HuffmanNode],
        dictionary: List[Optional[List[bool]]]=None,
        prefix: List[bool]=None
    ) -> List[Optional[List[bool]]]:
    """
    Recursively constructs the encoding dictionary.
    :param node: The HuffmanNode being traversed
    :param dictionary: The current dictionary being created during traversal
    :param prefix: The prefix for this Huffman node
    :return: A list where each index corresponse to a character code and the
             value is the Huffman sequence for that character
    """
    if not dictionary or not prefix:
        dictionary = [None] * ASCII_MAX
        prefix = []

    if node is None:
        return dictionary

    if node.value:
        dictionary[ord(node.value)] = prefix

    dictionary = construct_dict(node.left, dictionary, [*prefix, False])
    dictionary = construct_dict(node.right, dictionary, [*prefix, True])
    return dictionary


def encode(string: str, dictionary: List[Optional[List[bool]]]) -> List[bool]:
    """
    Encodes a string using Huffman encoding.
    :param string: The string to encode
    :param dictionary: The dictionary to use for encoding
    :return: A list of booleans representing the Huffman encoding of the input
             string
    """
    out: List[bool] = []
    for char in string:
        sequence = dictionary[ord(char)]
        out += sequence
    return out


def decode(bit_list: List[bool], root: HuffmanNode) -> str:
    """
    Decodes a string encoded using Huffman coding.
    :param bit_list: A list of booleans
    :param root: The root node of the Huffman tree
    :return: The decoded string
    """
    string = ""
    curr_node: Optional[HuffmanNode] = root
    for bit in bit_list:
        curr_node = curr_node.right if bit else curr_node.left

        if curr_node.value:
            string += curr_node.value
            curr_node = root

    return string


def bool_list_to_str(bool_list: List[bool]) -> str:
    """
    Returns the binary string representation of a list of booleans.
    :param bool_list: The input list of booleans
    :return: A string with 0 for False and 1 for True
    """
    return "".join(["1" if char else "0" for char in bool_list])


def main():
    """
    Entrypoint function
    """
    string = input("Enter a string to encode: ")
    print()

    frequency_table = construct_frequency_table(string)
    root_node = construct_huffman_tree(frequency_table)
    dictionary = construct_dict(root_node)

    bit_list = encode(string, dictionary)
    decoded = decode(bit_list, root_node)

    # Print output
    print("Dictionary:")
    for index, sequence in enumerate(dictionary):
        if dictionary[index]:
            print(chr(index), bool_list_to_str(sequence))
    print()

    original_bits = len(string.encode("ascii")) * 8
    print("Encoded: ", bool_list_to_str(bit_list))
    print("Encoded length (bits): ", len(bit_list))
    print("Decoded: ", decoded)
    print("Decoded length (bits): ", original_bits)
    print("Compression ratio: ", float(len(bit_list)) / original_bits)
