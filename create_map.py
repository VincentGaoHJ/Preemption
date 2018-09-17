# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 22:07:13 2018

@author: gaoha
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import csv

from io import BytesIO
import base64


def get_province():
    prov_dict = {}
    filename = './static/information.csv'
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        m = 0
        for row in reader:
            if m == 0:
                m += 1
                continue
            prov_dict[row[1][:2]] = row[2]
    return prov_dict


def create_map(your_castle, computer_castle):
    # 创建一个地图
    plt.figure(figsize=(14, 7))
    m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45,
                lon_0=100)
    # 把海岸线画上
    m.drawcoastlines()
    m.drawcountries(linewidth=1.5)
    # 中国的省区
    m.readshapefile('D:\python_documents\preemption\static\gadm36_CHN_shp\gadm36_CHN_1', 'states', drawbounds=True)

    if 'Taiwan' in your_castle:
        color = 'r'
    elif 'Taiwan' in computer_castle:
        color = '#0000ff'
    else:
        color = '#ffffff'
    ax = plt.gca()
    m.readshapefile('./static/gadm36_TWN_shp/gadm36_TWN_0', 'taiwan', drawbounds=True)
    for nshape, seg in enumerate(m.taiwan):
        poly = Polygon(seg, facecolor=color)
        ax.add_patch(poly)

    if 'Hong_Kong' in your_castle:
        color = 'r'
    elif 'Hong_Kong' in computer_castle:
        color = '#0000ff'
    else:
        color = '#ffffff'
    # ax = plt.gca()
    m.readshapefile('./static/gadm36_MAC_shp/gadm36_MAC_0', 'xianggang', drawbounds=True)
    for nshape, seg in enumerate(m.xianggang):
        poly = Polygon(seg, facecolor=color)
        ax.add_patch(poly)

    if 'Macao' in your_castle:
        color = 'r'
    elif 'Macao' in computer_castle:
        color = '#0000ff'
    else:
        color = '#ffffff'
    # ax = plt.gca()
    m.readshapefile('./static/gadm36_HKG_shp/gadm36_HKG_0', 'aomen', drawbounds=True)
    for nshape, seg in enumerate(m.aomen):
        poly = Polygon(seg, facecolor=color)
        ax.add_patch(poly)

    statenames = []
    colors = {}
    prov_dict = get_province()
    print(prov_dict)

    for shapedict in m.states_info:
        statename = shapedict['NL_NAME_1']
        p = statename.split('|')
        if len(p) > 1:
            s = p[1]
        else:
            s = p[0]
        s = s[:2]
        if s == '黑龍':
            s = '黑龙'

        statenames.append(s)
        if prov_dict[s] in your_castle:
            colors[s] = 'r'
        elif prov_dict[s] in computer_castle:
            colors[s] = '#0000ff'
        else:
            colors[s] = '#ffffff'

    # ax = plt.gca()
    for nshape, seg in enumerate(m.states):
        color = colors[statenames[nshape]]
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)

    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    plt.close('all')
    return data
