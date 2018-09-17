# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from io import BytesIO
import base64


def baseMap():
    # 创建一个地图
    plt.figure(figsize=(14, 7))
    m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45,
                lon_0=100)
    # 把海岸线画上
    m.drawcoastlines()
    m.drawcountries(linewidth=1.5)
    # 中国的省区
    m.readshapefile('D:\python_documents\preemption\static\gadm36_CHN_shp\gadm36_CHN_1', 'states', drawbounds=True)

    # gca就是Get Current Axes的缩写，实际上就是要获得当前图形的座标轴
    ax = plt.gca()
    for nshape, seg in enumerate(m.states):
        # 统一放上红色
        poly = Polygon(seg, facecolor='r')
        ax.add_patch(poly)

    # 加上港澳台
    ax = plt.gca()
    m.readshapefile('./static/gadm36_TWN_shp/gadm36_TWN_0', 'taiwan', drawbounds=True)
    for nshape, seg in enumerate(m.taiwan):
        poly = Polygon(seg, facecolor='r')
        ax.add_patch(poly)

    ax = plt.gca()
    m.readshapefile('./static/gadm36_MAC_shp/gadm36_MAC_0', 'xianggang', drawbounds=True)
    for nshape, seg in enumerate(m.xianggang):
        poly = Polygon(seg, facecolor='r')
        ax.add_patch(poly)

    ax = plt.gca()
    m.readshapefile('./static/gadm36_HKG_shp/gadm36_HKG_0', 'aomen', drawbounds=True)
    for nshape, seg in enumerate(m.aomen):
        poly = Polygon(seg, facecolor='r')
        ax.add_patch(poly)

    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    plt.close()
    return data
