import math
import os
import requests


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


def core():
    point_lt = Point(119.647057, 26.950660)
    point_rb = Point(119.6510056, 26.9422439)
    z = 17
    x1, y1 = lonlat2xyz(point_lt.lon, point_lt.lat, z)
    x2, y2 = lonlat2xyz(point_rb.lon, point_rb.lat, z)
    print(x1, y1, z)
    print(x2, y2, z)
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            download(i, j, z, r"C:\Users\cutec\Desktop\map")


if __name__ == '__main__':
    core()
