import pathlib, sys, re
import numpy as np

def get_dims(p: pathlib.Path) -> tuple[int, int, int, int]:
    assert p.exists(), \
            f"ERROR in get_dims({p}): path {p} does not exist."
    assert p.is_file(), \
            f"ERROR in get_dims({p}): path {p} is not a file."
    assert p.name[-9:] == ".4dfp.ifh", \
            f"ERROR in get_dims({p}): {p} is not a 4dfp.ifh file."
    with p.open('r') as f:
        lines = [line for line in f.readlines() if re.match(r'^matrix size', line) != None]
        lines = [int(re.sub(r'.* ([0-9]+)', r'\1', line)[:-1]) for line in lines]
    return tuple(lines)

def get_endianness(p: pathlib.Path) -> str:
    with p.open('r') as header:
        for h in filter(lambda l: re.match(r'^imagedata byte order', l), header):
            endianness = h.split(":=")[1].strip()
            if re.match("^big", endianness):
                return ">"
            break
    return "<"

def load(
        imgroot: str,
        byte_order: int | None = None
        ) -> np.ndarray:
    header_path = pathlib.Path(imgroot+".4dfp.ifh")
    img_path = pathlib.Path(imgroot+".4dfp.img")

    assert img_path.exists(), \
            f"ERROR in load({img_path}): path {img_path} does not exist."
    assert img_path.is_file(), \
            f"ERROR in load({img_path}): path {img_path} is not a file."

    endianness = get_endianness(header_path)
    dims = get_dims(header_path) 
    dsize = sys.getsizeof(np.float32)
    nvoxels = np.prod(dims[0:3]) 
    nframes = 1 if len(dims) < 4 else dims[3]
    bytes_per_frame = dsize * nvoxels
    bytes_to_read = nframes * bytes_per_frame
    temp = np.zeros(bytes_to_read, dtype=np.uint8)
    my_bytes = img_path.read_bytes()
    my_nums = np.ndarray(shape=dims, dtype=f"{endianness}f4", buffer=my_bytes)
    return my_nums
     
