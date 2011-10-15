"""
Lyle Scott III
lyle@digitalfoo.net
http://www.digitalfoo.net

CREDITS 
This program was written by reading 'DES Algorithm Illustrated' over and over 
and over. Thanks for this! 
-- http://orlingrabbe.com/des.htm
-- by J. Orlin Grabbe
"""

# print DEBUG messages
DEBUG = True


PC1 = [57,  49,  41,  33,  25,  17,   9,
        1,  58,  50,  42,  34,  26,  18,
       10,   2,  59,  51,  43,  35,  27,
       19,  11,   3,  60,  52,  44,  36,
       63,  55,  47,  39,  31,  23,  15,
        7,  62,  54,  46,  38,  30,  22,
       14,   6,  61,  53,  45,  37,  29,
       21,  13,   5,  28,  20,  12,   4]

PC2 = [14,  17,  11,  24,   1,   5,
       3,   28,  15,   6,  21,  10,
       23,  19,  12,   4,  26,   8,
       16,   7,  27,  20,  13,   2,
       41,  52,  31,  37,  47,  55,
       30,  40,  51,  45,  33,  48,
       44,  49,  39,  56,  34,  53,
       46,  42,  50,  36,  29,  32]

LSHIFT_MAP = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2,  2, 2, 2, 1]

IP = [58,   50,  42,  34,  26,  18,  10,   2,
      60,   52,  44,  36,  28,  20,  12,   4,
      62,   54,  46,  38,  30,  22,  14,   6,
      64,   56,  48,  40,  32,  24,  16,   8,
      57,   49,  41,  33,  25,  17,   9,   1,
      59,   51,  43,  35,  27,  19,  11,   3,
      61,   53,  45,  37,  29,  21,  13,   5,
      63,   55,  47,  39,  31,  23,  15,   7]

E = [32,   1,   2,   3,   4,   5,
      4,   5,   6,   7,   8,   9,
      8,   9,  10,  11,  12,  13,
     12,  13,  14,  15,  16,  17,
     16,  17,  18,  19,  20,  21,
     20,  21,  22,  23,  24,  25,
     24,  25,  26,  27,  28,  29,
     28,  29,  30,  31,  32,   1]

