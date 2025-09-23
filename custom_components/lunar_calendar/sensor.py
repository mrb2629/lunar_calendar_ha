"""Lunar Date Sensor for Home Assistant using amlich_hnd.core"""

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as ha_dt
from datetime import timedelta
from .amlich_hnd import core

CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]

HOANG_DAO_HOURS = {
    0: ["Tý","Sửu","Mão","Ngọ","Thân","Dậu"],    # Ngày Tý
    1: ["Dần","Mão","Tỵ","Thân","Tuất","Hợi"],  # Ngày Sửu
    2: ["Tý","Sửu","Thìn","Tỵ","Mùi","Tuất"],   # Ngày Dần
    3: ["Dần","Mão","Ngọ","Thân","Dậu","Hợi"],  # Ngày Mão
    4: ["Dần","Thìn","Tỵ","Thân","Dậu","Hợi"],  # Ngày Thìn
    5: ["Sửu","Dần","Mão","Tỵ","Thân","Tuất"],  # Ngày Tỵ
    6: ["Tý","Sửu","Mão","Ngọ","Thân","Dậu"],   # Ngày Ngọ
    7: ["Dần","Mão","Tỵ","Thân","Tuất","Hợi"],  # Ngày Mùi
    8: ["Tý","Sửu","Thìn","Tỵ","Mùi","Tuất"],   # Ngày Thân
    9: ["Dần","Mão","Ngọ","Thân","Dậu","Hợi"],  # Ngày Dậu
    10:["Dần","Thìn","Tỵ","Thân","Dậu","Hợi"],  # Ngày Tuất
    11:["Sửu","Dần","Mão","Tỵ","Thân","Tuất"],  # Ngày Hợi
}

HOANG_DAO_DAYS = {
    1:["Tý","Sửu","Tỵ","Mùi","Thìn","Tuất"],
    2:["Dần","Mão","Ngọ","Mùi","Dậu","Tý"],
    3:["Thìn","Tỵ","Thân","Dậu","Hợi","Dần"],
    4:["Ngọ","Mùi","Tuất","Hợi","Sửu","Thìn"],
    5:["Thân","Dậu","Tý","Sửu","Mão","Ngọ"],
    6:["Tuất","Hợi","Dần","Mão","Tỵ","Thân"],
    7:["Tý","Sửu","Tỵ","Mùi","Thìn","Tuất"],
    8:["Dần","Mão","Ngọ","Mùi","Dậu","Tý"],
    9:["Thìn","Tỵ","Thân","Dậu","Hợi","Dần"],
    10:["Ngọ","Mùi","Tuất","Hợi","Sửu","Thìn"],
    11:["Thân","Dậu","Tý","Sửu","Mão","Ngọ"],
    12:["Tuất","Hợi","Dần","Mão","Tỵ","Thân"],
}

def get_ngay_hoang_dao_trong_thang(lunar_month,lunar_year,lunar_leap,tz=7):
    start_solar = core.lunar_to_solar(1,lunar_month,lunar_year,lunar_leap,tz)
    if start_solar==(0,0,0): return []
    start_jd = core.jd_from_date(*start_solar)
    cand30 = core.lunar_to_solar(30,lunar_month,lunar_year,lunar_leap,tz)
    if cand30!=(0,0,0):
        jd30 = core.jd_from_date(*cand30)
        month_length = 30 if jd30>start_jd else 29
    else: 
        month_length=29
    hoang=set(HOANG_DAO_DAYS.get(lunar_month,[]))
    res=[]
    for ld in range(1,month_length+1):
        s=core.lunar_to_solar(ld,lunar_month,lunar_year,lunar_leap,tz)
        if s==(0,0,0): continue
        jd_day = core.jd_local_from_date(*s,tz)
        chi=CHI[(jd_day+1)%12]
        if chi in hoang: 
            res.append(ld)
    return res

