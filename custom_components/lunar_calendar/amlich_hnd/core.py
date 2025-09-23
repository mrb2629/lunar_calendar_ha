import math

DEBUG = False  # Bật = True để in debug

# ===============================
# Các hàm thiên văn cơ bản
# ===============================

def jd_from_date(dd, mm, yy):
    """Đổi ngày dương lịch sang số ngày Julius (JDN) tại 0h UT."""
    a = int((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5) + 365 * y
    jd += int(y / 4) - int(y / 100) + int(y / 400) - 32045
    return jd

def jd_to_date(jd):
    """Đổi JDN sang ngày dương lịch (ngày, tháng, năm)."""
    a = jd + 32044
    b = int((4 * a + 3) / 146097)
    c = a - int((146097 * b) / 4)
    d = int((4 * c + 3) / 1461)
    e = c - int((1461 * d) / 4)
    m = int((5 * e + 2) / 153)
    day = e - int((153 * m + 2) / 5) + 1
    month = m + 3 - 12 * int(m / 10)
    year = 100 * b + d - 4800 + int(m / 10)
    return (day, month, year)

def jd_local_from_date(dd, mm, yy, tz=7):
    """JDN hiệu chỉnh theo múi giờ địa phương (Việt Nam = 7)."""
    jd = jd_from_date(dd, mm, yy)
    jd = jd - 0.5 + tz/24.0
    return int(jd + 0.5)

def sun_longitude(jdn, timeZone):
    T = (jdn - 2451545.5 - timeZone/24.0) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr*M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr*2*M)
    DL += 0.000290 * math.sin(dr*3*M)
    L = (L0 + DL) * dr
    return L % (2*math.pi)

def new_moon(k):
    T = k/1236.85
    T2 = T*T
    T3 = T2*T
    dr = math.pi/180
    Jd1 = 2415020.75933 + 29.53058868*k
    Jd1 += 0.0001178*T2 - 0.000000155*T3
    Jd1 += 0.00033*math.sin((166.56+132.87*T-0.009173*T2)*dr)
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3
    C1 = (0.1734 - 0.000393*T)*math.sin(dr*M)
    C1 += 0.0021*math.sin(dr*2*M)
    C1 -= 0.4068*math.sin(dr*Mpr)
    C1 += 0.0161*math.sin(dr*2*Mpr)
    C1 -= 0.0004*math.sin(dr*3*Mpr)
    C1 += 0.0104*math.sin(dr*2*F)
    C1 -= 0.0051*math.sin(dr*(M+Mpr))
    C1 -= 0.0074*math.sin(dr*(M-Mpr))
    C1 += 0.0004*math.sin(dr*(2*F+M))
    C1 -= 0.0004*math.sin(dr*(2*F-M))
    C1 -= 0.0006*math.sin(dr*(2*F+Mpr))
    C1 += 0.0010*math.sin(dr*(2*F-Mpr))
    C1 += 0.0005*math.sin(dr*(2*Mpr+M))
    if T < -11:
        deltat = 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
    else:
        deltat = -0.000278 + 0.000265*T + 0.000262*T2
    return Jd1 + C1 - deltat

def get_new_moon_day(k, timeZone):
    return int(new_moon(k) + 0.5 + timeZone/24.0)

def get_sun_longitude(dayNumber, timeZone):
    return int(sun_longitude(dayNumber, timeZone) / math.pi * 6)

def get_lunar_month11(yy, timeZone):
    off = jd_from_date(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, timeZone)
    sunLong = get_sun_longitude(nm, timeZone)
    if sunLong >= 9:
        nm = get_new_moon_day(k-1, timeZone)
    return nm

def get_leap_month_offset(a11, timeZone):
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    last = get_sun_longitude(get_new_moon_day(k+1, timeZone), timeZone)
    i = 2
    while i < 14:
        arc = get_sun_longitude(get_new_moon_day(k+i, timeZone), timeZone)
        if arc == last:
            return i-1
        last = arc
        i += 1
    return 0

# ===============================
# Hàm chuyển đổi chính (đã sửa lỗi)
# ===============================

