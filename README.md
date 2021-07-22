export FLASK_APP=server.py
export FLASK_ENV=development
flask run -h 192.168.1.199

pip install -U flask-cors

##Requests:

---

**Get a JSON object of all bulbs and their attributes:**

- **<span style="color: green">GET /bulbs</span>**
* **Example:**
  * ```

        {
            "7C78B2173185": {
                "away_mode": false,
                "brightness": 80,
                "color": "00ffe0",
                "color_temp": 2996,
                "enr": "ZWtYa/x0pKYhJV2r",
                "ip": "192.168.1.137",
                "mac": "7C78B2173185",
                "nickname": "Dining Room 5",
                "power_loss_recovery": false,
                "push_switch": 1,
                "rssi": "0",
                "ssid": "Moore",
                "type": "MeshLight"
            },
            "7C78B2187720": {
                "away_mode": false,
                "brightness": 80,
                "color": "00ffe0",
                "color_temp": 2996,
                "enr": "xQUETXwFmHFEA/io",
                "ip": "192.168.1.175",
                "mac": "7C78B2187720",
                "nickname": "Dining Room 2",
                "power_loss_recovery": false,
                "push_switch": 1,
                "rssi": "0",
                "ssid": "Moore",
                "type": "MeshLight"
            },
            ...
        }
    
    ```

---

**Change the light mode**

* **<span style="color: green">POST /bulbs</span>**
* **Parameters:**
  * **<u>mode</u> (lower string)**: Determines what action the bulbs take
    * **Examples**: <i>"temp", "color", "rainbow", "party", "strobe"</i>
  * **<u>macs</u> (python string list)**: A list of the bulbs that are acted on
    * **Example**: <i>"['7C78B214359E', '7C78B2172ED6', '7C78B217887C']"</i>
  * **<u>color</u> (hex no hash)**: Sets the color (on certain modes)
    * **Examples**: <i>"FFFFFF", "ABCDEF", "000000", "FF000000"</i>
  * **<u>brightness</u> (0-100)**: Sets the brightness
    * **Examples**: <i>"0", "1", "2", "50", "99", "100"</i>

---

**Terminate a process:**

- **<span style="color: green">DELETE /bulbs</span>**

* **Parameters:**
  * **No Parameter**: Terminates all processes
  * **<u>pid</u> (guid)**: Determines which process to terminate
    * **Example**: <i>"675f0cb5-c6b1-477a-9c41-d23e07d1e092"</i>