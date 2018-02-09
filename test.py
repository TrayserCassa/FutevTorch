#!/usr/bin/python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from rpi_ws281x import *
from threading import Thread

class FutevTorch():
        def __init__(self, pin=18, frequency=800000, dma=5, brightness=255):
                self.__pin = pin
                self.__frequency = frequency
                self.__dma = dma
                self.__brightness = brightness

        def __init_torch(self):
                self.__thread = FutevTorchThread(self.__pin, self.__frequency, self.__dma, self.__brightness)

        def run_pulse(self, red, green, blue, intervall=0.005):
                self.__init_torch()
                self.__thread.set_color(red, green, blue)
                self.__thread.run_pulse(intervall)
                print("Run pulse")


        def run_rainbow(self, intervall=0.02):
                self.__init_torch()
                self.__thread.run_rainbow(intervall)
                print("Run rainbow")
                
        def stop(self):
                self.__thread.stop()
                self.__thread.join()


class FutevTorchThread(Thread):
        def __init__(self, pin=18, frequency=800000, dma=5, brihtness=255):
                Thread.__init__(self)
                self.__strip = PixelStrip(1, pin, frequency, dma, False, brihtness)
                self.__strip.begin()

                self.__red = 0
                self.__green = 0
                self.__blue = 0

                self.__mode = ""
                self.__pulse_intervall = 0
                self.__rainbow_intervall = 0
                

        def run_pulse(self, intervall):
                self.__mode = "pulse"
                self.__pulse_intervall = intervall
                self.start()

        def __show_pulse(self):
                while not self.__stop:
                        self.__smooth_start(self.__pulse_intervall)
                        self.__smooth_stop(self.__pulse_intervall)

        def run_rainbow(self, intervall):
                self.__mode = "rainbow"
                self.__rainbow_intervall = intervall
                self.start()

        def __show_rainbow(self):
                self.set_color(0, 255, 0)
                self.__smooth_start(0.005)
                while not self.__stop:
                        for i in range(255):                                
                                red, green, blue = self.__wheel((i) & 255) 
                                self.set_color(red, green, blue)
                                self.__show()
                                time.sleep(self.__rainbow_intervall)
                        print("done in rainbow")
                
                self.__smooth_stop(0.005)

        def __wheel(self, position):
	        if position < 85:
		        return position * 3, 255 - position * 3, 0
	        elif position < 170:
		        position -= 85
		        return 255 - position * 3, 0, position * 3
	        else:
		        position -= 170
		        return 0, position * 3, 255 - position * 3
                
                
        def set_color(self, red, green, blue):
                self.__red = red
                self.__green = green
                self.__blue = blue

        def run(self):
                self.__stop = False

                if self.__mode == "pulse":
                        self.__show_pulse()

                elif self.__mode == "rainbow":
                        self.__show_rainbow()
                        
                print("finished")

        def __show(self):
                self.__strip.setPixelColorRGB(0, self.__red, self.__green, self.__blue)
                self.__strip.show()

        def stop(self):
                print("do stop")
                self.__stop = True

        def __smooth_start(self, intervall = 0.002):
                self.__strip.setPixelColorRGB(0, self.__red, self.__green, self.__blue)
                for i in range(0, 255, 1):
                        self.__strip.setBrightness(i)
                        self.__strip.show()
                        time.sleep(intervall)
                
        def __smooth_stop(self, intervall = 0.002):
                for i in range(255, 0, -1):
                        self.__strip.setBrightness(i)
                        self.__strip.show()
                        time.sleep(intervall)

                        
if __name__ == '__main__':
        torch = FutevTorch()
        torch.run_pulse(255,0,255)
        print("warte 3 sekunden dann sollte das aufhören")
        time.sleep(3)
        torch.stop()
        torch.run_rainbow()
        print("warte 3 sekunden dann sollte das aufhören")
        time.sleep(3)
        torch.stop()
