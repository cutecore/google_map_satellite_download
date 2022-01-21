#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import requests
import numpy as np
import threading


def checkdir(dir, m3u8_file, drm_key_file, output_dir, decrypt_dir):
    if not os.path.exists(dir):
        print('error: 目录不存在')
        sys.exit(-1)
    if not os.path.exists(m3u8_file):
        print('error: m3u8文件不存在')
        sys.exit(-1)
    if not os.path.exists(drm_key_file):
        print('error: drm_key文件不存在')
        sys.exit(-1)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(decrypt_dir):
        os.mkdir(decrypt_dir)


def getDrmKey(drm_key_file):
    with open(drm_key_file, "br") as f:
        drm_key = f.readline().hex().upper()
        return drm_key


def getFileCout(m3u8_file):
    with open(m3u8_file, "r") as f:
        count_line = f.readlines()
        count_line = count_line[-2]
        count = int(count_line.split("_")[2].split(".")[0]) + 1
        return count


def buildUrl(url_base, count):
    urls = []
    for i in range(0, count):
        # https://stc001.dmm.com/digital/st1:jH2T1hW80bMyCLTEoc1W1RbWddenfRArSTGD9WGsgJMlnfWuS0z8QeHwwYymKXcvcuXjJ3CwD81tjGLK6wPAbkqyBqP5NioTGf8yzpwnXII=/k22OwYLUa6Bua06d7GsUV4-0effd5ea5d3bcb3bb17781646b717b7d1642747279/-/media_b2000000_656.ts
        url = url_base + "media_b6000000_{x}.ts".format(x=i)
        urls.append(url)
    return urls


def download(file_name, url):
    proxies = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809"
    }
    response = requests.get(url, proxies=proxies)
    with open(file_name, "wb") as code:
        code.write(response.content)


def toMp4(concat_file_list, ts_decrypt_dir, output_dir):
    with open(concat_file_list, "w+") as f:
        for i in range(0, count):
            file = ts_decrypt_dir + "media_b6000000_{x}.ts".format(x=i)
            line = "file '{file}'\n".format(file=file)
            f.write(line)
    output_file = output_dir + "output.mp4"
    ffmpeg_cmd = "ffmpeg -f concat -safe 0 -i {concat_file_list} -c copy {output_file}".\
        format(concat_file_list=concat_file_list, output_file=output_file)
    os.system(ffmpeg_cmd)


def temp():
    



class myThread (threading.Thread):
    def __init__(self, array,output_dir):
        threading.Thread.__init__(self)
        self.array = array

    def run(self):
        for url in self.array:
            filename = output_dir + url.split('-')[2]
            download(filename,url)


if __name__ == '__main__':
    if(2 != len(sys.argv)):
        print('python save.py dir')
        sys.exit(-1)
    else:
        dir = sys.argv[1]
        m3u8_file = dir + "/chunklist_b6000000.m3u8"
        drm_key_file = dir + "/drm_iphone"
        decrypt_dir = dir + '/decrypt'
        output_dir = dir + '/output'

        checkdir(dir, m3u8_file, drm_key_file, output_dir, decrypt_dir)
        key = getDrmKey(drm_key_file)
        print(key)
        count = getFileCout(m3u8_file)
        print(count)
        url_base = 'https://stc001.dmm.com/digital/st1:jH2T1hW80bMyCLTEoc1W1RbWddenfRArSTGD9WGsgJMlnfWuS0z8QeHwwYymKXcvcuXjJ3CwD81tjGLK6wPAbkqyBqP5NioTGf8yzpwnXII=/k22OwYLUa6Bua06d7GsUV4-0effd5ea5d3bcb3bb17781646b717b7d1642747279/-/'
        urls = buildUrl(url_base, count)
        # print(urls)
        # urlArraySplit = np.array_split(np.array(urls), 16)
        # threads = []
        # for item in urlArraySplit:
        #     thread = myThread(item,output_dir)
        #     thread.start()
        #     threads.append(thread)

        # for thread in threads:
        #     thread.join()

        for i in range(0, count):
            file_name = dir + "/media_b6000000_{x}.ts".format(x=i)
            url = url_base + "media_b6000000_{x}.ts".format(x=i)
            download(file_name, url)

            file_input = file_name
            file_output = output_dir + "/" + "media_b6000000_{x}.ts".format(x=i)
            iv = "%032x" % i
            openssl_cmd = r'D:\OpenSSL-Win64\bin\openssl.exe aes-128-cbc -d -in {file_input} -out {file_output} -K {k} -iv {iv} -nosalt'.\
                format(file_input=file_input, file_output=file_output, iv=iv, k=key)
            print(openssl_cmd)
            os.system(openssl_cmd)

