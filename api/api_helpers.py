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
from enum import Enum

class Lights(Enum):
    LIVING_ROOM = ['7C78B214359E', '7C78B2172ED6', '7C78B217887C', '7C78B2189C55', '7C78B2171F1F']
    OFFICE = ['7C78B216AE54']
    KITCHEN = ['7C78B216E2EF', '7C78B2151E03', '7C78B216AED2']
    DINING_ROOM = ['7C78B216E115', '7C78B2187720', '7C78B218F187', '7C78B215953A', '7C78B2173185']
    TAYLOR_BED = ['7C78B21529B8']
    TAYLOR_BATH = ['7C78B218995E', '7C78B216BEEC', '7C78B2176CDA']
    ALL = LIVING_ROOM + OFFICE + KITCHEN + DINING_ROOM + TAYLOR_BED + TAYLOR_BATH

def get_client():
    s = time.time()
    email, password = 'taylorbernt@gmail.com', 'Q$FqekFk2h7zF9i'
    client = Client(email=email, password=password)
    print('Signed into api as {0} ({1}s)'.format(email, str(round(time.time()-s, 2))))
    return client

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

_bulb_info_cache = {}
def _get_bulb_info(client, mac):
    info = client.bulbs.info(device_mac=mac)
    _bulb_info_cache[mac] = info
    return info

def get_bulbs_info(client, macs=None, try_use_cache=False):
    if try_use_cache and len(_bulb_info_cache) != 0:
        return _bulb_info_cache

    bulbs = client.bulbs.list()
    threads = list()
    for b in bulbs:
        if (macs is None) or (macs is not None and b.mac in macs):
            t = threading.Thread(target=_get_bulb_info, args=(client, b.mac,))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    return list(_bulb_info_cache.values())

_bulb_info_json_cache = {}
def _get_bulb_info_json(client, mac):
    bulb_info = client.bulbs.info(device_mac=mac)
    info = bulb_info.get_non_null_attributes()
    info['is_on'] = bulb_info.is_on
    info['is_online'] = bulb_info.is_online
    del info['switch_state']
    _bulb_info_json_cache[mac] = info
    return info

def get_bulbs_info_json(client, try_use_cache=False):
    if try_use_cache and len(_bulb_info_json_cache) != 0:
        return json.dumps(_bulb_info_json_cache)

    bulbs = client.bulbs.list()
    threads = list()
    for b in bulbs:
        t = threading.Thread(target=_get_bulb_info_json, args=(client, b.mac,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return json.dumps(_bulb_info_json_cache)