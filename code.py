import time
import board
import touchio

import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

num_pixels = 96
strip = neopixel.NeoPixel( board.D4, num_pixels, brightness=0.05, auto_write=False )
touch = touchio.TouchIn( board.A0 )

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
#
palette = [fancy.CHSV(1.0, 1.0, 1.0),
           fancy.CHSV(0.8, 1.0, 1.0),
           fancy.CHSV(0.3, 1.0, 1.0),
           fancy.CHSV(0.0, 1.0, 1.0),
           fancy.CHSV(0.3, 1.0, 1.0),
           fancy.CHSV(0.8, 1.0, 1.0)]

grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
#grad = [(0.0, 0x97461A), (0.3, 0xFBD8C5), (0.83, 0x6C2E16), (1.0, 0xEFDBCD)]
palette = fancy.expand_gradient( grad, 50 )

onoff = True
offset = 0

def palette_cycle() :
    for i in range( num_pixels ):
        colorindex = offset + ( i / num_pixels )
        color = fancy.palette_lookup( palette, colorindex )
        strip[i] = color.pack()
        if touch.value :
            return
    strip.show()

while True :
    if onoff :
        palette_cycle()
        offset += 0.025

    # deal w/ switching modes
    wason = not touch.value

    time.sleep(0.005)  # 5ms delay
    if not wason and touch.value :
        onoff = not onoff # toggle onoff state

        # when off paint/fill w/ the center color
        if not onoff :
            colorindex = offset + 0.5
            color = fancy.palette_lookup( palette, colorindex )
            strip.fill( color.pack() )
            strip.show()

        time.sleep(0.5)  # big delay so we dont 2x trigger