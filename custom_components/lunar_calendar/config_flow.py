"""Config flow for Lunar Calendar integration."""
from homeassistant import config_entries
import voluptuous as vol

from . import DOMAIN

class LunarCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lunar Calendar."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Kiểm tra nếu đã có một phiên bản được cấu hình, ngăn chặn việc tạo trùng lặp
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        # Vì không cần bất kỳ input nào, ta chỉ cần gọi create_entry
        if user_input is not None or True:
            return self.async_create_entry(title="Lịch Âm Lịch Việt", data={})

        # Bước này sẽ không bao giờ đạt được nếu ta luôn gọi async_create_entry
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))