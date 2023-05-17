import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import folium
from folium import plugins
import math


colormap=['#CD5C5C','#D6170F','#FF8278','#FF5D52','#FF392C','#FF1E1A','#FFA69E','#B30C06']

path = r"./traval_gps"
list1=os.listdir(path)

san_map = folium.Map(
    location=[43.88, 125.33],
    zoom_start=10,
    tiles='Stamen Terrain',
    # tiles='http://wprd03.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=7&ltype=10&x={x}&y={y}&z={z}',
    # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
    attr='default')

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
    
for d in list1:
    wgslong=[]
    wpslat=[]

    
    data = pd.read_excel(path+"\\"+d)

    data['long'] = data['long'].fillna(method='bfill')
    data['lat'] = data['lat'].fillna(method='bfill')
    for index,row in data.iterrows():
        i = gcj02towgs84(row["long"],row["lat"])
        wgslong.append(i[0])
        wpslat.append(i[1])
    data['long']=wgslong
    data['lat']=wpslat


    #     修改往返行程经度
    if d=='realworld21.csv':
        data.loc[:data.loc[data['lat']==data['lat'].max()].index[0],'long']=data.loc[:data.loc[data['lat']==data['lat'].max()].index[0],'long']+0.0005
        data.loc[data.loc[data['lat']==data['lat'].max()].index[0]:,'long']=data.loc[data.loc[data['lat']==data['lat'].max()].index[0]:,'long']-0.0005

    c=[]
    b=[]
    for i in range(int(len(data)/1000)):
        c.append(data.loc[i*1000,'long'])#经度
        b.append(data.loc[i*1000,'lat'])#维度

    Lon =c

    Lat =b
    tri = np.array(list(zip(Lat, Lon)))
    
    
#     添加倒雨滴标记点
#     folium.Marker([Lat[0],Lon[0]], popup='<i>highway</i>',tooltip='R'+str(j),icon=folium.Icon(color='lightgreen')).add_to(san_map)
#     folium.Marker([Lat[-1],Lon[-1]], popup='<i>highway</i>',tooltip='R'+str(j),icon=folium.Icon(color='lightgreen')).add_to(san_map)
    
    

    j=d.split('_')[0]
    print(j)
#     folium.PolyLine(tri, color='#FF8278',weight=5,opacity=0.7).add_to(san_map)
    #     opacity 修改透明度
    #     行程从上至下为高速、北部快速路、西部快速路、主干路-南四环、主干路-东环城路、主干路-人民大街环线、支路-南岭环线
    if j=='R1':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
    elif j=='R2':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
    elif j=='R3':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
    elif j=='R4':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
    elif j=='R5':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
    elif j=='R6':
        folium.PolyLine(tri, color=colormap[1],weight=5,opacity=0.7).add_to(san_map)
#     elif j=='R0':
    else:
        folium.PolyLine(tri, color='#009bb5',weight=5,opacity=0.7).add_to(san_map)
#     elif j=='R8':
#         folium.PolyLine(tri, color='#A52A2A',weight=5,opacity=0.7).add_to(san_map)

san_map.save('map_colors.html')
