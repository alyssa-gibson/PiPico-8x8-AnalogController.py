from machine import Pin, ADC, PWM
import time, utime

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(16,Pin.IN, Pin.PULL_UP)

sdi = machine.Pin(18,machine.Pin.OUT)
rclk = machine.Pin(19,machine.Pin.OUT)
srclk = machine.Pin(20,machine.Pin.OUT)

glyph_x = [0xFF,0xBB,0xD7,0xEF,0xD7,0xBB,0xFF,0xFF]
arrow_r = [0xFF,0xEF,0xC7,0xAB,0xEF,0xEF,0xEF,0xFF]
arrow_l = [0xFF,0xEF,0xEF,0xEF,0xAB,0xC7,0xEF,0xFF]
arrow_u = [0xFF,0xEF,0xDF,0x81,0xDF,0xEF,0xFF,0xFF]
arrow_d = [0xFF,0xF7,0xFB,0x81,0xFB,0xF7,0xFF,0xFF]

# Shift the data to 74HC595
def hc595_in(dat):
    for bit in range(7,-1, -1):
        srclk.low()
        time.sleep_us(30)
        sdi.value(1 & (dat >> bit))
        time.sleep_us(30)
        srclk.high()

def hc595_out():
    rclk.high()
    time.sleep_us(200)
    rclk.low()

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()
    xStatus = "middle"
    yStatus = "middle"
    buttonStatus = "not pressed"
    if xValue <= 600:
        xStatus = "left"
        for i in range(0,8):
            hc595_in(arrow_l[i])
            hc595_in(0x80>>i)
            hc595_out()
    elif xValue >= 60000:
        xStatus = "right"
        for i in range(0,8):
            hc595_in(arrow_r[i])
            hc595_in(0x80>>i)
            hc595_out()
    if yValue <= 600:
        yStatus = "up"
        for i in range(0,8):
            hc595_in(arrow_u[i])
            hc595_in(0x80>>i)
            hc595_out()
    elif yValue >= 60000:
        yStatus = "down"
        for i in range(0,8):
            hc595_in(arrow_d[i])
            hc595_in(0x80>>i)
            hc595_out()
    if buttonValue == 0:
        buttonStatus = "pressed"