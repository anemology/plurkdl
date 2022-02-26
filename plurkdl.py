# -*- coding: utf-8 -*-

import argparse
import datetime
import re
from datetime import timezone

import requests


class Plurk:
    def __init__(self, nick_name):
        self.user_id = self._get_user_id(nick_name)
        self.plurk_index = 0
        # set offset to now for first time
        self.offset = format_time_to_offset(datetime.datetime.now())

    def download(self, filename):
        """download plurks to file"""
        f = open(filename, "w")
        response_json = self.get_plurks()
        while response_json:
            self.parse_plurks(response_json, f)
            response_json = self.get_plurks()
        f.close()

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

    def parse_plurks(self, response_json, f):
        """parse response json and write to file"""
        plurks = response_json["plurks"]
        
        for plurk in plurks:
            post_time = change_timezone_local(plurk["posted"])
            plurk_content = plurk["content_raw"].replace("\n", " ")

            self.plurk_index += 1
            f.write(f"{self.plurk_index:05d}=={post_time}=={plurk_content}\n")

        self.offset = format_time_to_offset(parse_time(plurks[-1]["posted"]))

    def _get_user_id(self, nick_name):
        """parse html to get user_id"""
        r = requests.get("https://www.plurk.com/" + nick_name)
        regex = r'"user_id"\:\s(\d+)'
        match = re.search(regex, r.text)
        user_id = match.group(1)
        return user_id


def parse_time(time):
    """parse original time from plurk
    e.g. 'Sat, 11 Jan 2020 01:14:29 GMT' string to datetime
    """
    return datetime.datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")


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
    """reverse file contents with index"""
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


def main(args):
    filename = args.filename if args.filename else f"{args.username}.txt"
    plurk = Plurk(args.username)
    plurk.download(filename)

    if args.reverse:
        reverse_file(filename)

    print("Done!!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download plurk timeline.")
    parser.add_argument("-u", "--username", help="plurk username", required=True)
    parser.add_argument("-f", "--filename", help="output filename")
    parser.add_argument("-r", "--reverse", help="reverse order", action="store_true")

    args = parser.parse_args()
    main(args)
