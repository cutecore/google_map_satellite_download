# google_map_satellite_download

# 0.0 开始
工作中需要使用无偏移的谷歌影像，发现市面上的影像下载工具如bigemap需要付费，或是有水印，
上家公司有影像下载工具，就想自己写一个。不是做GIS，对OpenCV、GDAL、Python也没有深入了解，见谅。
  
简单实现了下面三个功能：

- 支持下载谷歌地图卫星影像散列瓦片
- 支持下载谷歌地图卫星散列瓦片合并为一张png 
- 支持合并后图片转换为geotiff 

# 0.1 注意
需要能访问google服务器，请在代码中配置你的proxy

# 0.2 下载tiff,使用 download_tiff.py

使用download_tiff，便可下载并生成tiff
生成geotiff文件，需要GDAL，[已经编译好的GDAL windows版本](https://www.gisinternals.com/release.php)

# 0.3 下载瓦片,使用 download_tile.py

下载散列瓦片，只需使用download_title.py, 
便可在nginx + leaflet中使用。

# 0.4
```
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
```        




