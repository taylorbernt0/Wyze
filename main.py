import os
from datetime import timedelta
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
import time
import math
import random
import colorsys

client = Client(email='taylorbernt@gmail.com', password='Q$FqekFk2h7zF9i')

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

def pulse_bulb(mac, duration):
    try:
      bulb = client.bulbs.info(device_mac=mac)
      r, g, b = 0, 0, 0
      speed = math.pi * 3
      i = 0
      start = time.time()
      while True:
        client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=int(-50*math.cos(i)+50))
        #client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color='%02x%02x%02x' % (r+i, g, b))
        #print('#%02x%02x%02x' % (r+i, g, b))
        #time.sleep(5)
        print(int(-50*math.cos(i)+50))
        i += 0.1 * speed
        if time.time() - start >= duration:
            break
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")

def party_mode(bulbs, duration):
    print('Starting party mode')
    try:
        bulbs = [client.bulbs.info(device_mac=mac) for mac in living_room_lights]
        for bulb in bulbs:
            client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model,
                                  brightness=100)
        print('Set all lights to 100% brightness')
        start = time.time()
        while True:
            for bulb in bulbs:

                hsv_color = (random.random(), 0.6, 1)
                rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                rgb_color = (int(255*rgb_color[0]), int(255*rgb_color[1]), int(255*rgb_color[2]))

                client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color='%02x%02x%02x' % rgb_color)
                print('#%02x%02x%02x' % rgb_color)
            print()
            if time.time() - start >= duration:
                break
    except WyzeApiError as e:
        # You will get a WyzeApiError is the request failed
        print(f"Got an error: {e}")


living_room_lights = ['7C78B214359E', '7C78B2172ED6', '7C78B217887C', '7C78B2189C55', '7C78B2171F1F']
party_mode(living_room_lights, 60)