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
        else :
            # pick the center color and fill the strip with that color statically displayed
            colorindex = offset + 0.5
            color = fancy.palette_lookup( palette, colorindex )
            strip.fill( color.pack() )
            strip.show()

        time.sleep( 0.5 )  # big delay so we dont 2x trigger