# -*- coding: utf-8 -*-

import argparse
import csv
import json
import os
import re
import string
from datetime import datetime, timezone

import requests

LETTERS = string.digits + string.ascii_lowercase


class Plurk:
    def __init__(self, nick_name: str, file_format: list = None):
        """Plurk downloader

        Args:
            nick_name (str): Plurk user's nick name
            file_format (str, optional): Output file format. Can be txt/json/csv. Defaults to "txt".
        """
        self.user_id = self._get_user_id(nick_name)
        self.format = ["txt"] if file_format is None else file_format
        # set offset to now for first time
        self.offset = format_time_to_offset(datetime.utcnow())
        self.plurks = {}

    def download(self, filename):
        """download plurks to file"""

        res = self.get_plurks()
        while res:
            self.parse_plurks(res)
            res = self.get_plurks()

        for ext in self.format:
            with open(f"{filename}.{ext}", "w") as f:
                self._writer(f, self.plurks, ext)

    def permalink(self, plurk_id: int) -> str:
        """get permalink from plurk_id"""
        return f"https://www.plurk.com/p/{to_base36(plurk_id)}"

    def get_plurks(self):
        """user_id,  plurk user id
        offset, get plurks before this time
        only_user = 1, get only this user's plurks, no replurk
        plurk only return 20 plurks once"""
        print("Get Plurks...offset=" + self.offset)
        postdata = {"user_id": self.user_id, "offset": self.offset, "only_user": "1"}
        r = requests.post("https://www.plurk.com/TimeLine/getPlurks", data=postdata)
        json_result = r.json()

        if "error" in json_result:
            if json_result["error"] == "NoReadPermissionError":
                print("This is a private timeline.")
        elif "plurks" in json_result and not json_result["plurks"]:
            print("Get Plurks...End")
        else:
            return json_result

    def parse_plurks(self, response_json):
        """parse response json and write to file"""
        plurks = response_json["plurks"]

        for plurk in plurks:
            self.plurks[plurk["plurk_id"]] = {
                "posted": plurk["posted"],
                "content": plurk["content"],
                "content_raw": plurk["content_raw"],
                "response_count": plurk["response_count"],
                "link": self.permalink(plurk["plurk_id"]),
            }

        self.offset = format_time_to_offset(parse_time(plurks[-1]["posted"]))

    def _get_user_id(self, nick_name):
        """parse html to get user_id"""
        r = requests.get("https://www.plurk.com/" + nick_name)
        regex = r'"user_id"\:\s(\d+)'
        match = re.search(regex, r.text)
        user_id = match.group(1)
        return user_id

    def _writer(self, f, plurks: dict, format: str):
        """write content to file"""
        if format == "txt":
            i = 0
            for k, v in plurks.items():
                post_time = change_timezone_local(v["posted"])
                plurk_content = v["content_raw"].replace("\r\n", " ").replace("\n", " ")

                i += 1
                f.write(f"{i:05d}=={k}=={post_time}=={plurk_content}=={v['link']}\n")

        elif format == "json":
            json.dump(plurks, f, ensure_ascii=False, indent=2)

        elif format == "csv":
            writer = csv.writer(f)
            writer.writerow(
                [
                    "plurk_id",
                    "posted",
                    "content",
                    "content_raw",
                    "response_count",
                    "link",
                ]
            )
            for k, v in plurks.items():
                writer.writerow(
                    [
                        k,
                        v["posted"],
                        escape_newlines(v["content"]),
                        escape_newlines(v["content_raw"]),
                        v["response_count"],
                        v["link"],
                    ]
                )


def parse_time(time):
    """parse original time from plurk
    e.g. 'Sat, 11 Jan 2020 01:14:29 GMT' string to datetime
    """
    return datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")


def format_time_to_offset(time):
    """change time to plurk offset format
    e.g. datetime to '2020-01-11T01:14:29.000Z' string
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def change_timezone_local(time):
    """change datetime to local time string"""
    time = parse_time(time)
    local_time = time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def reverse_file(filename):
    """reverse txt file contents with index"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines.reverse()

        index = 0
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                index += 1
                # replace numbers start of line with index
                line = re.sub(r"^\d+", f"{index:05d}", line)
                f.write(line)


def to_base36(n: int) -> str:
    """Convert positive integer to base 36 string.

    Ref: https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    """
    digits = []

    while n:
        digits.append(LETTERS[n % 36])
        n = n // 36

    digits.reverse()

    return "".join(digits)


def escape_newlines(text):
    return text.replace("\n", "\\n").replace("\r", "\\r")


def main(args):
    filename = args.filename if args.filename else args.username
    plurk = Plurk(args.username, args.file_format)
    plurk.download(filename)

    if args.reverse and "txt" in args.file_format and os.path.exists(f"{filename}.txt"):
        reverse_file(filename)

    print("Done!!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download plurk timeline.")
    parser.add_argument("-u", "--username", help="plurk username", required=True)
    parser.add_argument("-o", "--filename", help="output filename")
    parser.add_argument("-r", "--reverse", help="reverse order", action="store_true")
    parser.add_argument(
        "-f",
        "--file-format",
        help="output file format",
        choices=["txt", "csv", "json"],
        action="append",
        required=True,
    )

    args = parser.parse_args()
    main(args)
