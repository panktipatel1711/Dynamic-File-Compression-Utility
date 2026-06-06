import os, gzip, bz2, lzma, json, brotli
import zstandard as zstd
from src.huffman import decompress_huffman
def execute_decompression(src: str, dst: str | None = None):
    if not dst:
        bn = os.path.basename(src)
        for ext in [".zst", ".br", ".gz", ".bz2", ".xz", ".huf", ".store"]:
            if bn.endswith(ext): bn = bn[:-len(ext)]; break
        dst = os.path.join("decompressed_files", "restored_" + bn)
    if src.endswith(".zst"):
        with open(src, "rb") as fi, open(dst, "wb") as fo: zstd.ZstdDecompressor().copy_stream(fi, fo)
    elif src.endswith(".br"):
        with open(src, "rb") as fi, open(dst, "wb") as fo: fo.write(brotli.decompress(fi.read()))
    elif src.endswith(".gz"):
        with gzip.open(src, "rb") as fi, open(dst, "wb") as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    elif src.endswith(".bz2"):
        with bz2.open(src, "rb") as fi, open(dst, "wb") as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    elif src.endswith(".xz"):
        with lzma.open(src, "rb") as fi, open(dst, "wb") as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    elif src.endswith(".huf"): decompress_huffman(src, dst)
    elif src.endswith(".store"):
        with open(src, "rb") as fi, open(dst, "wb") as fo:
            while chunk := fi.read(65536): fo.write(chunk)
def verify_checksum_integrity(manifest_path: str) -> bool:
    from src.compress import compute_sha256
    with open(manifest_path, "r") as f: m = json.load(f)
    tmp = m["output"] + ".verify.tmp"
    try:
        execute_decompression(m["output"], tmp)
        ok = (compute_sha256(tmp) == m["sha256"])
    finally:
        if os.path.exists(tmp): os.remove(tmp)
    return ok