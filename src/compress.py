import os, gzip, bz2, lzma, json, time, hashlib, brotli
import zstandard as zstd
from src.strategy import determine_optimal_strategy
from src.huffman import compress_huffman
def compute_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(1048576): sha256.update(chunk)
    return sha256.hexdigest()
def execute_compression(source_file: str, output_destination: str | None = None, mode: str = "auto") -> dict:
    plan = determine_optimal_strategy(source_file, mode)
    ext_map = {"zstd": ".zst", "brotli": ".br", "gzip": ".gz", "bz2": ".bz2", "lzma": ".xz", "huffman": ".huf", "store": ".store"}
    dst = output_destination or os.path.join("compressed_files", os.path.basename(source_file) + ext_map.get(plan.codec, ".bin"))
    t0 = time.time()
    if plan.store_only or plan.codec == "store":
        with open(source_file, "rb") as fi, open(dst, "wb") as fo:
            while chunk := fi.read(1048576): fo.write(chunk)
    elif plan.codec == "huffman": compress_huffman(source_file, dst)
    elif plan.codec == "zstd":
        c = zstd.ZstdCompressor(level=plan.level)
        with open(source_file, "rb") as fi, open(dst, "wb") as fo: c.copy_stream(fi, fo)
    elif plan.codec == "brotli":
        with open(source_file, "rb") as fi, open(dst, "wb") as fo: fo.write(brotli.compress(fi.read(), quality=plan.level))
    elif plan.codec == "gzip":
        with open(source_file, "rb") as fi, gzip.open(dst, "wb", compresslevel=plan.level) as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    elif plan.codec == "bz2":
        with open(source_file, "rb") as fi, bz2.open(dst, "wb", compresslevel=plan.level) as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    elif plan.codec == "lzma":
        with open(source_file, "rb") as fi, lzma.open(dst, "wb", preset=plan.level) as fo:
            while chunk := fi.read(65536): fo.write(chunk)
    manifest = {"source": source_file, "output": dst, "codec": plan.codec, "level": plan.level, "sha256": compute_sha256(source_file), "orig_bytes": os.path.getsize(source_file), "out_bytes": os.path.getsize(dst), "ratio": round(os.path.getsize(dst)/max(1, os.path.getsize(source_file)), 4), "duration_seconds": round(time.time()-t0, 4)}
    with open(dst + ".dfc.json", "w") as f: json.dump(manifest, f, indent=4)
    return manifest