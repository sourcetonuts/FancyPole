import time
import board
import touchio
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

num_pixels = 96

strip = neopixel.NeoPixel(
    board.D4, num_pixels, brightness = 0.1,
    auto_write = False, pixel_order= neopixel.RGB )

print( "FancyPole #1 Trinket M0" )

class RainMan :
    def __init__( self, strip ) :
        # refer to
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
        # across the rainbow
        self.strip = strip
        self.lookup = []
        self.size = ( strip.n ) / 2

        grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
        palette = fancy.expand_gradient( grad, 20 )
        for index in range(self.size) :
            coloff = index / self.size
            rgb = fancy.palette_lookup( palette, coloff )
            color = rgb.pack()
            self.lookup.append( color )
        # delete to free memory grad and palette we don't them any longer
        del grad
        del palette

    def color_selected( self, coloff ) :
        coloff = coloff % 1
        colindex = int( coloff * self.size )
        return self.lookup[colindex]

    def show_static( self, coloff ) :
        color = self.color_selected( coloff )
        strip.fill( color )
        strip.show()

#    def show_static_white( self ) :
#        if strip.bpp == 4 :
#            strip.fill((255,255,255,255))
#        else :
#            strip.fill((255,255,255))
#        strip.show()

    def palette_cycle( self, coloff ) :
        for index in range( num_pixels ) :
            offset = coloff + ( index / num_pixels )
            rgb = self.color_selected( offset % 1 )
            strip[index] = rgb
        strip.show()

display = RainMan( strip )

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

inputMode = touchio.TouchIn( board.A0 )
modeMachine = TouchMode( inputMode, 2 )

offset = 0

# Loop Forever
while True :
    mode = modeMachine.update()
    if mode == 0 :
        display.palette_cycle( offset )
        offset += 0.005 # 0.035 # this sets how quickly the rainbow changes (bigger is faster)
    else :
        # and if just off just off paint/fill w/ the center color
        display.show_static( offset + 0.5 )

# end of program