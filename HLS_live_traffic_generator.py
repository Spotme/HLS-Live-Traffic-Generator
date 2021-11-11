#!/usr/bin/env python3

# MIT License
# Copyright (c) 2021 SpotMe S.A
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib.parse
import requests
import urllib
import os
import sys
import os
import threading
import time
from random import uniform


def download_segments(
        download_folder,
        variant_url_list,
        segment_list,
        host,
        thread_num,
        variant_number):
    f = open(download_folder + variant_url_list[int(variant_number)], "r")
    variant_file_content_lines = (f.read()).splitlines()
    for line in variant_file_content_lines:
        if ".ts" in line:
            if line not in segment_list:
                segment_list.append(line)
                variant_dir = os.path.dirname(variant_url_list[1])
                urllib.request.urlretrieve(
                    host + "/" + variant_dir + "/" + line,
                    download_folder + "/" + variant_dir + "/" + line)
                sys.stdout.write(".")
                sys.stdout.flush()
    return segment_list


def download_variant_file(
        variant_url_list,
        download_folder,
        host,
        variant_number):
    segment_url = variant_url_list[int(variant_number)]
    variant_folder = download_folder + os.path.dirname(segment_url)
    if not os.path.exists(variant_folder):
        os.makedirs(variant_folder)
    sys.stdout.write("*")
    sys.stdout.flush()
    urllib.request.urlretrieve(
        host + "/" + segment_url,
        variant_folder + "/" + segment_url)


def download_thread(
        number_of_segments,
        variant_url_list,
        download_folder,
        host,
        thread_num,
        variant_number):
    segment_list = []
    i = 0
    while i != int(number_of_segments):
        time.sleep(5)
        download_variant_file(
            variant_url_list,
            download_folder,
            host,
            variant_number)
        segment_list = download_segments(
            download_folder,
            variant_url_list,
            segment_list,
            host,
            thread_num,
            variant_number)
        i = len(segment_list)


def get_variant_urls(master_playlist_contents):
    lns = master_playlist_contents.splitlines()
    variant_url_list = []
    for ln in lns:
        if ln != '' and (not (ln).startswith("#")):
            variant_url_list.append(ln)
    return variant_url_list


def main(
        url,
        download_folder,
        number_of_segments,
        number_of_threads,
        variant_number):
    host = os.path.dirname(url)
    master_playlist_filename = os.path.basename(url)
    print("Fetching master playlist...")
    urllib.request.urlretrieve(url, download_folder + master_playlist_filename)
    with open(download_folder + master_playlist_filename) as f:
        master_playlist_contents = f.read()
    variant_url_list = get_variant_urls(master_playlist_contents)
    print(f"Starting threads({number_of_threads})...")

    # Start threads
    threads = []
    for i in range(int(number_of_threads)):
        t1 = threading.Thread(
            target=download_thread,
            args=(
                number_of_segments,
                variant_url_list,
                download_folder +
                str(i) +
                "/",
                host,
                i,
                variant_number))
        threads.append(t1)
        time.sleep(uniform(0.0, 3.0))
        t1.start()

    # Wait for threads to finish
    for x in threads:
        x.join()
    print("\n")


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 5:
        main(args[1], args[2], args[3], args[4], args[5])
    else:
        print(
            "Usage: ’,’python3', args[0], ‘m3u8_url’, ‘local_download_folder’,‘number_of_video_segments_to_download’,‘number_of_threads’,‘variant_number")
