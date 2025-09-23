function getMonday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

function getMoonPhaseIcon(lunarDay) {
    if (lunarDay == 1) return "🌑";
    if (lunarDay <= 7) return "🌒";
    if (lunarDay == 8) return "🌓";
    if (lunarDay <= 14) return "🌔";
    if (lunarDay <= 16) return "🌕";
    if (lunarDay <= 22) return "🌖";
    if (lunarDay <= 29) return "🌘";
    if (lunarDay >= 30) return "🌑";
    return "🌙";
}

function convertHoangDaoHours(hoursString) {
    const hourMap = {
        'Tý': '23h-1h',
        'Sửu': '1h-3h',
        'Dần': '3h-5h',
        'Mão': '5h-7h',
        'Thìn': '7h-9h',
        'Tỵ': '9h-11h',
        'Ngọ': '11h-13h',
        'Mùi': '13h-15h',
        'Thân': '15h-17h',
        'Dậu': '17h-19h',
        'Tuất': '19h-21h',
        'Hợi': '21h-23h',
    };

    return hoursString
        .split(',')
        .map(hour => {
            const trimmedHour = hour.trim();
            return hourMap[trimmedHour] || trimmedHour;
        })
        .join(' | ');
}

class LunarCalendar extends HTMLElement {
    set hass(hass) {
        if (!this.content) {
            const card = document.createElement("ha-card");
            card.header = "";
            this.content = document.createElement("div");
            card.appendChild(this.content);
            this.appendChild(card);
        }

        const entityId = this.config ? this.config.entity : "sensor.ngay_am_lich";
        const state = hass.states[entityId];

        let lunarHourSensor = "N/A";
        let lunarDaySensor = "N/A";
        let lunarMonthSensor = "N/A";
        let lunarYearSensor = "N/A";
        let danhSachGioHoangDao = "";
        let danhSachNgayHoangDao = "";
        let tinhChatGio = "";
        let tinhChatNgay = "";
        let d = 0;
        let m = 0;
        let lunarDatesOfWeek = {};

        if (state && state.attributes) {
            lunarHourSensor = state.attributes["Can Chi Giờ"] || "N/A";
            lunarDaySensor = state.attributes["Can Chi Ngày"] || "N/A";
            lunarMonthSensor = state.attributes["Can Chi Tháng"] || "N/A";
            lunarYearSensor = state.attributes["Can Chi Năm"] || "N/A";
            danhSachGioHoangDao = state.attributes["Danh sách giờ Hoàng đạo"] || "";
            danhSachNgayHoangDao = state.attributes["Danh sách ngày Hoàng đạo trong tháng (âm lịch)"] || "";
            tinhChatGio = state.attributes["Tính chất giờ hiện tại"] || "";
            tinhChatNgay = state.attributes["Tính chất ngày hiện tại"] || "";
            d = state.attributes["Ngày âm lịch"] || 0;
            m = state.attributes["Tháng âm lịch"] || 0;
            lunarDatesOfWeek = state.attributes["Ngày âm lịch tuần này"] || {};
        }

        const gioIcon = tinhChatGio === "Hoàng đạo" ? "⭐ " : "";
        const ngayIcon = tinhChatNgay === "Hoàng đạo" ? "⭐ " : "";

        const gioClass = tinhChatGio === "Hoàng đạo" ? "highlight-hoangdao" : "";
        const ngayClass = tinhChatNgay === "Hoàng đạo" ? "highlight-hoangdao" : "";

        let arrNgayHoangDao = danhSachNgayHoangDao
            .split(",")
            .map(x => parseInt(x.trim(), 10))
            .filter(x => !isNaN(x));

        const date = new Date();
        const ddd = getMonday(date);

        let day = [];
        for (let i = 0; i < 7; i++) {
            let tempDate = new Date(ddd);
            tempDate.setDate(ddd.getDate() + i);
            day[i] = tempDate.getDate();
        }

        let lday = [];
        for (let i = 0; i < 7; i++) {
            let sensorDayKey;
            if (i === 6) { // Chủ Nhật
                sensorDayKey = `Ngày 8`;
            } else { // Thứ 2 - Thứ 7
                sensorDayKey = `Ngày ${i + 2}`;
            }

            const lunar_date_string = lunarDatesOfWeek[sensorDayKey];
            if (lunar_date_string) {
                const lunar_day_part = lunar_date_string.split('/')[0];
                lday.push(parseInt(lunar_day_part));
            } else {
                lday.push("?");
            }
        }

        let act = date.getDay();
        if (act == 0) act = 7;

        const today = Intl.DateTimeFormat("vi-VN", { weekday: "long" }).format(date);
        const currdate = date.toLocaleDateString("en-GB");

        const moonIcon = getMoonPhaseIcon(d);
        const lunarDateNumericInfo = `${moonIcon} ${d} / ${m}`;

        const lunarCanChiHTML = `
            <div class="can-chi-header">
                <div class="can-chi-col ${gioClass}">Giờ</div>
                <div class="can-chi-col ${ngayClass}">Ngày</div>
                <div class="can-chi-col">Tháng</div>
                <div class="can-chi-col">Năm</div>
            </div>
            <div class="can-chi-values">
                <div class="can-chi-col ${gioClass}">${gioIcon}${lunarHourSensor}</div>
                <div class="can-chi-col ${ngayClass}">${ngayIcon}${lunarDaySensor}</div>
                <div class="can-chi-col">${lunarMonthSensor}</div>
                <div class="can-chi-col">${lunarYearSensor}</div>
            </div>
        `;

        const gioHoangDaoHTML = danhSachGioHoangDao ? `
            <div class="gio-hoang-dao">
                ⏰ Giờ hoàng đạo: ${convertHoangDaoHours(danhSachGioHoangDao)}
            </div>
        ` : '';

        // Xóa nội dung cũ trước khi thêm nội dung mới
        this.content.innerHTML = '';
        this.content.innerHTML = `
            <div class="ldate">
                <div class="ldate-top">
                    <div class="day">
                        <div class="today-text">${today}</div>
                        <div class="currdate-text">☀️ ${currdate}</div>
                    </div>
                    <div class="date-block">
                        <div class="lunar-date-numeric">${lunarDateNumericInfo}</div>
                        ${lunarCanChiHTML}
                    </div>
                </div>
                ${gioHoangDaoHTML}
                <div class="week">
                    ${day
                        .map(
                            (d, i) => {
                                const isNgayHoangDao = arrNgayHoangDao.includes(lday[i]);
                                const starIcon = isNgayHoangDao ? "⭐ " : "";
                                return `
                                    <div class="we ${i === 6 ? "red" : ""} ${i + 1 === act ? "act" : ""}">
                                        <div class="we0">${["TH 2", "TH 3", "TH 4", "TH 5", "TH 6", "TH 7", "CN"][i]}</div>
                                        <div class="we1">${d}</div>
                                        <div class="we2">${starIcon}${lday[i]}</div>
                                    </div>`;
                            }
                        )
                        .join("")}
                </div>
            </div>
            <style>
                .ldate {
                    display: flex;
                    flex-direction: column;
                    padding: 5px;
                    font-family: Arial, sans-serif;
                }
                .ldate-top {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                }
                .day {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .today-text {
                    font-size: 2em;
                }
                .currdate-text {
                    font-size: 1.1em;
                    margin-top: 2px;
                }
                .lunar-date-numeric {
                    font-size: 2em;
                    width: 100%;
                    text-align: center;
                }
                .can-chi-header, .can-chi-values {
                    display: flex;
                    justify-content: space-between;
                    width: 100%;
                }
                .can-chi-col {
                    flex: 1;
                    text-align: center;
                    padding: 2px;
                    font-size: 1.1em;
                }
                .can-chi-header .can-chi-col {
                    font-size: 0.9em;
                    color: #888;
                }
                .can-chi-values .can-chi-col {
                    border-radius: 4px;
                    margin: 0 2px;
                }
                @media (prefers-color-scheme: light) {
                    .can-chi-values .can-chi-col {
                        background: #f0f0f0;
                    }
                }
                @media (prefers-color-scheme: dark) {
                    .can-chi-values .can-chi-col {
                        background: var(--card-background-color);
                        opacity: 0.8;
                    }
                }
                .gio-hoang-dao {
                    text-align: center;
                    font-size: 1em;
                    margin: 5px 0;
                    font-weight: bold;
                    color: #FF0000;
                }
                .week {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 2px;
                    margin-bottom: 5px;
                    width: 100%;
                }
                .we {
                    flex: 1;
                    text-align: center;
                    padding: 2px;
                }
                .we0 {
                    font-size: 1em;
                    color: #888;
                }
                .we1 {
                    font-size: 1.5em;
                }
                .we2 {
                    font-size: 1.2em;
                    color: #888;
                }
                .we.red .we0 {
                    color: #f05a5a;
                }
                .we.act {
                    background: #639FED;
                    color: #fff;
                    border-radius: 4px;
                }
                .we.act .we0,
                .we.act .we1,
                .we.act .we2 {
                    color: #fff;
                }
                .highlight-hoangdao {
                    font-weight: bold;
                }
            </style>
        `;
    }

    setConfig(config) {
        this.config = config;
    }

    getCardSize() {
        return 3;
    }
}

customElements.define("lunar-calendar", LunarCalendar);
