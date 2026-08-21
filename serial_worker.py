import serial
import time
from pynput.keyboard import Controller, Key
from parser import parse_weight

keyboard = Controller()

running = False
ser = None


def start_serial(port, baudrate, databits, parity, stopbits, callback_log):
    global running, ser
    running = True

    bytesize_map = {
        "5": serial.FIVEBITS,
        "6": serial.SIXBITS,
        "7": serial.SEVENBITS,
        "8": serial.EIGHTBITS
    }

    parity_map = {
        "None": serial.PARITY_NONE,
        "Even": serial.PARITY_EVEN,
        "Odd": serial.PARITY_ODD
    }

    stopbits_map = {
        "1": serial.STOPBITS_ONE,
        "1.5": serial.STOPBITS_ONE_POINT_FIVE,
        "2": serial.STOPBITS_TWO
    }

    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize_map[databits],
            parity=parity_map[parity],
            stopbits=stopbits_map[stopbits],
            timeout=1
        )
    except Exception as e:
        callback_log(f"Błąd: {e}")
        running = False
        return

    while running:
        try:
            if ser.in_waiting > 0:
                raw = ser.read(ser.in_waiting).decode(errors="ignore")
                for line in raw.splitlines():
                    value = parse_weight(line)
                    if value:
                        callback_log(value)

                        for c in value:
                            keyboard.press(c)
                            keyboard.release(c)
                            time.sleep(0.02)

                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)

        except Exception:
            callback_log("Rozłączono urządzenie...")
            break

    if ser:
        ser.close()


def stop_serial():
    global running
    running = False