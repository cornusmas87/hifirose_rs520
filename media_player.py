import logging
import requests
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

INPUT_SOURCES = {
    "LINE IN": 1,
    "OPTICAL IN": 2,
    "eARC IN": 3,
    "USB IN": 4,
    "AES/EBU IN": 5,
}

REVERSE_INPUT_SOURCES = {v: k for k, v in INPUT_SOURCES.items()}

class HifiRoseMediaPlayer(MediaPlayerEntity):
    _attr_should_poll = True
    _attr_device_class = "receiver"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, host: str, entry_id: str, name: str = "HifiRose RS520"):
        self._host = host
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"hifirose_rs520_{host.replace('.', '_')}"
        self._attr_state = MediaPlayerState.OFF
        self._attr_volume_level = 0.0
        self._attr_source = None
        self._attr_source_list = list(INPUT_SOURCES.keys())

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._attr_name,
            "manufacturer": "HiFi Rose",
            "model": "RS520",
            "configuration_url": f"http://{self._host}:9283"
        }

    async def async_turn_on(self):
        await self._send_post("/remote_bar_order", {
            "barControl": "remote_bar_order_sleep_on_off",
            "value": "1"
        })
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._send_post("/remote_bar_order", {
            "barControl": "remote_bar_order_sleep_on_off",
            "value": "-1"
        })
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume: float):
        vol_int = int(volume * 100)
        await self._send_post("/volume", {
            "volumeType": "volume_set",
            "volumeValue": vol_int
        })
        self._attr_volume_level = volume
        self.async_write_ha_state()

    async def async_select_source(self, source: str):
        func_mode = INPUT_SOURCES.get(source)
        if func_mode:
            await self._send_post("/input.mode.set", {"funcMode": func_mode})
            self._attr_source = source
            self.async_write_ha_state()

    async def async_update(self):
        try:
            response = await self.hass.async_add_executor_job(
                lambda: requests.post(
                    f"http://{self._host}:9283/get_current_state",
                    json={},
                    timeout=5
                )
            )
            data = response.json().get("data", {})

            # Volume parsing - only update if valid
            volume_raw = data.get("volume")
            if volume_raw is not None and isinstance(volume_raw, (int, float)) and volume_raw > 0:
                self._attr_volume_level = int(volume_raw) / 100.0
            else:
                _LOGGER.debug(f"Volume data invalid or zero: {volume_raw}, keeping previous level.")

            # Source parsing
            func_mode = None
            temp_arr = data.get("tempArr", [])
            for entry in temp_arr:
                if entry.startswith("funcMode:"):
                    try:
                        func_mode = int(entry.split(":")[1])
                    except ValueError:
                        func_mode = None
                    break
            self._attr_source = REVERSE_INPUT_SOURCES.get(func_mode)

            # Power state
            is_on = data.get("isPlaying", False) or data.get("isPowerOn", False)
            self._attr_state = MediaPlayerState.ON if is_on else MediaPlayerState.OFF

        except Exception as e:
            _LOGGER.error(f"Failed to update HifiRose RS520 state: {e}")
            self._attr_state = MediaPlayerState.OFF

    async def _send_post(self, endpoint: str, payload: dict):
        def _do_post():
            return requests.post(f"http://{self._host}:9283{endpoint}", json=payload, timeout=5)
        try:
            await self.hass.async_add_executor_job(_do_post)
        except Exception as e:
            _LOGGER.error(f"POST {endpoint} failed: {e}")

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
):
    host = config_entry.data[CONF_HOST]
    name = config_entry.title or "HifiRose RS520"
    entity = HifiRoseMediaPlayer(host, config_entry.entry_id, name)
    async_add_entities([entity], update_before_add=True)
