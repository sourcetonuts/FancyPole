import time
import board
import microcontroller
import touchio
from digitalio import DigitalInOut, Direction, Pull
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
led_brightness = 0.25 # fraction of full power (TBD mamps
pin_leddata = board.D4
pin_touch = board.A0
pin_status = board.D13
print( "FancyPole" )

strip = neopixel.NeoPixel( pin_leddata, num_pixels, brightness = led_brightness, auto_write = False )
touch = touchio.TouchIn( pin_touch )
status = DigitalInOut( pin_status )
status.direction = Direction.OUTPUT

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors

# across the rainbow
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]

# nice set of orange
#grad = [ (0.0,0x708800), (0.1,0x305500), (0.5,0x001100), (0.9,0x305500), (1.0,0x708800)]

# shades of gray
#grad = [ (0.0,0xf0f0f0), (0.5,0x101010), (1.0,0xf0f0f0)]

# gold
#grad = [ (0.0,0xffdf00), (0.5,0xc5b358), (1.0,0xffdf00)]


palette = fancy.expand_gradient( grad, 20 )

# todo read in these as stored from NVM or Drive or ?
onoff = True
offset = 0.001

def show_static() :
    print("show_static()")
    # pick the center color and fill the strip with that color statically displayed
    colorindex = offset + 0.5
    color = fancy.palette_lookup( palette, colorindex )
    strip.fill( color.pack() )
    strip.show()
    print( "offset: {}".format(offset) )
    microcontroller.nvm[0] = int( offset * num_pixels ) % num_pixels

def remember_settings() :
    stored = microcontroller.nvm[0]
    print("remember_settings({})".format(stored) )
    if stored == 0 :
        onoff = True
        offset = 0.001
    elif stored > num_pixels :
        onoff = True
        offset = 0.001
    else :
        onoff = False
        offset = stored / num_pixels
        show_static()

def palette_cycle() :
    for i in range( num_pixels ):
        colorindex = offset + ( i / num_pixels )
        color = fancy.palette_lookup( palette, colorindex )
        strip[i] = color.pack()
        if touch.value :
            return
    strip.show()

def restart_rainbow() :
    print("restart_rainbow()")
    # flash back before starting rainbow
    #strip.fill( (0,0,0) )
    #strip.show()

remember_settings()
status.value = onoff

# Loop Forever
while True :
    if onoff :
        # cycle the rainbow when on
        palette_cycle()
        offset += 0.035 # this sets how quickly the rainbow changes (bigger is faster)

    # deal w/ button presses...
    wason = not touch.value
    time.sleep(0.005)  # 5ms delay for debounce
    if not wason and touch.value :
        # just touched mode button
        time.sleep(0.005)  # 5ms delay for debounce
        onoff = not onoff # toggle onoff state
        status.value = onoff

        if onoff :
            # when just on restart color cycling
            restart_rainbow()
            microcontroller.nvm[0] = 0 # zero offset stored changing rainbow is active
        else :
            # and if just off just off paint/fill w/ the center color
            show_static()

        time.sleep( 0.5 )  # big delay so we dont 2x trigger button presses