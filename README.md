# 4dfpy

This is a (very!) simple package for converting the binary data from Avi Snider's 4dfp neuroimaging file format into a Numpy array, that can then be used in your Python scripts.

## Install

```bash
pip install 4dfpy
```

## Running

```python
import 4dfpy

my_4dfp_data = 4dfpy.load("/path/to/myimg")
```

The path to the 4dfp files should **only include the root name** without the
extension (example: "/path/to/myimg.4dfp.img" should instead be "/path/to/myimg").
Make sure the .4dfp.img and .4dfp.hdr files are in the same directory.

[ ] TODO: add support for including file extension
