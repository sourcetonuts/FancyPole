import time
import board
import touchio
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

num_pixels = 30

# pin usage: TRINKET: board.D4, GEMMA: board.D1
strip = neopixel.NeoPixel( board.D4, num_pixels, brightness = 0.25, auto_write = False )

print( "FancyPole Gemma M0" )

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
# across the rainbow
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
palette = fancy.expand_gradient( grad, 20 )

#
# returns the mid color in the palette
# which we call the selected color
#
def color_selected( coloff ) :
    # pick the center color and fill the strip with that color statically displayed
    colorindex = coloff + 0.5
    color = fancy.palette_lookup( palette, colorindex )
    return color.pack()

#
# sets the strip to the color offset into the palette
#
def show_static( coloff ) :
    rgb = color_selected( coloff )
    strip.fill( rgb )
    strip.show()

#
# cycles through the palette starting w/ an offset into the palette
# show all of the palette, so loops back to the start based on the
# starting offset
#
def palette_cycle( coloff ) :
    for i in range( num_pixels ) :
        colorindex = coloff + ( i / num_pixels )
        color = fancy.palette_lookup( palette, colorindex )
        rgb = color.pack()
        strip[i] = rgb
    strip.show()

# TouchMode
# this class manages a single captouch pin and cycles through modes
# on that pin up to provided lastmode
#
class TouchMode :
    def __init__( self, inputMode, num = 2, name = None ) :
        self.value = 0
        self.lastmode = num - 1
        self.input = inputMode
        self.name = name or "mode"

    def update( self ) :
        wasoff = not self.input.value
        time.sleep(0.005)  # 5ms delay for debounce
        if not wasoff and self.input.value :
            # just touched button
            time.sleep(0.005)  # 5ms delay for debounce
            if self.value >= self.lastmode :
                self.value = 0
            else :
                self.value = self.value + 1
            # debounce
            time.sleep( 0.5 )
            print( self.name + " {}".format( self.value ) )
        return self.value

# OnOff pin usage: TRINKET: board.A0, GEMMA: board.A1
# Mode pin usage: TRINKET: board.A3, GEMMA: board.A2

inputOnOff = touchio.TouchIn( board.A0 )
onoffMachine = TouchMode( inputOnOff, 2, "onoff" )
inputMode = touchio.TouchIn( board.A3 )
modeMachine = TouchMode( inputMode, 3 )

OnOff = True
offset = 0.001
mode = 0

# Loop Forever
while True :
    OnOff = onoffMachine.update()
    if OnOff == 0 :
        palette_cycle( offset )
        offset += 0.035 # this sets how quickly the rainbow changes (bigger is faster)
    else :
        newmode = modeMachine.update()
        if mode != newmode :
            mode = newmode

        if mode == 0 :
            # and if just off just off paint/fill w/ the center color
            show_static( offset )
        else :
            show_static( offset )