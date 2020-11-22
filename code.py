import board
import touchio
import neopixel

print( "FancyPole #2 Trinket M0" )

# make the strip and here a 96 LED NeoPixel strip (can be dotstar, etc. w/ libraries)
strip = neopixel.NeoPixel(
    board.D4, 96, brightness = 0.25,
    auto_write = False, pixel_order= neopixel.RGBW )

# Kenny's Display classs, It uses strip passed and libraries: adafruit_fancyled
import MyPy.rainman
display = MyPy.rainman.RainMan( strip )

# Kenny's TouchMode class, It uses touchio passed and libraries: time
import MyPy.touchmode

# handles the application's Mode:
# 0:rainbow select
# 1:display selected color
inputMode = touchio.TouchIn( board.A0 )
modeMachine = MyPy.touchmode.TouchMode( inputMode, 2 )

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