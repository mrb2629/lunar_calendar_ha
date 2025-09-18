// lunar_day.js
// Script tra ve ngay am (ngay trong thang am lich)

const today = new Date();
const lunarDay = +Intl.DateTimeFormat("zh-TW-u-ca-chinese", { day: "numeric" })
  .format(today)
  .match(/\d+/)[0];

console.log(lunarDay);
