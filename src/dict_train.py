import os, random, pathlib
import zstandard as zstd
def train_zstd_dictionary(samples_dir: str, pattern: str = "*.log", dict_size: int = 114688) -> str | None:
    bp = pathlib.Path(samples_dir); paths = list(bp.glob(pattern))
    if not paths: return None
    samples = []
    for p in paths:
        try:
            b = p.read_bytes()
            if len(b) < 1024: samples.append(b)
            else:
                for _ in range(min(10, len(b) // 4096)):
                    idx = random.randrange(0, len(b) - 4096); samples.append(b[idx : idx + 4096])
        except IOError: continue
    if not samples: return None
    bd = zstd.train_dictionary(dict_size, samples); path = os.path.join("src", f"zstd_trained_{dict_size}.dict")
    with open(path, "wb") as f: f.write(bd.as_bytes())
    return path