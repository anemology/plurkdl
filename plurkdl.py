# -*- coding: utf-8 -*-

import requests
import re
import sys
import datetime
from datetime import timezone, timedelta


def get_user_id(nick_name):
    r = requests.get("https://www.plurk.com/" + nick_name)
    # parse html to get user_id
    regex = r"\"user_id\"\:\s(\d+)"
    match = re.search(regex, r.text)
    userid = match.group(1)
    return userid


def get_plurks(user_id, offset):
    """user_id,  plurk user id  
    offset, get plurks before this time  
    only_user = 1, get only this user's plurks, no replurk  
    plurk only return 20 plurks once"""
    print("Get Plurks...offset=" + offset)
    postdata = {"user_id": user_id, "offset": offset, "only_user": "1"}
    r = requests.post("https://www.plurk.com/TimeLine/getPlurks", data=postdata)
    json_result = r.json()

    if "error" in json_result:
        if json_result["error"] == "NoReadPermissionError":
            print("This is a private timeline.")
    elif "plurks" in json_result and not json_result["plurks"]:
        print("Get Plurks...End")
    else:
        return json_result


def parse_plurks(response_json, f):
    """parse response json and write to file"""
    plurks = response_json["plurks"]
    for index, plurk in enumerate(plurks):
        post_time = change_timezone_local(plurk["posted"])
        replaced_newline = " "
        # replaced_newline = "\n                     "
        f.write(
            post_time
            + "=="
            + plurk["content_raw"].replace("\n", replaced_newline)
            + "\n"
        )
        if index == len(plurks) - 1:
            global offset
            offset = format_time_to_offset(parse_time(plurk["posted"]))


def parse_time(time):
    """parse original time from plurk"""
    # Sat, 11 Jan 2020 01:14:29 GMT
    # E, d MMM yyyy HH:mm:ss 'GMT'
    # return datetime.datetime.strptime(time, "%a, %d %b %Y %H:%M:%S GMT")
    return datetime.datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")


def format_time_to_offset(time):
    """change time to plurk offset format"""
    # Sat, 11 Jan 2020 01:14:29 GMT -> 2020-01-11T01:14:29.000Z
    # yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
    return time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def change_timezone_local(time):
    """change to local time"""
    time = parse_time(time)
    local_time = time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    # return str(time.replace(tzinfo=timezone.utc).astimezone(tz=timezone(timedelta(hours=8))))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def main():
    if len(sys.argv) != 3:
        print("Please input two parameters.")
        print(r"python plurkdl.py {username} {filename}")
        print("ex. python plurkdl.py plurkwork result.txt")
        sys.exit(1)

    user_id = get_user_id(sys.argv[1])
    print("User ID=" + user_id)

    # set offset to now for first time
    if "offset" not in globals():
        global offset
        offset = format_time_to_offset(datetime.datetime.now())

    response_json = get_plurks(user_id, offset)
    f = open(sys.argv[2], "w", encoding="utf-8")
    while response_json is not None:
        parse_plurks(response_json, f)
        response_json = get_plurks(user_id, offset)
        pass
    f.close()
    print("Done!!!")


if __name__ == "__main__":
    main()
