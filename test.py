import radio
from microbit import *
from random import randint
from math import pow

def cur_time():
    return round(running_time()/1000)

img = '09990:99000:99990:99990:09090'
radio.on()
radio.config(power=0, channel=0, queue=1)
channel = 0
while True:
    message = radio.receive()
    if message == 'ping':
        radio.config(channel=0)
        display.show(Image.YES)
        radio.send('occupied')
        display.clear()
        sleep(100)
        display.show(Image.YES)
        radio.send('occupied')
        display.clear()
        radio.config(channel=channel)

    # If the message is 'code', display the image on screen
    if message == 'code':
        display.show(Image(img))
    display.clear()

    if button_a.is_pressed():
        print('channel', channel)
        if channel != 0:
            radio.send('code')
        else:
            display.show(Image.NO)
            continue
    
    if button_b.was_pressed():
        sleep(randint(60, 90))
        channel = 0
        radio.config(channel=0)
        radio.send(str(cur_time()))
        sleep(500)
        message = radio.receive()
        print('message', message)
        if message == None or not message.isdigit():
            print('is not dig')
            continue
        print('is dig')
        dif = cur_time()-int(message)
        print('cur', cur_time())
        print('rec', message)
        print('dif', dif)
        if dif in range(-1, 2):
            print('yes')
            msg_bank = []
            # sleep(pow(randint(5, 25), 2))
            for i in range(1, 84):
                radio.config(channel=i)
                sleep(90)
                radio.send('ping')
                sleep(90)
                nxt_msg = radio.receive()
                if nxt_msg != None and nxt_msg != 'ping':
                    msg_bank.append(i)
            radio.config(channel=0)
            print('bank', msg_bank)
            for i in range(1, 84*2):
                if i not in msg_bank:
                    sleep(1000)
                    radio.config(channel=i)
                    channel = i
                    break
        else:
            print('no')
        

    
    # sleep(500)