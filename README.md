# flotillascratch
Use Pimoroni Flotilla with Scratch 1.4 on the Pi with ScratchPy

A way to allow kids to program with the awesome Flotilla dock and modules using Scratch 1.4 on a Raspberry Pi.

## Setup

First you'll need to install [flotilla-python](https://github.com/pimoroni/flotilla-python/) and [ScratchPy](https://github.com/pilliq/scratchpy).

If you've installed Flotilla Rockpool follow the Flotilla Python instructions to make sure the daemon is not running (you'll need to do this everytime you reboot the Pi.)

Download or clone this project. 

## Trying the Demos

Open one of the Demo projects in Scratch, the image on the Stage will show you which modules to connect to the Flotilla Dock. 

Click on 'Sensing' and then right-click on the 'sensor value' block and choose 'enable remote sensor connections'

Open Programming->Python2 (IDLE)

Open flotillascratch.py and run it - you can use F5. 

Now go back to Scratch and try out the project. 

If you change the modules plugged in to the dock you can just return to IDLE and press F5. 

(You can also run the script from the command line.)

More info at [Flotilla with Scratch 1.4](http://www.techagekids.com/2017/02/flotilla-with-scratch-14-on-raspberry-pi.html)

## Create your Own Project

In Scratch, click on 'Sensing' and then right-click on the 'sensor value' block and choose 'enable remote sensor connections'. 

Connecting an **input module** to the Flotilla Dock and then running flotillascratch.py will automatically create 'sensor value' entries for the module. 

To update an **output module** you need to create specific global (for all sprites) variables:
+ Number: number1 (a number or text string)
+ Matrix: matrix1 (a string of 8 digits corresponding to a bar graph, e.g. 1 2 3 4 5 6 7)
+ Rainbow: rainbow1.red, rainbow1.blue, rainbow1.green (values 0-255), rainbow1.brightness

If you have more that one module of a particular type then use rainbow2 etc. 

## Limitations

You can only control all the pixels on a Rainbow together at the moment and there's limited support for the Matrix. Will add these when I think of a simple way to do it from Scratch. 

Can't set brightness on Number and Matrix (will add)

No requirements checking for modules. 

No automatic updating of available modules in Scratch (but this may be possible.)

Lots more it could do, but hopefully this is a useful start. 

## License

MIT

