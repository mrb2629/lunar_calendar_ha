# 🌙 Lịch Âm Lịch Việt (Lunar Calendar) cho Home Assistant

Đây là một tích hợp (Integration) và Custom Card cho Home Assistant, giúp hiển thị ngày Âm lịch (Việt Nam/Trung Quốc) và lịch tuần.

## 🚀 Cài Đặt (Qua HACS)

### 1. Thêm Repository

1. Mở HACS trong giao diện Home Assistant.
2. Truy cập **Integrations** (hoặc **Frontend** nếu bạn cài đặt Custom Card).
3. Nhấn vào **ba chấm** góc trên bên phải, chọn **Custom repositories**.
4. **URL Repository:** `https://github.com/mrb2629/lunar_calendar_ha`
5. **Category:** Chọn **Integration**.
6. Nhấn **ADD**.
7. Tìm kiếm và cài đặt **Lịch Âm Lịch Việt**.

### 2. Khởi Động Lại Home Assistant

Sau khi cài đặt, bạn cần khởi động lại Home Assistant.

### 3. Cấu Hình Sensor

1. Vào **Settings** (Cài đặt) -> **Devices & Services** (Thiết bị & Dịch vụ) -> **Integrations** (Tích hợp).
2. Nhấn **+ ADD INTEGRATION** (Thêm tích hợp).
3. Tìm kiếm và chọn **Lịch Âm Lịch Việt**. (Không cần cấu hình, nhấn **FINISH**).

Sensor sẽ được tạo: `sensor.ngay_am_lich` với các thuộc tính là ngày/tháng/năm Âm lịch.

## 🖼️ Sử Dụng Custom Card (Hiển thị Lịch Tuần)

Để hiển thị giao diện lịch tuần đẹp mắt, bạn cần thêm file JS vào cấu hình Lovelace Resources.

1. Vào **Settings** -> **Dashboards** -> **Resources** (Tài nguyên).
2. Nhấn **+ ADD RESOURCE** (Thêm tài nguyên).
3. **URL:** `/hacsfiles/lunar_calendar_ha/lunar_calendar.js`
4. **Resource Type:** **JavaScript Module**.

Sau đó, thêm card vào Dashboard bằng **YAML Card**:

type: custom:lunar-calendar

# Không cần entity vì card tự tính toán

Automation
```yaml
  alias: Bat den vao ngay 15 va 30 am lich
  description: Tu dong bat den luc mat troi moc va tat den luc 9h ngay 15/30 am lich
  mode: single
  trigger:
    - platform: sun
      event: sunrise
    - platform: time
      at: "09:00:00"

  condition: []
  action:
    - choose:
      # Khi mat troi moc
        - conditions:
            - condition: trigger
              id: sunrise
            - condition: or
              conditions:
                - condition: state
                  entity_id: sensor.ngay_am_lich
                  state: "15"
                - condition: state
                  entity_id: sensor.ngay_am_lich
                  state: "30"
          sequence:
            - service: switch.turn_on
              target:
                entity_id: switch.ten
      # Khi den 9h
        - conditions:
            - condition: trigger
              id: time_9h
          sequence:
            - service: switch.ten
              target:
                entity_id: switch.chuangmi_plug_m1_3

