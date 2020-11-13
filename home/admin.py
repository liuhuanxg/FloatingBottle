from django.contrib import admin
from .models import User, City, Site, Bus,BusSite, BusType

admin.site.site_header='智能公交管理后台'
admin.site.site_title='智能公交管理后台'


# 城市管理
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["city_name", "city_number"]
    search_fields = ["city_name", "city_number"]
    list_per_page = 30


# 站台管理
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ["site_name", "site_number","city"]
    search_fields = ["site_name", "site_number","city"]
    list_per_page = 50


# 车辆类型管理
@admin.register(BusType)
class BusTypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "add_time",]
    date_hierarchy = "add_time"
    search_fields = ["type_name",]
    list_per_page = 30


# 公交管理
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ["bus_name", "start_time","end_time","money","status","city"]
    search_fields = ["bus_name", "start_time","end_time","money","status","foreign_key__related_city"]
    list_per_page = 50
    list_filter = ["type"]


# 公交-站台管理
@admin.register(BusSite)
class BusSiteAdmin(admin.ModelAdmin):
    list_display = ["bus", "site","level","station_time"]
    list_per_page = 50
    ordering = ["id"]