#!/usr/bin/env python3
"""lzw — LZW compression and decompression. Zero deps."""

def compress(data):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    w = ""
    result = []
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = next_code
            next_code += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def decompress(codes):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    result = [dictionary[codes[0]]]
    w = result[0]
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad code: {code}")
        result.append(entry)
        dictionary[next_code] = w + entry[0]
        next_code += 1
        w = entry
    return ''.join(result)

def main():
    texts = [
        "TOBEORNOTTOBEORTOBEORNOT",
        "ABABABABABABABAB",
        "The quick brown fox jumps over the lazy dog. The quick brown fox jumps again.",
    ]
    for text in texts:
        codes = compress(text)
        decoded = decompress(codes)
        ratio = len(codes) * 12 / (len(text) * 8)  # assuming 12-bit codes
        print(f"Original:     {text[:50]}{'...' if len(text)>50 else ''} ({len(text)} chars)")
        print(f"Compressed:   {len(codes)} codes (ratio: {ratio:.2f})")
        print(f"Decompressed: {'OK ✓' if decoded == text else 'FAIL ✗'}\n")

if __name__ == "__main__":
    main()
