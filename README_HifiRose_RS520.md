# HiFi Rose RS520 - Home Assistant Integration

This is a **custom integration** for [Home Assistant](https://www.home-assistant.io) that allows basic local control of the **HiFi Rose RS520** amplifier over your local network (LAN), **without relying on cloud services**.

## ✨ Features

- Turn the RS520 on/off
- Set volume via Home Assistant
- Switch between input sources (LINE IN, OPTICAL IN, eARC IN, USB IN, AES/EBU IN)
- Entity exposed as a `media_player` in Home Assistant
- UI-configurable via the Integrations page

## ⚠ Limitations

- The **volume slider does not reflect changes made on the amplifier itself** (due to current API limitations).  
- **Power state and input source** do sync correctly in both directions.
- No media playback metadata or album art is shown (not supported in current mode).

## 📡 Network Setup

Please ensure that your RS520 amplifier has a **static IP address** assigned via your router.  
The integration communicates with the device on **port `9283`**, which must be accessible on your LAN.

Example:  
`http://192.168.1.12:9283`

## 🔧 Installation

1. Copy the `hifirose_rs520` folder into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.
3. Navigate to **Settings → Devices & Services → Add Integration**.
4. Search for **HiFi Rose RS520** and enter the static IP address of your amplifier.

## 🧪 Tested On

**Home Assistant**  
- Installation method: Home Assistant OS  
- Core: `2025.6.1`  
- Supervisor: `2025.07.3`  
- Operating System: `15.2`  
- UI version: `20250531.3`  

**HiFi Rose Firmware**  
- Version: `5.9.02`

## 🛠️ Contributing

Feel free to fork and improve this integration!  
If you add features or fix bugs, please share the updated version with me as well so we can keep the integration evolving.

---

# HiFi Rose RS520 - Home Assistant integráció

Ez egy **egyedi integráció** a [Home Assistant](https://www.home-assistant.io) rendszerhez, amely lehetővé teszi a **HiFi Rose RS520** erősítő alapvető helyi (LAN-on keresztüli) vezérlését, **felhőszolgáltatás használata nélkül**.

## ✨ Funkciók

- Az RS520 be- és kikapcsolása
- Hangerő beállítása Home Assistantból
- Bemenetválasztás (LINE IN, OPTICAL IN, eARC IN, USB IN, AES/EBU IN)
- Az eszköz `media_player` entitásként jelenik meg a Home Assistantban
- Az Integrációk menüből UI-n keresztül konfigurálható

## ⚠ Korlátozások

- A **hangerő csúszka nem tükrözi az erősítőn kézzel beállított hangerőt** (jelenlegi API korlát miatt).  
- **A ki-/bekapcsolt állapot és a bemenet** viszont helyesen szinkronizálódik.
- Médialejátszási információk (pl. albumborító, számcím) nem érhetők el.

## 📡 Hálózati beállítás

Fontos, hogy az RS520 erősítő **fix IP címet kapjon a routertől**.  
Az integráció a **9283-as porton** kommunikál az eszközzel, amelynek elérhetőnek kell lennie a helyi hálózaton.

Példa:  
`http://192.168.1.12:9283`

## 🔧 Telepítés

1. Másold a `hifirose_rs520` mappát a Home Assistant `/config/custom_components/` könyvtárába.
2. Indítsd újra a Home Assistantot.
3. Lépj a **Beállítások → Eszközök és Szolgáltatások → Új integráció hozzáadása** menüpontra.
4. Keresd meg a **HiFi Rose RS520**-at, és add meg az erősítő fix IP-címét.

## 🧪 Tesztelt verziók

**Home Assistant**  
- Telepítési mód: Home Assistant OS  
- Core: `2025.6.1`  
- Supervisor: `2025.07.3`  
- Operációs rendszer: `15.2`  
- Felület verzió: `20250531.3`  

**HiFi Rose firmware**  
- Verzió: `5.9.02`

## 🛠️ Hozzájárulás

Bátran fejleszd tovább az integrációt!  
Ha hibát javítasz vagy funkciót bővítesz, kérlek oszd meg velem is a frissített verziót, hogy közösen fejleszthessük tovább.