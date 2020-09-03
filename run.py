#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:53
@Auther  : Jarrett
@FileName: run
@Software: PyCharm
"""

# 各种API接口
# https://lab.isaaclin.cn/nCoV/api/area?latest=0
#https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/05-30-2020.csv
# https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
# https://coronavirus.jhu.edu/map.html
# https://experience.arcgis.com/experience/685d0ace521648f8a5beeeee1b9125cd
# https://lab.isaaclin.cn/nCoV/
# 有效https://lab.isaaclin.cn/nCoV/api/provinceName?lang=zh


import numpy as np
import pandas as pd
import json
import requests
import jsonpath
from pyecharts.charts import Map
from pyecharts import options as opts

def GetChinaData():
    """
    获取中国的数据
    :return:
    """
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist' # 需要更换api
    response = requests.post(url).text
    resp = json.loads(response)  # 使用变量resp来接收字典格式的数据
    for data in resp['data']:  # 遍历提取每个国家的疫情数据
        name = data['name']  # 国家名
        confirm = data['confirm']  # 该国家疫情人数
        dead = data['dead']
        heal = data['heal']
        nowConfirm = data['nowConfirm']
        confirmCompare = data['confirmCompare']
        nowConfirmCompare = data['nowConfirmCompare']
        healCompare = data['healCompare']
        deadCompare = data['deadCompare']
        # print(name, confirm, dead,heal, nowConfirm, confirmCompare, nowConfirmCompare, healCompare, deadCompare)
    return data

def GetWorldData():
    """
    绘制世界地图！
    :return:
    """
    # 1.目标网站
    url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    # 2.请求资源
    resp = requests.get(url)
    # 3.提取数据
    # 类型转换 json-->dict
    data = json.loads(resp.text)
    print(data)
    name = jsonpath.jsonpath(data, "$..name")       # 国家名
    confirm = jsonpath.jsonpath(data, "$..confirm")     # 确诊人数
    dead = jsonpath.jsonpath(data, "$..dead")       # 死亡人数
    nowConfirm = jsonpath.jsonpath(data, "$..nowConfirm")       # 现存确诊人数
    confirmCompare = jsonpath.jsonpath(data, "$..confirmCompare")   # 新增确诊
    healCompare = jsonpath.jsonpath(data, "$..healCompare")     # 新增治愈
    deadCompare = jsonpath.jsonpath(data, "$..deadCompare")     # 新增死亡

    # 以下内容参考 http://gallery.pyecharts.org/#/Map/README
    c = (
        Map()
            .add("确诊人数", [list(z) for z in zip(name, confirm)], "world", name_map = nameMap,
                 is_map_symbol_show = False)
            .add("死亡人数", [list(z) for z in zip(name, dead)], "world", name_map=nameMap,
                 is_map_symbol_show=False)
            .add("现存确诊", [list(z) for z in zip(name, nowConfirm)], "world", name_map=nameMap,
                 is_map_symbol_show=False)
            .add("新增确诊", [list(z) for z in zip(name, confirmCompare)], "world", name_map=nameMap,
                 is_map_symbol_show=False)
            .add("新增治愈", [list(z) for z in zip(name, healCompare)], "world", name_map=nameMap,
                 is_map_symbol_show=False)
            .add("新增死亡", [list(z) for z in zip(name, deadCompare)], "world", name_map=nameMap,
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2019-nCoV 世界地图"),
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                        pieces=[
                        {"min":50000,"label":'>50000',"color":"#893448"},
                        {"min":10000,"max":49999,"label":'10000-49999',"color":"#ff585e"},
                        {"min":5000,"max":9999,"label":'5000-9999',"color":"#FB8146"},
                        {"min":1000,"max":4999,"label":'1000-4999',"color":"#ffa500"},
                        {"min":100,"max":999,"label":'100-999',"color":"#ffb248"},
                        {"min":0,"max":99,"label":'0-99',"color":"#fff2d1"},
                        ]),
        )
            .render("map_world.html")
    )
    print('successful')
    return True

# 世界各个国家的名称映射表
nameMap = {
        'Singapore Rep.':'新加坡',
        'Dominican Rep.':'多米尼加',
        'Palestine':'巴勒斯坦',
        'Bahamas':'巴哈马',
        'Timor-Leste':'东帝汶',
        'Afghanistan':'阿富汗',
        'Guinea-Bissau':'几内亚比绍',
        "Côte d'Ivoire":'科特迪瓦',
        'Siachen Glacier':'锡亚琴冰川',
        "Br. Indian Ocean Ter.":'英属印度洋领土',
        'Angola':'安哥拉',
        'Albania':'阿尔巴尼亚',
        'United Arab Emirates':'阿联酋',
        'Argentina':'阿根廷',
        'Armenia':'亚美尼亚',
        'French Southern and Antarctic Lands':'法属南半球和南极领地',
        'Australia':'澳大利亚',
        'Austria':'奥地利',
        'Azerbaijan':'阿塞拜疆',
        'Burundi':'布隆迪',
        'Belgium':'比利时',
        'Benin':'贝宁',
        'Burkina Faso':'布基纳法索',
        'Bangladesh':'孟加拉国',
        'Bulgaria':'保加利亚',
        'The Bahamas':'巴哈马',
        'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
        'Belarus':'白俄罗斯',
        'Belize':'伯利兹',
        'Bermuda':'百慕大',
        'Bolivia':'玻利维亚',
        'Brazil':'巴西',
        'Brunei':'文莱',
        'Bhutan':'不丹',
        'Botswana':'博茨瓦纳',
        'Central African Rep.':'中非',
        'Canada':'加拿大',
        'Switzerland':'瑞士',
        'Chile':'智利',
        'China':'中国',
        'Ivory Coast':'象牙海岸',
        'Cameroon':'喀麦隆',
        'Dem. Rep. Congo':'刚果民主共和国',
        'Congo':'刚果',
        'Colombia':'哥伦比亚',
        'Costa Rica':'哥斯达黎加',
        'Cuba':'古巴',
        'N. Cyprus':'北塞浦路斯',
        'Cyprus':'塞浦路斯',
        'Czech Rep.':'捷克',
        'Germany':'德国',
        'Djibouti':'吉布提',
        'Denmark':'丹麦',
        'Algeria':'阿尔及利亚',
        'Ecuador':'厄瓜多尔',
        'Egypt':'埃及',
        'Eritrea':'厄立特里亚',
        'Spain':'西班牙',
        'Estonia':'爱沙尼亚',
        'Ethiopia':'埃塞俄比亚',
        'Finland':'芬兰',
        'Fiji':'斐',
        'Falkland Islands':'福克兰群岛',
        'France':'法国',
        'Gabon':'加蓬',
        'United Kingdom':'英国',
        'Georgia':'格鲁吉亚',
        'Ghana':'加纳',
        'Guinea':'几内亚',
        'Gambia':'冈比亚',
        'Guinea Bissau':'几内亚比绍',
        'Eq. Guinea':'赤道几内亚',
        'Greece':'希腊',
        'Greenland':'格陵兰',
        'Guatemala':'危地马拉',
        'French Guiana':'法属圭亚那',
        'Guyana':'圭亚那',
        'Honduras':'洪都拉斯',
        'Croatia':'克罗地亚',
        'Haiti':'海地',
        'Hungary':'匈牙利',
        'Indonesia':'印度尼西亚',
        'India':'印度',
        'Ireland':'爱尔兰',
        'Iran':'伊朗',
        'Iraq':'伊拉克',
        'Iceland':'冰岛',
        'Israel':'以色列',
        'Italy':'意大利',
        'Jamaica':'牙买加',
        'Jordan':'约旦',
        'Japan':'日本',
        'Japan':'日本本土',
        'Kazakhstan':'哈萨克斯坦',
        'Kenya':'肯尼亚',
        'Kyrgyzstan':'吉尔吉斯斯坦',
        'Cambodia':'柬埔寨',
        'Korea':'韩国',
        'Kosovo':'科索沃',
        'Kuwait':'科威特',
        'Lao PDR':'老挝',
        'Lebanon':'黎巴嫩',
        'Liberia':'利比里亚',
        'Libya':'利比亚',
        'Sri Lanka':'斯里兰卡',
        'Lesotho':'莱索托',
        'Lithuania':'立陶宛',
        'Luxembourg':'卢森堡',
        'Latvia':'拉脱维亚',
        'Morocco':'摩洛哥',
        'Moldova':'摩尔多瓦',
        'Madagascar':'马达加斯加',
        'Mexico':'墨西哥',
        'Macedonia':'马其顿',
        'Mali':'马里',
        'Myanmar':'缅甸',
        'Montenegro':'黑山',
        'Mongolia':'蒙古',
        'Mozambique':'莫桑比克',
        'Mauritania':'毛里塔尼亚',
        'Malawi':'马拉维',
        'Malaysia':'马来西亚',
        'Namibia':'纳米比亚',
        'New Caledonia':'新喀里多尼亚',
        'Niger':'尼日尔',
        'Nigeria':'尼日利亚',
        'Nicaragua':'尼加拉瓜',
        'Netherlands':'荷兰',
        'Norway':'挪威',
        'Nepal':'尼泊尔',
        'New Zealand':'新西兰',
        'Oman':'阿曼',
        'Pakistan':'巴基斯坦',
        'Panama':'巴拿马',
        'Peru':'秘鲁',
        'Philippines':'菲律宾',
        'Papua New Guinea':'巴布亚新几内亚',
        'Poland':'波兰',
        'Puerto Rico':'波多黎各',
        'Dem. Rep. Korea':'朝鲜',
        'Portugal':'葡萄牙',
        'Paraguay':'巴拉圭',
        'Qatar':'卡塔尔',
        'Romania':'罗马尼亚',
        'Russia':'俄罗斯',
        'Rwanda':'卢旺达',
        'W. Sahara':'西撒哈拉',
        'Saudi Arabia':'沙特阿拉伯',
        'Sudan':'苏丹',
        'S. Sudan':'南苏丹',
        'Senegal':'塞内加尔',
        'Solomon Is.':'所罗门群岛',
        'Sierra Leone':'塞拉利昂',
        'El Salvador':'萨尔瓦多',
        'Somaliland':'索马里兰',
        'Somalia':'索马里',
        'Serbia':'塞尔维亚',
        'Suriname':'苏里南',
        'Slovakia':'斯洛伐克',
        'Slovenia':'斯洛文尼亚',
        'Sweden':'瑞典',
        'Swaziland':'斯威士兰',
        'Syria':'叙利亚',
        'Chad':'乍得',
        'Togo':'多哥',
        'Thailand':'泰国',
        'Tajikistan':'塔吉克斯坦',
        'Turkmenistan':'土库曼斯坦',
        'East Timor':'东帝汶',
        'Trinidad and Tobago':'特里尼达和多巴哥',
        'Tunisia':'突尼斯',
        'Turkey':'土耳其',
        'Tanzania':'坦桑尼亚',
        'Uganda':'乌干达',
        'Ukraine':'乌克兰',
        'Uruguay':'乌拉圭',
        'United States':'美国',
        'Uzbekistan':'乌兹别克斯坦',
        'Venezuela':'委内瑞拉',
        'Vietnam':'越南',
        'Vanuatu':'瓦努阿图',
        'West Bank':'西岸',
        'Yemen':'也门',
        'South Africa':'南非',
        'Zambia':'赞比亚',
        'Zimbabwe':'津巴布韦'
    }


if __name__ == '__main__':
    GetWorldData()

