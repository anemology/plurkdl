# plurkdl

Download specific user's plurks from [plurk.com](https://www.plurk.com).

## Usage

```bash
usage: plurkdl.py [-h] -u USERNAME [-o FILENAME] [-r] -f {txt,csv,json}

Download plurk timeline.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        plurk username
  -o FILENAME, --filename FILENAME
                        output filename
  -r, --reverse         reverse order
  -f {txt,csv,json}, --file-format {txt,csv,json}
                        output file format
```

### Example

```python
python -m pip install -r requirements.txt
python plurkdl.py --username plurkwork -f txt -f json -f csv
```

`reverse` is a optional parameter for txt. It will reverse the line order, default is newest first.

## TODO

- [x] Output file format: csv/json  
- [x] Add url on every plurk
- [ ] Download resources, such as emoticons, avatars, images etc.
- [ ] Download response.
- [ ] Output file format: html, like [backup](https://www.plurk.com/settings/backup) from plurk website.

## Changelog

### v1.3.0 - 2022-05-15

Add support to save content as json and csv.

### v1.2.0 - 2022-02-26

Change command line parameters, see `Usage` for details.

### v1.1 - 2020-07-04

Add optional parameter `reverse` to reverse order.

### v1.0 - 2020-01-29

First Version
