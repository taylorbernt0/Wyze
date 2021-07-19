import os
import threading
from datetime import timedelta
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
import time
import math
import random
import colorsys

email, password = 'taylorbernt@gmail.com', 'Q$FqekFk2h7zF9i'
client = Client(email=email, password=password)

print('Signed into api as {}'.format(email))

def list_devices():
    try:
        response = client.devices_list()
        for device in client.devices_list():
            print(f"mac: {device.mac}")
            print(f"nickname: {device.nickname}")
            print(f"is_online: {device.is_online}")
            print(f"product model: {device.product.model}")
            print()
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def pulse_mode(macs, duration):
    print('Starting pulse mode')
    try:
        bulbs = [client.bulbs.info(device_mac=mac) for mac in macs]
        for bulb in bulbs:
            client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model,
                                  brightness=100)
        print('Set all lights to 100% brightness')

        speed = 20

        start = time.time()
        while True:

            hsv_color = (random.random(), 0.6, 1)
            rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
            rgb_color = (int(255 * rgb_color[0]), int(255 * rgb_color[1]), int(255 * rgb_color[2]))
            hex_color = '%02x%02x%02x' % rgb_color

            for bulb in bulbs:
                client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=hex_color)

            for i in range(100 // speed + 1):
                for bulb in bulbs:
                    client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=i)
            for i in range(100 // speed + 1):
                for bulb in bulbs:
                    client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=100-i)

            if time.time() - start >= duration:
                break
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def hsv_to_hex(hsv_color):
    rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
    rgb_color = (int(255 * rgb_color[0]), int(255 * rgb_color[1]), int(255 * rgb_color[2]))
    return '%02x%02x%02x' % rgb_color

def set_brightness(bulb, brightness):
    if type(bulb) is list:
        for b in bulb:
            set_brightness(b, brightness)
    else:
        client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model,
                                brightness=brightness)

def set_color(bulb, color):
    if type(bulb) is list:
        for b in bulb:
            set_color(b, color)
    else:
        client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model,
                           color=color)

def party_mode(macs, duration=99999):
    print('Starting party mode')
    try:
        bulbs = [client.bulbs.info(device_mac=mac) for mac in macs]
        set_brightness(bulbs, 100)

        start = time.time()
        while time.time() - start < duration:
            threads = list()

            for bulb in bulbs:
                hex_color = hsv_to_hex((random.random(), 0.6, 1))

                t = threading.Thread(target=set_color, args=(bulb, hex_color))
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def rainbow_mode(macs, speed=1, duration=99999):
    print('Starting rainbow mode')
    try:
        bulbs = [client.bulbs.info(device_mac=mac) for mac in macs]
        set_brightness(bulbs, 100)

        start = time.time()

        i = 0
        while time.time() - start < duration:
            threads = list()

            hex_color = hsv_to_hex((i / 100.0, 0.6, 1))
            for bulb in bulbs:
                t = threading.Thread(target=set_color, args=(bulb, hex_color))
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

            i += speed
            i %= 100
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def strobe_mode(macs, duration=99999):
    print('Starting strobe mode')
    try:
        bulbs = [client.bulbs.info(device_mac=mac) for mac in macs]
        set_brightness(bulbs, 100)
        set_color(bulbs, 'FFFFFF')

        start = time.time()

        on = False
        while time.time() - start < duration:
            threads = list()

            for bulb in bulbs:
                t = threading.Thread(target=set_brightness, args=(bulb, 100 if on else 0))
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

            on = not on
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

living_room_lights = ['7C78B214359E', '7C78B2172ED6', '7C78B217887C', '7C78B2189C55', '7C78B2171F1F']
office_light = ['7C78B216AE54']
kitchen_lights = ['7C78B216E2EF', '7C78B2151E03', '7C78B216AED2']
dining_lights = ['7C78B216E115', '7C78B2187720', '7C78B218F187', '7C78B215953A', '7C78B2173185']
taylor_light = ['7C78B21529B8']
taylor_bathroom_lights = ['7C78B218995E', '7C78B216BEEC', '7C78B2176CDA']

all_lights = living_room_lights + office_light + kitchen_lights + dining_lights + taylor_light + taylor_bathroom_lights

if __name__ == "__main__":
    rainbow_mode(living_room_lights)