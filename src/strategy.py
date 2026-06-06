from dataclasses import dataclass
from src.detector import analyze_magic_bytes, calculate_shannon_entropy, detect_mime_type
@dataclass
class ExecutionPlan:
    codec: str; level: int; chunk_size: int; store_only: bool
def determine_optimal_strategy(file_path: str, user_mode: str = "auto") -> ExecutionPlan:
    if user_mode == "huffman": return ExecutionPlan(codec="huffman", level=0, chunk_size=1048576, store_only=False)
    det = analyze_magic_bytes(file_path)
    if det in ["gzip", "bz2", "xz", "zstd", "png", "jpeg"]: return ExecutionPlan(codec="store", level=0, chunk_size=0, store_only=True)
    mime = detect_mime_type(file_path); metrics = calculate_shannon_entropy(file_path)
    if metrics["entropy"] > 7.95: return ExecutionPlan(codec="store", level=0, chunk_size=0, store_only=True)
    if user_mode == "fast": return ExecutionPlan(codec="zstd", level=3, chunk_size=1048576, store_only=False)
    if user_mode == "max": return ExecutionPlan(codec="lzma", level=7, chunk_size=1048576, store_only=False)
    is_txt = metrics["text_ratio"] > 0.75 and metrics["entropy"] < 7.6
    if "text" in mime or is_txt or mime in ["application/json", "text/csv"]: return ExecutionPlan(codec="brotli", level=5, chunk_size=4194304, store_only=False)
    if "log" in file_path or metrics["newlines"] > 1000: return ExecutionPlan(codec="zstd", level=7, chunk_size=2097152, store_only=False)
    return ExecutionPlan(codec="zstd", level=5, chunk_size=2097152, store_only=False)