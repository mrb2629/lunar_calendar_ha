"""The Lunar Calendar integration."""
DOMAIN = "lunar_calendar"
PLATFORMS = ["sensor"]

async def async_setup(hass, config):
    """Set up the Lunar Calendar component."""
    return True

# HÀM NÀY PHẢI GỌI setup_entry của nền tảng Sensor
async def async_setup_entry(hass, entry):
    """Set up Lunar Calendar from a config entry."""
    # SỬ DỤNG 'async_forward_entry_setups' (số nhiều)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
