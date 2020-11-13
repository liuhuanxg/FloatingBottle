#-*-coding:utf-8 -*-

from django.http import HttpResponse
from .models import *
import re
re.compile()

# 添加公交类型
def add_bus_type(request):
    type_list = ["市区普线", "郊区普线", "快速公交", "微循环线", "通勤线路", "快速直达"]
    for type in type_list:
        BusType.objects.create(
            type_name = type
        )
    return HttpResponse("类型添加成功")


# 添加公交车信息
def add_bus(request):
    """
    for i in range(1, 5):
        Bus.objects.create(
            bus_name="快速公交" + str(i) + "线",
            start_time="5:30",
            end_time="21:30",
            money=2,
            status=1,
            city_id=1,
            type_id=3,
        )
    # 添加市区普线
    for i in range(1, 300):
        Bus.objects.create(
            bus_name= str(i)+"路",
            start_time = "5:30",
            end_time = "22:30",
            money = 2,
            status = 1,
            city_id = 1,
            type_id = 1,
        )
    for i in range(804, 999):
        Bus.objects.create(
            bus_name= str(i)+"路",
            start_time = "5:30",
            end_time = "21:30",
            money = 2,
            status = 1,
            city_id = 1,
            type_id = 2,
        )

    for i in range(3, 207):
        Bus.objects.create(
            bus_name="专" + str(i) + "路",
            start_time="5:30",
            end_time="21:30",
            money=2,
            status=1,
            city_id=1,
            type_id=4,
        )
    bus_list = ["356通勤快车", "381通勤快车","397通勤快车", "483通勤快车",
                "356通勤快车657~312联运","676通勤快车",
                "679通勤快车", "通勤东湖港", "通勤向阳", "通勤柴厂屯", "通勤海子角",
                ]
    for i in bus_list:
        Bus.objects.create(
            bus_name=i,
            start_time="5:30",
            end_time="21:30",
            money=2,
            status=1,
            city_id=1,
            type_id=5,
        )
    """
    for i in range(1, 219):
        Bus.objects.create(
            bus_name="快速直达专线" + str(i) ,
            start_time="5:30",
            end_time="21:30",
            money=2,
            status=1,
            city_id=1,
            type_id=6,
        )
    return HttpResponse("车辆添加成功")

def add_site(request):
    """"""
    site_list ="丑子山,丑子山桥,仇庄,仇庄村,仇店,仇店北,仇店南,仇店小学,仓上,仓上小区,仓储库,仓头村,仓房小区,传媒大学,充电站,出水沟,创业路,创业路北站,创业路南口,创业路南站,创新中路,创新路南,邵镇,辛庄,厂桥路口东,厂桥路口南,厂桥路口西,厂洼,厂洼北站,厂洼街东口,采石场地铁,俸伯站,垂杨柳,城乡,城乡大卖场,城关新城,城关新城路口,城关街道办事处,城南嘉园,城南嘉园北,城后街,城外,昌平永安里,昌平涧头村,昌平王庄,昌平白各庄南,昌平肖村,昌平肖村南(御汤山别墅),昌平胡庄,昌平良各庄,昌平西关,昌平西关环岛,昌平西关环岛东,昌平西关环岛北,昌平西关环岛南,昌平西关环岛西,昌平西山口,昌平西营村东,昌平西营村西,昌平西街中路,昌平西马坊,昌平西马坊村东,昌平西马坊村西,昌平豆各庄路南口(七里渠派出所),昌平辛店,昌平辛店村西,昌平陈庄,昌平麦庄,昌平麻峪,昌平鼓楼东街,昌平鼓楼南街北口,昌平鼓楼西街,昌盛园二区东门,昌盛园北口,昌盛园小学,昌盛路,昌金路口,春晖园,春晖园北,春林大街西,春秀路,春秀路北口,春秀路南口,春秀路口北,春秀路小区,曹刘庄东,曹刘村,曹各庄,曹园,曹园工业园,曹园村,曹园逸家小区,曹坨,曹坨村北口,曹官营东站,曹官营西站,曹家坟,曹家庄,曹家房,曹家房西,曹家沟,曹家沟南,曹家路,曹家路东口,曹庄,曹村,曹碾,曹碾东口,曹碾中街,曹碾村,曹碾西口,曹章,曹肖路北口,曹辛庄,曾庄,朝丰家园,朝丰家园北站,朝丰家园南站,朝内小街,朝凤庵村,朝外北街,朝外市场街,朝宗桥北,朝新嘉园,朝来农艺园,朝来农艺园北站,朝来家园,朝来家园东区,朝来家园西区".split(",")
    number =1000097
    print(site_list)
    for i in site_list:
        Site.objects.create(
            site_name=i,
            site_number = number,
            city_id = 1,
        )
        number += 1
    return HttpResponse("站点添加成功")


import random
def add_bus_site(request):
    bus_list = Bus.objects.all()[0:20]
    site_list = Site.objects.all()
    for i in bus_list:
        j = 0
        while j <20:
            site_id = random.choice(site_list).id
            b = BusSite.objects.filter(bus_id=i.id,site_id=site_id)
            if b.exists():
                pass
            else:
                BusSite.objects.create(
                    bus_id = i.id,
                    site_id = site_id,
                    level = j,
                    station_time = random.randint(3,10)
                )
                j+=1
    return HttpResponse("添加成功")

def del_bus_site(request):
    BusSite.objects.all().delete()
    return HttpResponse("删除成功")