async def async_setup_entry(hass:HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    async_add_entities([LunarDateSensor()],True)

class LunarDateSensor(SensorEntity):
    _attr_name="Ngày Âm Lịch"
    _attr_icon="mdi:calendar-star"
    _attr_unique_id="lunar_calendar_date_sensor"

    async def async_update(self):
        now=ha_dt.now()
        dd,mm,yy=now.day,now.month,now.year
        tz=7
        lunar_day,lunar_month,lunar_year,lunar_leap=core.solar_to_lunar(dd,mm,yy,tz)
        jd=core.jd_local_from_date(dd,mm,yy,tz)

        # Thêm "N" nếu là tháng nhuận
        lunar_month_display = f"{lunar_month}N" if lunar_leap else str(lunar_month)

        # Năm
        can_year=CAN[(lunar_year+6)%10]; chi_year=CHI[(lunar_year+8)%12]
        can_chi_year=f"{can_year} {chi_year}"
        # Tháng
        chi_month=CHI[(lunar_month+1)%12]
        start_can={0:2,5:2,1:4,6:4,2:6,7:6,3:8,8:8,4:0,9:0}[(lunar_year+6)%10]
        can_month=CAN[(start_can+lunar_month-1)%10]
        can_chi_month=f"{can_month} {chi_month}"
        # Ngày
        can_day=CAN[(jd+9)%10]; chi_day=CHI[(jd+1)%12]
        can_chi_day=f"{can_day} {chi_day}"
        # Giờ
        chi_index_hour=((now.hour+1)//2)%12
        chi_hour=CHI[chi_index_hour]
        can_hour=CAN[((jd+9)%10*2+chi_index_hour)%10]
        can_chi_hour=f"{can_hour} {chi_hour}"

        tinh_chat_ngay="Hoàng đạo" if chi_day in HOANG_DAO_DAYS.get(lunar_month,[]) else "Hắc đạo"
        hoang_hours=HOANG_DAO_HOURS.get((jd+1)%12,[])
        tinh_chat_gio="Hoàng đạo" if chi_hour in hoang_hours else "Hắc đạo"
        lunar_days_in_month=get_ngay_hoang_dao_trong_thang(lunar_month,lunar_year,lunar_leap,tz)

        # --- Thêm phần tính toán ngày âm lịch cho cả tuần ---
        lunar_dates_of_week = {}
        start_of_week = now - timedelta(days=now.weekday()) # Lấy ngày thứ Hai của tuần
        for i in range(7):
            current_day = start_of_week + timedelta(days=i)
            lunar_d, lunar_m, lunar_y, lunar_l = core.solar_to_lunar(current_day.day, current_day.month, current_day.year, tz)
            lunar_m_disp = f"{lunar_m}N" if lunar_l else str(lunar_m)
            lunar_dates_of_week[f"Ngày {i+2}"] = f"{lunar_d}/{lunar_m_disp}"

        # State chính hiển thị đầy đủ ngày/tháng/năm âm lịch
        self._attr_native_value=f"{lunar_day}/{lunar_month_display}/{lunar_year}"

        # Thuộc tính chi tiết
        self._attr_extra_state_attributes={
            "Ngày âm lịch": lunar_day,
            "Tháng âm lịch": lunar_month_display,
            "Năm âm lịch": lunar_year,
            "Can Chi Ngày": can_chi_day,
            "Can Chi Tháng": can_chi_month,
            "Can Chi Năm": can_chi_year,
            "Can Chi Giờ": can_chi_hour,
            "Tính chất ngày hiện tại": tinh_chat_ngay,
            "Tính chất giờ hiện tại": tinh_chat_gio,
            "Danh sách giờ Hoàng đạo": ", ".join(hoang_hours),
            "Danh sách ngày Hoàng đạo trong tháng (âm lịch)": ", ".join(str(x) for x in lunar_days_in_month),
            "Ngày âm lịch tuần này": lunar_dates_of_week
        }