SBOXES = {0:
            [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
             [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
             [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
             [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
          1:
            [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
             [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
             [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
             [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
          2:
            [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
             [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
             [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
             [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
          3:
            [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
             [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
             [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
             [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
          4:
            [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
             [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
             [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
             [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
          5:
            [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
             [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
             [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
             [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
          6:
            [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
             [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
             [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
             [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
          7:
            [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
             [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
             [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
             [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]}

P = [16,   7,  20,  21,
     29,  12,  28,  17,
      1,  15,  23,  26,
      5,  18,  31,  10,
      2,   8,  24,  14,
     32,  27,   3,   9,
     19,  13,  30,   6,
     22,  11,   4,  25]

IP_INV = [[40,   8,  48,  16,  56,  24,  64,  32],
          [39,   7,  47,  15,  55,  23,  63,  31],
          [38,   6,  46,  14,  54,  22,  62,  30],
          [37,   5,  45,  13,  53,  21,  61,  29],
          [36,   4,  44,  12,  52,  20,  60,  28],
          [35,   3,  43,  11,  51,  19,  59,  27],
          [34,   2,  42,  10,  50,  18,  58,  26],
          [33,   1,  41,   9,  49,  17,  57,  25]]


def hex_to_64binary(hexstr):
    """convert a hex string to a 64 bit wide binary number"""
    print_broken_str('hex', hexstr)

    int64 = long(hexstr, 16)
    print_broken_str('int64', int64)
    bin64 = str(bin(int64))[2:].rjust(64, '0')
    print_broken_str('bin64', bin64)

    return bin64


def print_broken_str(label, value, break_at=None):
    """print a label/value pair and insert a space in the value at break_at
    intervals
    """
    if not DEBUG: 
        return
    if break_at == None:
        s = value
    else:
        s = ''
        for i in xrange(0, len(value), break_at):
            for ii in xrange(break_at):
                s += str(value[i+ii])
            s += ' '
    print '%s: %s\n' % (label.ljust(10), s),


def lshift(c, d, iteration):
    """left shift bits; append knocked off bit to end of string"""
    for i in xrange(LSHIFT_MAP[iteration]):
        c = '%s%s' % (c[1:], c[0])
        d = '%s%s' % (d[1:], d[0])
    return (c, d)


def permutate(permutation, in_bits, out_bits_wide):
    """Map the bits contained within in_bits to a new bit string out_bits 
    according to some permutation.
    
    The values are mapped via:
        1)
        2) 
    """
    out_bits = [-1] * out_bits_wide
    for i in xrange(len(permutation)):
        in_bits_i = permutation[i] - 1        
        out_bits[i] = in_bits[in_bits_i]
    return ''.join(map(str, out_bits))        


def xor(bits1, bits2):
    """xor bits1 bit string with bits2 bit string; also used for 2bit addition.
    
    Truth Table for XOR (think of T=1 and F=0...)
    T T = F 
    T F = T
    F T = T
    F F = F
    """
    bits = []

    for i in xrange(len(bits1)):
        b1 = int(bits1[i])
        b2 = int(bits2[i])
        xor_bit = int(bool(b1) ^ bool(b2))
        bits.append(xor_bit)

    return ''.join(map(str, bits))


def main():
    # message
    m = hex_to_64binary('0123456789ABCDEF')
    print_broken_str('M', m, 4)

    # key
    k = hex_to_64binary('133457799BBCDFF1')
    print_broken_str('K', k, 8)

    # initial permutation of message
    ip = permutate(IP, m, 64)
    print_broken_str('IP', ip, 8)
    
    middle = len(ip) / 2
    l = ip[:middle]
    r = ip[middle:]
    print_broken_str('l', l, 4)
    print_broken_str('r', r, 4)

    # apply PC1 permutation to the key and split in half to form c and d
    cd = permutate(PC1, k, 56)
    middle = len(cd) / 2
    c = cd[:middle]
    d = cd[middle:]
    print_broken_str('cd:', cd, 7)
    print_broken_str('c0:', c, 7)
    print_broken_str('d0:', d, 7)

    # loop 16 'rounds'
    for round_i in xrange(16):
        print '-'*80
        
        # left shift the bits of c and d
        (c, d) = lshift(c, d, round_i)
        print_broken_str('c%d' % (round_i+1), c, 7)
        print_broken_str('d%d' % (round_i+1), d, 7)

        # apply PC2 permutation
        k = permutate(PC2, c+d, 48)
        print_broken_str('k%d' % (round_i+1), k, 6)

        # apply E permutation
        e = permutate(E, r, 48)
        print_broken_str('E(R%d)' % (round_i), e, 6)

        # xor k with e (2 bit addition)
        x = xor(k, e)
        print_broken_str('xor(K%d,E(R%d)' % (round_i+1, round_i), x, 6)

        # apply SBOX permutations to blocks of 6 values of the result of the 
        # previous XOR.
        s = []
        for n in xrange(len(x) / 6):
            start = 6 * n
            end = (6 * n) + 6
            b = x[start:end]
            i = int(b[0])*2**1 + int(b[-1])*2**0
            j = (int(b[1])*2**3 + int(b[2])*2**2 +
                 int(b[3])*2**1 + int(b[4])*2**0)
            s.append(str(bin(SBOXES[n][i][j]))[2:].rjust(4, '0'))
        s = ''.join(s)
        print_broken_str('S%d' % (round_i+1), s, 4)

        # apply P permutation.
        f = permutate(P, s, 32)
        print_broken_str('f%d' % (round_i+1), f, 4)

        # save value of l to calculate r (because the r bits have to get 
        # shifted into l before we calculate the new r)
        l_prev = l

        # shift r into l (both 32 bits)
        l = r
        print_broken_str('L%s' % (round_i+1), l, 4)

        # the new 32 bits of r are the saved value of l XORed/added to the value
        # of f
        r = xor(l_prev, f)
        print_broken_str('R%d' % (round_i+1), r, 4)


if __name__ == '__main__':
    main()
