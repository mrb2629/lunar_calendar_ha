"""Platform for sensor."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as ha_dt
import datetime

# Import thu vien bat buoc
try:
    from lunardate import LunarDate
    LUNAR_DATE_AVAILABLE = True
except ImportError:
    LUNAR_DATE_AVAILABLE = False

# Constants cho Can Chi
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


# ==========================================================
# 1. HAM THIET LAP BAT BUOC (async_setup_entry)
# ==========================================================
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensor platform."""
    if LUNAR_DATE_AVAILABLE:
        async_add_entities([LunarDateSensor()])
    else:
        async_add_entities([LunarDateErrorSensor()])


# ==========================================================
# 2. CLASS SENSOR CHINH (Tinh toan Lich Am)
# ==========================================================
class LunarDateSensor(SensorEntity):
    """Lunar Date Sensor using lunardate for backend calculation."""

    _attr_name = "Ngay Am Lich"
    _attr_icon = "mdi:calendar-star"
    _attr_unique_id = "lunar_calendar_date_sensor"

    _state: StateType = None
    _attributes: dict = {}

    def __init__(self):
        self.update()

    @property
    def state(self) -> StateType:
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        return self._attributes

    def update(self) -> None:
        now_utc = ha_dt.utcnow()
        now_local = ha_dt.as_local(now_utc)
        today = now_local.date()

        lunar_day = "N/A"
        lunar_month = "N/A"
        can_chi_year = "N/A"
        can_chi_month = "N/A"
        can_chi_day = "N/A"
        note = "Loi khong xac dinh."

        try:
            lunar_today = LunarDate.fromSolarDate(today.year, today.month, today.day)

            lunar_day_num = lunar_today.day
            lunar_month_num = lunar_today.month
            lunar_year_num = lunar_today.year

            lunar_day = str(lunar_day_num)
            lunar_month = str(lunar_month_num)

            # Bảng ánh xạ Can năm -> Can tháng Giêng (index)
            CAN_START_MONTH = {
                0: 2,  # Giáp -> Bính
                5: 2,  # Kỷ  -> Bính
                1: 4,  # Ất  -> Mậu
                6: 4,  # Canh -> Mậu
                2: 6,  # Bính -> Canh
                7: 6,  # Tân  -> Canh
                3: 8,  # Đinh -> Nhâm
                8: 8,  # Nhâm -> Nhâm
                4: 0,  # Mậu  -> Giáp
                9: 0   # Quý  -> Giáp
            }

            # Can Chi nam
            can_index_year = (lunar_year_num + 6) % 10
            chi_index_year = (lunar_year_num + 8) % 12
            can_chi_year = f"{CAN[can_index_year]} {CHI[chi_index_year]}"

            note = 'Tinh toan bang lunardate (Backend).'

            # Can Chi thang
            chi_index_month = (lunar_month_num + 1) % 12
            start_can = CAN_START_MONTH[can_index_year]
            can_index_month = (start_can + lunar_month_num - 1) % 10
            can_chi_month = f"{CAN[can_index_month]} {CHI[chi_index_month]}"

            # Can Chi ngay
            def jd_from_date(d):
                a = (14 - d.month) // 12
                y = d.year + 4800 - a
                m = d.month + 12 * a - 3
                jd = d.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
                return jd

            jd = jd_from_date(today)
            can_index_day = (jd + 9) % 10
            chi_index_day = (jd + 1) % 12
            can_chi_day = f"{CAN[can_index_day]} {CHI[chi_index_day]}"
            
            # 7. Tinh Can Chi gio
            current_hour = now_local.hour
            chi_index_hour = ((current_hour + 1) // 2) % 12
            can_index_hour = (can_index_day * 2 + chi_index_hour) % 10
            can_chi_hour = f"{CAN[can_index_hour]} {CHI[chi_index_hour]}"


        except Exception as e:
            lunar_day = "Error"
            lunar_month = "Error"
            can_chi_year = "Error"
            can_chi_month = "Error"
            can_chi_day = "Error"
            note = f"Loi runtime tong quat: {type(e).__name__}"

        self._state = lunar_day
        self._attributes = {
            'lunar_day_num': lunar_day,
            'lunar_month_num': lunar_month,
			'Gio Am lich': can_chi_hour,
			'Ngay Am lich': can_chi_day,
			'Thang Am lich': can_chi_month,
            'Nam Am lich': can_chi_year,     
            'Ghi chu': note,
        }


# ==========================================================
# 3. CLASS SENSOR BAO LOI (Fallback)
# ==========================================================
class LunarDateErrorSensor(SensorEntity):
    _attr_name = "Lich Am Loi"
    _attr_icon = "mdi:alert-circle"
    _attr_unique_id = "lunar_calendar_error_sensor"
    _attr_state = "Loi Cai Dat"
    _attr_extra_state_attributes = {
        'Ghi chu': 'Khong the import thu vien lunardate. Vui long kiem tra log va HACS.'
    }
