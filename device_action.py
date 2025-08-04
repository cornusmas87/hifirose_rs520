from typing import List
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import EntityRegistry, RegistryEntry
from homeassistant.components.device_automation import ActionType
from .const import DOMAIN

async def async_get_actions(hass, device_id: str) -> List[ActionType]:
    return [
        {
            "domain": DOMAIN,
            "type": "turn_on",
            "device_id": device_id,
            "entity_id": "",
        },
        {
            "domain": DOMAIN,
            "type": "turn_off",
            "device_id": device_id,
            "entity_id": "",
        }
    ]

async def async_call_action_from_config(hass, config, variables, context=None):
    service = "turn_on" if config["type"] == "turn_on" else "turn_off"
    await hass.services.async_call("media_player", service, {
        "entity_id": config["entity_id"]
    }, context=context)

def async_validate_action_config(hass, config: ConfigType) -> ConfigType:
    return config
