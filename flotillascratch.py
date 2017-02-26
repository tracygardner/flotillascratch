# Copyright (C) 2017 Tracy Gardner

import scratch
import flotilla
import time
import thread

s = scratch.Scratch()
client = flotilla.Client()

inputs = {}
outputs = {}


# Detect the modules connected to the Dock and create corresponding
# inputs and outputs
        
def updatemodules():

    dial = slider = touch = light = joystick = colour = weather = motion = rainbow = 1
    number = matrix = motor = 1

    inputs.clear()
    outputs.clear()
    
    for module in client.available.values():
        print module.name
       
        if module.is_a(flotilla.Dial):
            inputs['dial' + str(dial)] = [-1, module, flotilla.Dial.position.fget]
            dial +=1
        elif module.is_a(flotilla.Slider):
            inputs['slider' + str(slider)] = [-1, module, flotilla.Slider.position.fget]
            slider +=1
        elif module.is_a(flotilla.Touch):
            inputs['touch' + str(touch) + '.one'] = [-1, module, flotilla.Touch.one.fget]
            inputs['touch' + str(touch) + '.two'] = [-1, module, flotilla.Touch.two.fget]
            inputs['touch' + str(touch) + '.three'] = [-1, module, flotilla.Touch.three.fget]
            inputs['touch' + str(touch) + '.four'] = [-1, module, flotilla.Touch.four.fget]
            touch +=1
        elif module.is_a(flotilla.Light):
            inputs['light' + str(light)] = [-1, module, flotilla.Light.light.fget]
            light +=1
        elif module.is_a(flotilla.Joystick):
            inputs['joystick' + str(joystick) + '.x'] = [-1, module, flotilla.Joystick.x.fget]
            inputs['joystick' + str(joystick) + '.y'] = [-1, module, flotilla.Joystick.y.fget]
            joystick +=1
        elif module.is_a(flotilla.Weather):
            inputs['weather' + str(weather) + '.temperature'] = [-1, module, flotilla.Weather.temperature.fget]
            inputs['weather' + str(weather) + '.pressure'] = [-1, module, flotilla.Weather.pressure.fget]
            weather +=1
        elif module.is_a(flotilla.Motion):
            inputs['motion' + str(motion) + '.x'] = [-1, module, flotilla.Motion.x.fget]
            inputs['motion' + str(motion) + '.y'] = [-1, module, flotilla.Motion.y.fget]
            inputs['motion' + str(motion) + '.z'] = [-1, module, flotilla.Motion.z.fget]
            motion +=1
        elif module.is_a(flotilla.Colour):
            inputs['colour' + str(colour) + '.red'] = [-1, module, flotilla.Colour.red.fget]
            inputs['colour' + str(colour) + '.green'] = [-1, module, flotilla.Colour.green.fget]
            inputs['colour' + str(colour) + '.blue'] = [-1, module, flotilla.Colour.blue.fget]
            inputs['colour' + str(colour) + '.clear'] = [-1, module, flotilla.Colour.clear.fget]
            colour +=1
        elif module.is_a(flotilla.Number):
            outputs['number' + str(number)] = module
            number +=1
        elif module.is_a(flotilla.Rainbow):
            outputs['rainbow' + str(rainbow)] = module
            rainbow +=1
        elif module.is_a(flotilla.Matrix):
            outputs['matrix' + str(matrix)] = module
            matrix +=1
        elif module.is_a(flotilla.Motor):
            outputs['motor' + str(motor)] = module
            motor +=1
            

# Listen for events from Scratch
def listen():
    while True:
        try:
            yield s.receive()
        except scratch.ScratchError:
            raise StopIteration

# Check whether an input has changed and if so send the value to Scratch
def checkInput(key):
    if inputs[key][1] is not None:
        value = inputs[key][2](inputs[key][1])
        if value != inputs[key][0] :
            inputs[key][0] = value
            s.sensorupdate({key : value})

# Check inputs on separate thread    
def checkInputs(threadName, delay):
    while True:
        for input in inputs.keys():
            checkInput(input)
        
        time.sleep(delay)

try:
    
    updatemodules()

    try: 
        thread.start_new_thread (checkInputs, ('Inputs', 0.1))
    except:
       print 'Error: unable to start thread'

    for msg in listen():
        if msg is None:
            break
        if msg[0] == 'broadcast':
            print(msg);
            if msg[1] == 'updatemodules':
                # Detect modules currently attached to the dock
                updatemodules()
        elif msg[0] == 'sensor-update':
            toupdate = msg[1]
            for k, v in toupdate.iteritems():
                try: 
                    if k.startswith('number'):
                        try:                      
                            outputs[k].set_number(v)
                            outputs[k].update()
                        except:
                            outputs[k].set_string(v)
                            outputs[k].update()
                    elif k.startswith('rainbow'):
                        rainbown, dot, prop = k.partition('.')
                        rainbow = outputs[rainbown]
                        if prop == 'set':
                            print 'setting to ', v
                            outputs[rainbown][1] = v
                        elif prop == 'brightness':
                            rainbow.set_brightness(v)
                        elif prop == 'red':       
                             pixel = rainbow.pixels[0]
                             rainbow.set_all(v, pixel[1], pixel[2])
                        elif prop == 'green':
                            pixel = rainbow.pixels[0]
                            rainbow.set_all(pixel[0], v, pixel[2])                       
                        elif prop == 'blue':                      
                            pixel = rainbow.pixels[0]
                            rainbow.set_all(pixel[0], pixel[1], v)                       
                        rainbow.update()
                    elif k.startswith('matrix'):
                        bars = v.split()
                        outputs[k].clear()
                        for bar, val in enumerate(bars):
                            for i in range(0, int(val)):
                                outputs[k].set_pixel(int(bar), 7-i, True).update()
                    elif k.startswith('motor'):
                        outputs[k].set_speed(v)
                except:
                    print 'Problem setting ', k, ' to ', v
                        
except KeyboardInterrupt:
    s.disconnect()
    client.stop()
                            

                
