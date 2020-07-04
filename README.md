# plurkdl

Download specific user's plurks from [plurk.com](https://www.plurk.com).

## Usage

### Linux

```python
python -m pip install requests
# python plurkdl.py {username} {filename} {reverse}
python plurkdl.py plurkwork plurkwork.txt y
```

`reverse` is a optional parameter. It will reverse the line order, default is newest first.

### Windows

Download `.exe` from [release](https://github.com/anemology/plurkdl/release) and run in commandline.

```bat
plurkdl.exe plurkwork plurkwork.txt y
```

## Changelog

### v1.1 - 2020-07-04

Add optional parameter `reverse` to reverse order.

### v1.0 - 2020-01-29

First Version
