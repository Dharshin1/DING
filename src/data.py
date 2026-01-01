import os
import hashlib
import time
import gzip
import bz2
import lzma

try:
    import zstd
except ImportError:
    zstd = None

try:
    import lz4.frame as lz4f
except ImportError:
    lz4f = None


DING_DIR = ".ding"


def init(path):
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        print(f"Error: path does not exist: {abs_path}")
        return

    if not os.path.isdir(abs_path):
        print(f"Error: not a directory: {abs_path}")
        return

    ding_path = os.path.join(abs_path, DING_DIR)
    objects_path = os.path.join(ding_path, "objects")

    if os.path.exists(ding_path):
        print("It is already a ding repository")
        return

    os.mkdir(ding_path)
    os.mkdir(objects_path)
    print(f"Initialisied a ding repo in {ding_path}")


def repo_path():
    cwd = os.getcwd()

    while True:
        ding_path = os.path.join(cwd, DING_DIR)

        if os.path.exists(ding_path):
            return cwd

        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent

    return None


def compress_raw(data):
    return data


def compress_gzip(data):
    return gzip.compress(data, compresslevel=6)


def compress_bz2(data):
    return bz2.compress(data, compresslevel=9)


def compress_lzma(data):
    return lzma.compress(data, preset=6)


def compress_zstd(data):
    if not zstd:
        raise RuntimeError("zstd not installed")
    return zstd.ZSTD_compress(data, 6)
    


def compress_lz4(data):
    if not lz4f:
        raise RuntimeError("lz4 not installed")
    return lz4f.compress(data)


ALGORITHMS = {
    "raw": compress_raw,
    "gzip": compress_gzip,
    "bz2": compress_bz2,
    "lzma": compress_lzma,
}

if zstd:
    ALGORITHMS["zstd"] = compress_zstd

if lz4f:
    ALGORITHMS["lz4"] = compress_lz4


def hash_objects(args):
    repo = repo_path()
    if repo is None:
        print("error: not inside a ding repository")
        return

    ding_path = os.path.join(repo, DING_DIR)
    objects_path = os.path.join(ding_path, "objects")
    os.makedirs(objects_path, exist_ok=True)

    filename = args.file
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"error: file not found: {filename}")
        return

    original_size = len(content)
    oid = hashlib.sha256(content).hexdigest()

    print(f"\nFile hash: {oid}")
    print(f"Original size: {original_size} bytes\n")

    results = []

    for name, compressor in ALGORITHMS.items():
        start = time.perf_counter()
        compressed = compressor(content)
        elapsed = time.perf_counter() - start

        compressed_size = len(compressed)
        ratio = compressed_size / original_size

        obj_name = f"{name}-{oid}"
        obj_path = os.path.join(objects_path, obj_name)

        with open(obj_path, "wb") as f:
            f.write(compressed)

        results.append((name, elapsed, compressed_size, ratio))

    print("Algorithm | Time (ms) | Size (bytes) | Ratio")
    print("-" * 50)
    for name, t, size, ratio in results:
        print(f"{name:8} | {t*1000:8.2f} | {size:12} | {ratio:.3f}")

