import os
import threading
from datetime import timedelta
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
import time
import math
import random
import colorsys
import json
import multiprocessing


def print_devices(client):
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

def hsv_to_hex(hsv_color):
    rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
    rgb_color = (int(255 * rgb_color[0]), int(255 * rgb_color[1]), int(255 * rgb_color[2]))
    return '%02x%02x%02x' % rgb_color

def set_brightness(client, bulbs, brightness):
    if type(bulbs) is list:
        for b in bulbs:
            set_brightness(client, b, brightness)
    else:
        client.bulbs.set_brightness(device_mac=bulbs.mac, device_model=bulbs.product.model,
                                brightness=brightness)

def set_brightness_threaded(client, bulbs, brightness):
    threads = list()
    for bulb in bulbs:
        t = threading.Thread(target=set_brightness, args=(client, bulb, brightness), daemon=True)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

def set_color(client, bulbs, color):
    if type(bulbs) is list:
        for b in bulbs:
            set_color(client, b, color)
    else:
        client.bulbs.set_color(device_mac=bulbs.mac, device_model=bulbs.product.model,
                           color=color)

def set_color_threaded(client, bulbs, color):
    threads = list()
    for bulb in bulbs:
        t = threading.Thread(target=set_color, args=(client, bulb, color), daemon=True)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

def set_temp(client, bulbs, temp):
    if type(bulbs) is list:
        for b in bulbs:
            set_temp(client, b, temp)
    else:
        client.bulbs.set_color_temp(device_mac=bulbs.mac, device_model=bulbs.product.model,
                           color_temp=temp)

def set_temp_threaded(client, bulbs, temp):
    threads = list()
    for bulb in bulbs:
        t = threading.Thread(target=set_temp, args=(client, bulb, temp), daemon=True)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

def set_on(client, bulbs):
    if type(bulbs) is list:
        for b in bulbs:
            set_on(client, b)
    else:
        client.bulbs.turn_on(device_mac=bulbs.mac, device_model=bulbs.product.model)

def set_off(client, bulbs):
    if type(bulbs) is list:
        for b in bulbs:
            set_off(client, b)
    else:
        client.bulbs.turn_off(device_mac=bulbs.mac, device_model=bulbs.product.model)

def party_mode(client, macs, brightness=100, duration=99999):
    print('Starting party mode')
    try:
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)

        start = time.time()
        while time.time() - start < duration:
            threads = list()

            for bulb in bulbs:
                hex_color = hsv_to_hex((random.random(), 1, 1))

                t = threading.Thread(target=set_color, args=(client, bulb, hex_color), daemon=True)
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def rainbow_mode(client, macs, brightness=100, speed=2, duration=99999):
    print('Starting rainbow mode')
    try:
        #bulbs = [client.bulbs.info(device_mac=mac) for mac in macs]
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)

        start = time.time()

        i = 0
        while time.time() - start < duration:
            threads = list()

            hex_color = hsv_to_hex((i / 100.0, 1, 1))
            for bulb in bulbs:
                t = threading.Thread(target=set_color, args=(client, bulb, hex_color), daemon=True)
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

            i += speed
            i %= 100
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def strobe_mode(client, macs, brightness=100, duration=99999):
    print('Starting strobe mode')
    try:
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        set_color_threaded(client, bulbs, 'FF0000')

        start = time.time()

        on = False
        while time.time() - start < duration:
            threads = list()

            for bulb in bulbs:
                t = threading.Thread(target=set_on if on else set_off, args=(bulb,), daemon=True)
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

            on = not on
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def color_mode(client, macs, color, brightness=100):
    try:
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        set_color_threaded(client, bulbs, color)
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def temp_mode(client, macs, temp, brightness=100):
    try:
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        set_temp_threaded(client, bulbs, temp)
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

bulb_info_cache = {}
def _get_bulb_info(client, mac):
    info = client.bulbs.info(device_mac=mac)
    bulb_info_cache[mac] = info
    return info

def get_bulbs_info(client, macs=None, try_use_cache=False):
    if try_use_cache and len(bulb_info_cache) != 0:
        return bulb_info_cache

    bulbs = client.bulbs.list()
    threads = list()
    for b in bulbs:
        if (macs is None) or (macs is not None and b.mac in macs):
            t = threading.Thread(target=_get_bulb_info, args=(client, b.mac,))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    return list(bulb_info_cache.values())

bulb_info_json_cache = {}
def _get_bulb_info_json(client, mac):
    info = client.bulbs.info(device_mac=mac).get_non_null_attributes()
    del info['switch_state']
    bulb_info_json_cache[mac] = info
    return info

def get_bulbs_info_json(client, try_use_cache=False):
    if try_use_cache and len(bulb_info_json_cache) != 0:
        return json.dumps(bulb_info_json_cache)

    bulbs = client.bulbs.list()
    threads = list()
    for b in bulbs:
        t = threading.Thread(target=_get_bulb_info_json, args=(client, b.mac,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return json.dumps(bulb_info_json_cache)

living_room_lights = ['7C78B214359E', '7C78B2172ED6', '7C78B217887C', '7C78B2189C55', '7C78B2171F1F']
office_light = ['7C78B216AE54']
kitchen_lights = ['7C78B216E2EF', '7C78B2151E03', '7C78B216AED2']
dining_lights = ['7C78B216E115', '7C78B2187720', '7C78B218F187', '7C78B215953A', '7C78B2173185']
taylor_light = ['7C78B21529B8']
taylor_bathroom_lights = ['7C78B218995E', '7C78B216BEEC', '7C78B2176CDA']

all_lights = living_room_lights + office_light + kitchen_lights + dining_lights + taylor_light + taylor_bathroom_lights

def get_client():
    email, password = 'taylorbernt@gmail.com', 'Q$FqekFk2h7zF9i'
    client = Client(email=email, password=password)
    print('Signed into api as {}'.format(email))
    return client

if __name__ == "__main__":
    client = get_client()
    #rainbow_mode(all_lights, speed=4)
    lis = get_bulbs_info_json(client)
    print(lis)
    #rainbow_mode(client, macs=living_room_lights)