"""Config flow for Lunar Calendar integration."""
from homeassistant import config_entries
import voluptuous as vol

from . import DOMAIN

class LunarCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lunar Calendar."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        return self.async_create_entry(title="Lịch Âm Lịch Việt", data={})
