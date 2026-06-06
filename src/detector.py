import math
import mimetypes
from collections import Counter
MAGIC_SIGNATURES = {b"\x1f\x8b": "gzip", b"\x42\x5a\x68": "bz2", b"\xfd\x37\x7a\x58\x5a\x00": "xz", b"\x28\xb5\x2f\xfd": "zstd", b"\xff\xd8\xff": "jpeg", b"\x89PNG\r\n\x1a\n": "png"}
def analyze_magic_bytes(file_path: str) -> str | None:
    try:
        with open(file_path, "rb") as f: header = f.read(16)
        for sig, codec in MAGIC_SIGNATURES.items():
            if header.startswith(sig): return codec
    except IOError: return None
    return None
def calculate_shannon_entropy(file_path: str, sample_size: int = 262144) -> dict:
    try:
        with open(file_path, "rb") as f: buffer = f.read(sample_size)
        if not buffer: return {"entropy": 0.0, "text_ratio": 0.0, "newlines": 0}
        total = len(buffer); freq = Counter(buffer)
        entropy = -sum((c / total) * math.log2(c / total) for c in freq.values())
        text_bytes = sum(32 <= b <= 126 or b in (9, 10, 13) for b in buffer)
        return {"entropy": entropy, "text_ratio": text_bytes / total, "newlines": buffer.count(b"\n")}
    except IOError: return {"entropy": 0.0, "text_ratio": 0.0, "newlines": 0}
def detect_mime_type(file_path: str) -> str:
    mime, _ = mimetypes.guess_type(file_path)
    return mime or "application/octet-stream"