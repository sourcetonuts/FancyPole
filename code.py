import time
import board
import touchio

import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

# with the following 96 LED setup on an Adafruit Trinket M0
# it could be wired up to run off of a basic/standard USB charger or laptop
# cabling required for Trinket
#   USB micro for power
#   pin 1 to touch button/copper pad
#   pin 4 to NeoPixel data input pin
#   along with USB and GND from the Trinket for NeoPixel power/ground/data-in 3 conductor cable

num_pixels = 96
led_brightness = 0.1 # mamps
pin_leddata = board.D4
pin_touch = board.A0

strip = neopixel.NeoPixel( pin_leddata, num_pixels, brightness = led_brightness, auto_write = False )
touch = touchio.TouchIn( pin_touch )

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
#
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
palette = fancy.expand_gradient( grad, 50 )

# todo read in these as stored from NVM or Drive or ?
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
        # just touched mode button
        onoff = not onoff # toggle onoff state

        # when off paint/fill w/ the center color
        if onoff :
            # flash back before starting rainbow
            strip.fill( (0,0,0) )
            strip.show()
            offset = 0
        else :
            # pick the center color and fill the strip with that color statically displayed
            colorindex = offset + 0.5
            color = fancy.palette_lookup( palette, colorindex )
            strip.fill( color.pack() )
            strip.show()

        time.sleep( 0.5 )  # big delay so we dont 2x trigger