def solar_to_lunar(dd, mm, yy, timeZone=7):
    """Đổi Dương lịch -> Âm lịch (có xử lý đúng tháng nhuận)."""
    dayNumber = jd_from_date(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)

    monthStart = get_new_moon_day(k+1, timeZone)
    if monthStart > dayNumber:
        monthStart = get_new_moon_day(k, timeZone)

    a11 = get_lunar_month11(yy, timeZone)
    b11 = get_lunar_month11(yy+1, timeZone)
    if a11 >= monthStart:
        lunarYear = yy
        a11 = get_lunar_month11(yy-1, timeZone)
    else:
        lunarYear = yy+1

    lunarDay = dayNumber - monthStart + 1
    diff = int((monthStart - a11) / 29)
    lunarMonth = diff + 11
    lunarLeap = 0

    # -----------------------------
    # 🔧 CHỈNH SỬA QUAN TRỌNG:
    # Trước đây khi diff == leapMonthDiff,
    # code gán nhầm ngày đầu tháng nhuận cho tháng thường trước đó.
    # Nay đã tách rõ: diff == leapMonthDiff -> tháng nhuận (lunarLeap=1).
    # -----------------------------
    if b11 - a11 > 365:
        leapMonthDiff = get_leap_month_offset(a11, timeZone)
        if diff == leapMonthDiff:
            lunarLeap = 1
        elif diff > leapMonthDiff:
            lunarMonth -= 1

    if lunarMonth > 12:
        lunarMonth -= 12
    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1

    if DEBUG:
        print(f"[DEBUG] DL {dd}/{mm}/{yy} -> AL {lunarDay}/{lunarMonth}{'(nhuận)' if lunarLeap else ''}/{lunarYear}")

    return lunarDay, lunarMonth, lunarYear, lunarLeap

def lunar_to_solar(lunarDay, lunarMonth, lunarYear, lunarLeap, timeZone=7):
    if lunarMonth < 11:
        a11 = get_lunar_month11(lunarYear-1, timeZone)
        b11 = get_lunar_month11(lunarYear, timeZone)
    else:
        a11 = get_lunar_month11(lunarYear, timeZone)
        b11 = get_lunar_month11(lunarYear+1, timeZone)
    k = int(0.5 + (a11 - 2415021.076998695)/29.530588853)
    off = lunarMonth - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leapOff = get_leap_month_offset(a11, timeZone)
        leapMonth = leapOff - 1
        if leapMonth < 1:
            leapMonth += 12
        if lunarLeap != 0 and lunarMonth != leapMonth:
            return 0,0,0
        elif lunarLeap != 0 or off >= leapOff:
            off += 1
    monthStart = get_new_moon_day(k+off, timeZone)
    return jd_to_date(monthStart + lunarDay - 1)

    # In debug
    print(f"== DEBUG solar_to_lunar({dd}/{mm}/{yy}) ==")
    print(f"dayNumber (JDN)   = {dayNumber}")
    print(f"monthStart (DL)  = {jd_to_date(monthStart)} (JDN {monthStart})")
    print(f"a11 (DL)         = {jd_to_date(a11)} (JDN {a11})")
    print(f"b11 (DL)         = {jd_to_date(b11)} (JDN {b11})")
    print(f"diff             = {diff}")
    print(f"lunarMonth       = {lunarMonth}")
    print(f"lunarLeap        = {lunarLeap}")
    print("======================================")

    return lunarDay, lunarMonth, lunarYear, lunarLeap


# ------------------------
# Test nhanh
# Cách chạy test
# python core.py
# ------------------------
if __name__ == "__main__":
    test_days = [
        (20, 3, 2004),
        (20, 3, 2024),
        (26, 7, 2025),
    ]
    for dd, mm, yy in test_days:
        lunarDay, lunarMonth, lunarYear, lunarLeap = solar_to_lunar(dd, mm, yy, 7)
        print(f"Dương lịch {dd}/{mm}/{yy} -> Âm lịch {lunarDay}/{lunarMonth}{' (nhuận)' if lunarLeap else ''}/{lunarYear}")
