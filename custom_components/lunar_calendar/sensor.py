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
    # Kiem tra neu thu vien da duoc cai dat thanh cong
    if LUNAR_DATE_AVAILABLE:
        async_add_entities([LunarDateSensor()])
    else:
        # Trong truong hop loi import nghiem trong
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
        """Initialize the sensor and schedule first update."""
        self.update()

    @property
    def state(self) -> StateType:
        """Return the state of the sensor (Lunar Day)."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self._attributes

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        
        # 1. Lay ngay hien tai theo mui gio dia phuong cua Home Assistant
        now_utc = ha_dt.utcnow()
        now_local = ha_dt.as_local(now_utc)
        today = now_local.date() 

        lunar_day = "N/A"
        lunar_month = "N/A"
        can_chi_year = "N/A"
        note = "Loi khong xac dinh."
        
        try:
            # 2. Tinh toan Lich Am dung lunardate
            lunar_today = LunarDate.fromSolarDate(today.year, today.month, today.day)
            
            # 3. Trich xuat du lieu
            lunar_day = str(lunar_today.day)
            lunar_month = str(lunar_today.month)
            lunar_year_num = lunar_today.year 

            # 4. Tinh Can Chi
            # 4. Tinh Can Chi nam
            can_index = (lunar_year_num + 6) % 10
            chi_index = (lunar_year_num + 8) % 12
            can_chi_year = f"{CAN[can_index]} {CHI[chi_index]} {lunar_year_num}"
            
            note = 'Tinh toan bang lunardate (Backend).'

        except AttributeError as e:
            lunar_day = "Error"
            lunar_month = "Error"
            can_chi_year = "Error"
            note = f"Loi AttributeError: {e}"
        
        except Exception as e:
            lunar_day = "Error"
            lunar_month = "Error"
            can_chi_year = "Error"
            note = f"Loi runtime tong quat: {type(e).__name__}"

        # 5. Cap nhat Trang thai va Thuoc tinh
        self._state = lunar_day # Trang thai chinh la Ngay Am (1-30)
        self._attributes = {
            'lunar_day_num': lunar_day,
            'lunar_month_num': lunar_month,
            'lunar_year_can_chi': can_chi_year,
            'date_format_vi': today.strftime("%d/%m/%Y"),
            'is_full_moon': lunar_day == '15',
            'is_new_moon': lunar_day == '1',
            'Ghi chu': note,
        }

# ==========================================================
# 3. CLASS SENSOR BAO LOI (Fallback)
# ==========================================================
# Tao Sensor phu chi de bao loi neu thu vien lunardate khong load duoc
class LunarDateErrorSensor(SensorEntity):
    _attr_name = "Lich Am Loi"
    _attr_icon = "mdi:alert-circle"
    _attr_unique_id = "lunar_calendar_error_sensor"
    _attr_state = "Loi Cai Dat"
    _attr_extra_state_attributes = {'Ghi chu': 'Khong the import thu vien lunardate. Vui long kiem tra log va HACS.'}

