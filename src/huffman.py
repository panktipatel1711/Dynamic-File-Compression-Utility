import os, heapq, json
class HuffmanNode:
    def __init__(self, byte_val: int | None, frequency: int):
        self.byte_val = byte_val; self.frequency = frequency; self.left = None; self.right = None
    def __lt__(self, other): return self.frequency < other.frequency
def build_frequency_map(file_path: str) -> dict:
    freq = {}
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            for byte in chunk: freq[byte] = freq.get(byte, 0) + 1
    return freq
def construct_huffman_tree(freq_map: dict) -> HuffmanNode | None:
    if not freq_map: return None
    heap = [HuffmanNode(b, f) for b, f in freq_map.items()]; heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap); n2 = heapq.heappop(heap)
        parent = HuffmanNode(None, n1.frequency + n2.frequency); parent.left = n1; parent.right = n2; heapq.heappush(heap, parent)
    return heap[0] if heap else None
def generate_codes_from_tree(root: HuffmanNode, current_code: str, lookup_table: dict):
    if root is None: return
    if root.byte_val is not None: lookup_table[root.byte_val] = current_code; return
    generate_codes_from_tree(root.left, current_code + "0", lookup_table)
    generate_codes_from_tree(root.right, current_code + "1", lookup_table)
def compress_huffman(src_path: str, dst_path: str):
    freq_map = build_frequency_map(src_path); root = construct_huffman_tree(freq_map); lookup_table = {}
    if root: generate_codes_from_tree(root, "", lookup_table)
    header_data = json.dumps({str(k): v for k, v in lookup_table.items()}).encode("utf-8"); header_length = len(header_data)
    with open(src_path, "rb") as fi, open(dst_path, "wb") as fo:
        fo.write(header_length.to_bytes(4, byteorder="big")); fo.write(header_data); bit_accumulator = []
        while chunk := fi.read(65536):
            for byte in chunk:
                for bit in lookup_table[byte]:
                    bit_accumulator.append(int(bit))
                    if len(bit_accumulator) == 8:
                        val = 0
                        for b in bit_accumulator: val = (val << 1) | b
                        fo.write(bytes([val])); bit_accumulator.clear()
        if bit_accumulator:
            pad_len = 8 - len(bit_accumulator); bit_accumulator.extend([0] * pad_len)
            val = 0
            for b in bit_accumulator: val = (val << 1) | b
            fo.write(bytes([val])); fo.write(bytes([pad_len]))
        else: fo.write(bytes([0]))
def decompress_huffman(src_path: str, dst_path: str):
    with open(src_path, "rb") as fi, open(dst_path, "wb") as fo:
        h_len_bytes = fi.read(4)
        if not h_len_bytes: return
        h_len = int.from_bytes(h_len_bytes, byteorder="big"); code_map = json.loads(fi.read(h_len).decode("utf-8"))
        rev_lookup = {v: int(k) for k, v in code_map.items()}; body = fi.read()
        if not body: return
        pad_len = body[-1]; data = body[:-2]; last = body[-2]; bits = []
        for byte in data: bits.append(f"{byte:08b}")
        if pad_len < 8: bits.append(f"{last:08b}"[:-pad_len] if pad_len > 0 else f"{last:08b}")
        buf = ""; out = bytearray()
        for bit in "".join(bits):
            buf += bit
            if buf in rev_lookup: out.append(rev_lookup[buf]); buf = ""
        fo.write(out)