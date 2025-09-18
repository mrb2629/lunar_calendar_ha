"""The Lunar Calendar integration."""
DOMAIN = "lunar_calendar"

async def async_setup(hass, config):
    """Set up the Lunar Calendar component."""
    # Không cần xử lý cấu hình trong configuration.yaml nữa
    return True

async def async_setup_entry(hass, entry):
    """Set up Lunar Calendar from a config entry."""
    # Chuyển tiếp việc setup sang nền tảng Sensor
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

# Bổ sung hàm để xử lý việc gỡ bỏ (optional, but good practice)
async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
