"""The Lunar Calendar integration."""
DOMAIN = "lunar_calendar"
PLATFORMS = ["sensor"] # Khai báo các nền tảng sẽ setup

async def async_setup(hass, config):
    """Set up the Lunar Calendar component."""
    return True # Không làm gì nếu không có config trong configuration.yaml

async def async_setup_entry(hass, entry):
    """Set up Lunar Calendar from a config entry."""
    # Gọi hàm setup_platform bất đồng bộ cho tất cả các nền tảng
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # Gọi hàm unload_platform bất đồng bộ
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
