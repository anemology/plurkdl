# plurkdl

Download specific user's plurks from [plurk.com](https://www.plurk.com).

## Usage

```bash
usage: plurkdl.py [-h] -u USERNAME [-f FILENAME] [-r]

Download plurk timeline.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        plurk username
  -f FILENAME, --filename FILENAME
                        output filename
  -r, --reverse         reverse order
```

### Example

```python
python -m pip install -r requirements.txt
python plurkdl.py --username plurkwork --filename plurkwork.txt --reverse
```

`reverse` is a optional parameter. It will reverse the line order, default is newest first.

## TODO

[ ] Output file format: csv/json  
[ ] Add url on every plurk

## Changelog

### v1.2.0 - 2022-02-26

Change command line parameters, see `Usage` for details.

### v1.1 - 2020-07-04

Add optional parameter `reverse` to reverse order.

### v1.0 - 2020-01-29

First Version
