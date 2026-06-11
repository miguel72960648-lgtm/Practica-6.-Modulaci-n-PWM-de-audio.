import serial
import time

# ─────────────────────────────────────────────────────────
# CONFIGURACIÓN
PORT     = "COM6"
BAUDRATE = 115200
# ─────────────────────────────────────────────────────────

# Notas de "Estrellita ¿Dónde Estás?" (Twinkle Twinkle Little Star)
# Formato: (frecuencia_Hz, duración_ms)
# 0 Hz = silencio

ESTRELLITA = [
    # "Es - tre - lli - ta  ¿dón - de  es - tás?"
    (262, 400), (262, 400), (392, 400), (392, 400),
    (440, 400), (440, 400), (392, 800),
    # "Yo  me  pre - gun - to  lo  que  e - res"
    (349, 400), (349, 400), (330, 400), (330, 400),
    (294, 400), (294, 400), (262, 800),
    # "En  el  cie - lo  y  en  el  mar"
    (392, 400), (392, 400), (349, 400), (349, 400),
    (330, 400), (330, 400), (294, 800),
    # "co - mo  es - tre - lla  bri - llan - te"
    (392, 400), (392, 400), (349, 400), (349, 400),
    (330, 400), (330, 400), (294, 800),
    # "Es - tre - lli - ta  ¿dón - de  es - tás?"
    (262, 400), (262, 400), (392, 400), (392, 400),
    (440, 400), (440, 400), (392, 800),
    # "Yo  me  pre - gun - to  lo  que  e - res"
    (349, 400), (349, 400), (330, 400), (330, 400),
    (294, 400), (294, 400), (262, 800),
]


def send_to_esp32(tones, port, baudrate):
    print(f"Conectando a {port}...")
    ser = serial.Serial(port, baudrate, timeout=2)
    time.sleep(2)

    print("Reproduciendo Estrellita...")
    for freq, dur in tones:
        cmd = f"{freq},{dur}\n"
        ser.write(cmd.encode())
        time.sleep(dur / 1000.0)

    ser.write(b"STOP\n")
    ser.close()
    print("Reproducción finalizada.")


if __name__ == "__main__":
    send_to_esp32(ESTRELLITA, PORT, BAUDRATE)