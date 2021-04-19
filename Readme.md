# Huff
Huffman coding demo
https://en.wikipedia.org/wiki/Huffman_coding

```
$ python3 -m huff
Enter a string to encode: Lorem ipsum dolor sit amet, consectetur adipiscing elit

Dictionary:
  100
, 111010
L 111011
a 01111
c 0100
d 11000
e 1111
g 01110
i 001
l 11001
m 0101
n 11010
o 1010
p 11011
r 0110
s 1011
t 000
u 11100

Encoded:  111011101001101111010110000111011101111100010110011000101011001101001101001011001000100011110101111100011101010001001010110101011111101000001111000111000110100011111100000111011001101101000011101001110100111111001001000
Encoded length (bits):  219
Decoded:  Lorem ipsum dolor sit amet, consectetur adipiscing elit
Decoded length (bits):  440
Compression ratio:  0.49772727272727274
```
