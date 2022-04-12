import radio
from microbit import *
from random import randint

def cur_time():
    return round(running_time()/1000)

img = '09990:99000:99990:99990:09090'
radio.on()
radio.config(power=0, channel=0, queue=80)
cur_freq = 0
while True:
    message = radio.receive()
    if message == 'ping':
        radio.send(str(cur_freq))

    if message != None and message[:3] == 'join':
        content = message.split('-')
        dif = cur_time()-int(content[1])
        if dif in range(-2, 3):
            cur_freq = int(content[2])
            radio.config(channel=1)
            print('caught up. cur freq', cur_freq)

    if message != None and message.isdigit() and int(message) == cur_freq:
        display.show(Image(img))
    display.clear()

    if button_a.is_pressed():
        if cur_freq > 0:
            radio.send(str(cur_freq))
        else:
            display.show(Image.NO)
            continue
    
    
    if button_b.was_pressed():
        cur_freq = 0
        radio.config(channel=0)
        sleep(randint(125, 250))
        radio.send(str(cur_time()))
        sleep(500)
        message = radio.receive()
        print('message', message)
        if message == None or not message.isdigit():
            display.show(Image.SAD)
            sleep(500)
            continue
        dif = cur_time()-int(message)
        if dif in range(-2, 3):
            msg_bank = []
            radio.config(channel=1)
            radio.send('ping')
            sleep(1000)
            while True:
                nxt_msg = radio.receive()
                print('message', nxt_msg)
                if nxt_msg != None and nxt_msg != 'ping' and '-' not in nxt_msg:
                    radio.send(nxt_msg)
                    print('added')
                    msg_bank.append(nxt_msg)
                elif nxt_msg == None:
                    break
            print('bank', msg_bank)
            for i in range(1, len(msg_bank)+2):
                print('i', i)
                if str(i) not in msg_bank:
                    print('free')
                    display.show(Image.YES)
                    sleep(1000)
                    cur_freq = i
                    print('cur_freq', i)
                    sleep(500)
                    radio.config(channel=0)
                    radio.send('join-'+str(cur_time())+'-'+str(i))
                    radio.config(channel=1)
                    break