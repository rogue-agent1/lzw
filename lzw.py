#!/usr/bin/env python3
"""lzw - LZW compression and decompression."""
import sys

def lzw_compress(data):
    if not data:
        return []
    dictionary = {bytes([i]): i for i in range(256)}
    next_code = 256
    result = []
    w = bytes([data[0]])
    for i in range(1, len(data)):
        c = bytes([data[i]])
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = next_code
            next_code += 1
            w = c
    result.append(dictionary[w])
    return result

def lzw_decompress(codes):
    if not codes:
        return b""
    dictionary = {i: bytes([i]) for i in range(256)}
    next_code = 256
    result = bytearray(dictionary[codes[0]])
    w = dictionary[codes[0]]
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = w + w[:1]
        else:
            raise ValueError(f"Invalid code: {code}")
        result.extend(entry)
        dictionary[next_code] = w + entry[:1]
        next_code += 1
        w = entry
    return bytes(result)

def test():
    data = b"TOBEORNOTTOBEORTOBEORNOT"
    compressed = lzw_compress(data)
    assert len(compressed) < len(data)
    decompressed = lzw_decompress(compressed)
    assert decompressed == data
    data2 = b"ABABABABAB"
    c2 = lzw_compress(data2)
    assert lzw_decompress(c2) == data2
    assert lzw_compress(b"") == []
    assert lzw_decompress([]) == b""
    single = b"A"
    assert lzw_decompress(lzw_compress(single)) == single
    binary = bytes(range(256)) * 2
    assert lzw_decompress(lzw_compress(binary)) == binary
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("lzw: LZW compression. Use --test")
