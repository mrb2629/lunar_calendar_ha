"""The Lunar Calendar integration."""
DOMAIN = "lunar_calendar"

async def async_setup(hass, config):
    """Set up the Lunar Calendar component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up Lunar Calendar from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True
