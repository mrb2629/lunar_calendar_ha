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

>- type: custom:lunar-calendar  
>  entity: sensor.ngay_am_lich  

<img width="501" height="276" alt="lich 1" src="https://github.com/user-attachments/assets/64e0d0e3-42be-4350-882e-10f451131bee" />
  
Automation
```yaml
- id: "0205"
  alias: 0205 Bat den vao ngay 15 va 1 am lich
  description: Tu dong bat den luc mat troi moc va tat den luc 10h ngay 15/1 am lich
  mode: single
  trigger:
    # Trigger luc mat troi moc
    - platform: sun
      event: sunrise
      id: "sunrise"

    # Trigger luc 10:00
    - platform: time
      at: "10:00:00"
      id: "time_10h"

  condition: []
  action:
    - choose:
        - conditions:
            - condition: trigger
              id: "sunrise"
            - condition: or
              conditions:
                - condition: state
                  entity_id: sensor.ngay_am_lich
                  state: "15"
                - condition: state
                  entity_id: sensor.ngay_am_lich
                  state: "1"
          sequence:
            - service: switch.turn_on
              target:
                entity_id: switch.chuangmi_plug_m1_3

        - conditions:
            - condition: trigger
              id: "time_10h"
          sequence:
            - service: switch.turn_off
              target:
                entity_id: switch.chuangmi_plug_m1_3
