from machine import Pin, PWM
import time
import sys
import struct
from machine import SoftI2C

# ── Configuración I2C y ADS1115 ──────────────────────────
I2C_SDA = 21
I2C_SCL = 22
ADS_ADDR = 0x48

i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)

def ads_read_voltage():
    config = 0xC3E3
    i2c.writeto_mem(ADS_ADDR, 0x01, struct.pack('>H', config))
    time.sleep_ms(10)
    raw = struct.unpack('>h', i2c.readfrom_mem(ADS_ADDR, 0x00, 2))[0]
    voltage = raw * 4.096 / 32767
    return round(voltage, 4)

# ── Configuración PWM ─────────────────────────────────────
BUZZER_PIN = 25
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty(0)  # ← empieza apagado

print("ESP32 listo.")

# ── Bucle principal ───────────────────────────────────────
while True:
    try:
        line = sys.stdin.readline().strip()  # ← cambiado de input() a readline()
        
        if line == "STOP":
            buzzer.duty(0)
            print("STOP recibido")
            continue

        if "," in line:
            parts = line.split(",")
            freq = int(parts[0])
            dur  = int(parts[1])

            if freq == 0:
                buzzer.duty(0)          # silencio
            else:
                buzzer.freq(freq)
                buzzer.duty(512)        # suena

            v = ads_read_voltage()
            print("FREQ:{} V:{}".format(freq, v))

            time.sleep_ms(dur)
            buzzer.duty(0)              # ← apaga al terminar cada nota

    except Exception as e:
        buzzer.duty(0)
        print("Error: {}".format(e))