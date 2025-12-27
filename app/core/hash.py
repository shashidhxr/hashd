import hashlib
from pathlib import Path
from typing import Union

BUFFER_SIZE = 1024 * 1024       # 1MB chunks

# process in streaming(no OOM risk)

def sha256_file(path: Union[str, Path]) -> str:
    hash = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            hash.update(chunk)

    return hash.hexdigest() 