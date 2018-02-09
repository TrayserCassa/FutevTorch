# Futev Torch Lib 

This library is written in Python3 and used the pip3 package 
https://pypi.python.org/pypi/rpi_ws281x/1.1.0

So install this Lib with 
>> sudo pip3 install rpi_ws281x



Basic Usage:

>>      torch = FutevTorch()
        torch.run_pulse(255,0,255)
        print("Pulse")
        sleep(3)
        torch.stop()

        torch.run_rainbow()
        print("Rainbow")
        sleep(3)
        torch.stop()

        torch.run_blink_short(255,0,0, intervall=10)
        print("blink short")
        sleep(3)
        torch.stop()

        torch.run_blink_long(0,0,255)
        print("blink long")
        sleep(3)
        torch.stop()
