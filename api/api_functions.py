from api_helpers import *

def party_mode(client, macs, brightness=100, duration=99999):
    print('Starting party mode')
    try:
        s = time.time()
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        print("Initialized bulbs ({}s)".format(str(round(time.time() - s, 2))))

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
    print('Starting rainbow mode...')
    try:
        s = time.time()
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        print("Initialized bulbs ({}s)".format(str(round(time.time()-s, 2))))

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

def strobe_mode(client, macs, color='FFFFFF', brightness=100, duration=99999):
    print('Starting strobe mode')
    try:
        s = time.time()
        bulbs = get_bulbs_info(client, macs=macs)
        set_brightness_threaded(client, bulbs, brightness)
        set_color_threaded(client, bulbs, color)
        print("Initialized bulbs ({}s)".format(str(round(time.time() - s, 2))))

        start = time.time()

        on = False
        while time.time() - start < duration:
            threads = list()

            for bulb in bulbs:
                t = threading.Thread(target=set_on if on else set_off, args=(client, bulb,), daemon=True)
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


if __name__ == "__main__":
    client = get_client()

    if True:
        party_mode(client, macs=Lights.LIVING_ROOM)
    else:
        lis = get_bulbs_info_json(client)
        print(lis)