import math
import os
import requests
import numpy as np
import threading


def swap(a, b):
    a, b = b, a
    return a, b


class Point:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


class Box:
    def __init__(self, point_lt, point_rb):
        self.point_lt = point_lt
        self.point_rb = point_rb


def build_url(x, y, z):
    return "http://khms0.google.com/kh/v=893?&x={x}&y={y}&z={z}".format(x=x, y=y, z=z)


def download(x, y, z, path):
    print('[Download]:',x,y,z,path)
    proxies = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809"
    }
    url = build_url(x, y, z)
    response = requests.get(url, proxies=proxies)
    path = path + "\\{z}\\{x}\\".format(z=z, x=x)
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = path + "\\{y}.png".format(y=y)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
    else:
        print("network error!")

class myThread (threading.Thread):
    def __init__(self, array):
        threading.Thread.__init__(self)
        self.array = array
       
    def run(self):
        for i in self.array:
            download(i[0],i[1],i[2],i[3])


def xyz2lonlat(x, y, z):
    n = math.pow(2, z)
    lon = x / n * 360.0 - 180.0
    lat = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat = lat * 180.0 / math.pi
    return lon, lat


def lonlat2xyz(lon, lat, zoom):
    n = math.pow(2, zoom)
    x = ((lon + 180) / 360) * n
    y = (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2 * n
    return int(x), int(y)


def cal_tiff_box(x1, y1, x2, y2, z):
    LT = xyz2lonlat(x1, y1, z)
    RB = xyz2lonlat(x2 + 1, y2 + 1, z)
    return Point(LT[0], LT[1]), Point(RB[0], RB[1])

def downloadPlus(x1, y1, x2, y2, z, path):
    urlArray = [] 
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            urlArray.append([i, j, z, path])
  
    urlArraySplit = np.array_split(np.array(urlArray),16)
    
    threads = []

    for item in urlArraySplit:
        thread = myThread(item)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def core(point_lt,point_rb,path,z):
    x1, y1 = lonlat2xyz(point_lt.lon, point_lt.lat, z)
    x2, y2 = lonlat2xyz(point_rb.lon, point_rb.lat, z)
    print(x1, y1, z)
    print(x2, y2, z)
    print((x2-x1+1) * (y2-y1+1))
    downloadPlus(x1, y1, x2, y2, z, path)
    
if __name__ == '__main__':
    # 存储目录
    path = r"D:\map"
    # 下载范围的 左上点经纬度
    point_lt = Point(116.286476, 40.069985)
    # 下载范围的 右下点经纬度
    point_rb = Point(116.324707 ,40.054938)
    # 开始级别 
    level_start = 16
    # 结束级别
    level_end = 17

    for i in range(level_start,level_end+1):
        core(point_lt,point_rb,path,i)


