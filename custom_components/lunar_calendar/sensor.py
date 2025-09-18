"""Platform for sensor."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as ha_dt
import datetime

# --- KHAI BÁO DỮ LIỆU CAN CHI (Giữ nguyên) ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
# Giả định năm 2024 (Dương lịch) là năm Âm lịch Giáp Thìn (năm thứ 4721)
# 4721 % 10 = 1 (Giáp); 4721 % 12 = 5 (Thìn).
LUNAR_YEAR_START = 4721 
# -----------------------------------------------

# Hàm setup chính cho Config Entry
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensor platform."""
    # Khởi tạo và thêm thực thể Sensor
    async_add_entities([LunarDateSensor()])


class LunarDateSensor(SensorEntity):
    """Representation of a Lunar Date Sensor."""

    # Thuộc tính bắt buộc cho HA mới
    _attr_name = "Ngày Âm Lịch"
    _attr_icon = "mdi:calendar-star"
    _attr_unique_id = "lunar_calendar_date_sensor"
    
    # Thiết lập loại lớp thiết bị, tuy không bắt buộc nhưng nên có
    # _attr_device_class = SensorDeviceClass.DATE 
    
    # Thiết lập trạng thái ban đầu
    _state: StateType = None
    _attributes: dict = {}

    def __init__(self):
        """Initialize the sensor."""
        self.update() # Gọi update ngay khi khởi tạo

    @property
    def state(self) -> StateType:
        """Return the state of the sensor (Gregorian Date)."""
        # Trạng thái chính của Sensor: Ngày Dương lịch theo format ISO 8601
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self._attributes

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        today = ha_dt.now().date()
        
        # *** LỖI TIỀM ẨN: CẦN DÙNG THƯ VIỆN CHUYÊN DỤNG CHO CHUYỂN ĐỔI ÂM LỊCH ***
        # Dùng thư viện Lunar-Gregorian đã được cài đặt hoặc tự triển khai logic phức tạp.
        # Nếu chỉ dùng logic Can Chi đơn giản:
        
        gregorian_year = today.year
        
        # Tính Can Chi dựa trên năm Dương lịch (KHÔNG HOÀN TOÀN CHÍNH XÁC VÌ KHÔNG XÉT NGÀY TẾT)
        lunar_year_num = LUNAR_YEAR_START + (gregorian_year - 2024)
        can_chi_year = f"{CAN[(lunar_year_num - 1) % 10]} {CHI[(lunar_year_num - 1) % 12]}"
        
        # CHỖ NÀY CẦN CHUYỂN ĐỔI NGÀY/THÁNG ÂM LỊCH CHÍNH XÁC (Dùng thư viện hoặc logic JS cũ)
        # Ta sẽ giả lập ngày Âm lịch:
        
        # *** MÔ PHỎNG DỮ LIỆU (Giống code JS gốc, nhưng chuyển sang logic Python) ***
        # Để sử dụng lại logic JS gốc, bạn cần cài đặt thư viện V8 hoặc node-runner trong Python, điều này không khả thi.
        # KHẮC PHỤC: Sử dụng thư viện Python như "pylunar" hoặc "lunardate" (cần thêm vào manifest.json requirements)
        
        # MÔ PHỎNG SƠ BỘ:
        lunar_day = "Tạm: XX"
        lunar_month = "Tạm: YY" 
        
        self._state = today.strftime("%Y-%m-%d")
        self._attributes = {
            'lunar_day': lunar_day,
            'lunar_month': lunar_month,
            'lunar_year_can_chi': can_chi_year,
            'date_format_vi': today.strftime("%d/%m/%Y"),
            'Ghi chú': 'Thông tin ngày và tháng Âm lịch cần thư viện Python chuyên dụng để chính xác.',
        }
