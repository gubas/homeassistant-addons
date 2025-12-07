from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "wled_icons"
DATA_HOST = "host"
DATA_ADDON_URL = "addon_url"

class WledIconsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input.get(DATA_HOST)
            
            # Set default addon_url if not provided
            if not user_input.get(DATA_ADDON_URL):
                user_input[DATA_ADDON_URL] = "http://localhost:8234"
            
            title = "WLED Icons"
            if host:
                title = f"WLED Icons ({host})"
                
            return self.async_create_entry(
                title=title,
                data=user_input
            )
        
        schema = vol.Schema({
            vol.Optional(DATA_HOST): str,
            vol.Optional(DATA_ADDON_URL, default="http://localhost:8234"): str
        })
        return self.async_show_form(
            step_id="user", 
            data_schema=schema, 
            errors=errors
        )
