from machine import Pin
import time
import keyboard

# Configuración de pines
PIN_A = 3
PIN_B = 2
PIN_BUTTON = 0

# Configuración de pines como entrada
pin_a = Pin(PIN_A, Pin.IN)
pin_b = Pin(PIN_B, Pin.IN)
pin_button = Pin(PIN_BUTTON, Pin.IN)

# Variables para el estado del encoder
encoder_posicion = 0
pin_a_estado_anterior = pin_a.value()

def manejar_cambio(pin):
    global encoder_posicion
    global pin_a_estado_anterior

    pin_a_estado = pin_a.value()
    pin_b_estado = pin_b.value()

    if pin == pin_a and pin_a_estado != pin_a_estado_anterior:
        if pin_b_estado != pin_a_estado:
            encoder_posicion += 1
            keyboard.press_and_release('right')
        else:
            encoder_posicion -= 1
            keyboard.press_and_release('left')

    pin_a_estado_anterior = pin_a_estado

def manejar_click(pin):
    if pin() == 0:  # Verifica si el botón está presionado
        keyboard.press_and_release('enter')

# Configurar interrupciones
pin_a.irq(trigger=Pin.IRQ_BOTH, handler=manejar_cambio)
pin_b.irq(trigger=Pin.IRQ_BOTH, handler=manejar_cambio)
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=manejar_click)

try:
    while True:
        # Tu código principal aquí
        time.sleep(0.1)

except KeyboardInterrupt:
    # Manejar la interrupción de teclado (Ctrl+C)
    pass
