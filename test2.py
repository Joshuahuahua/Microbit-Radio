import radio
from microbit import *
from random import randint

def cur_time():
    return round(running_time()/1000)

def send(type, value = 0):
    radio.send(type+':'+str(value)+':'+str(cur_time()))

def listen():
    message = radio.receive()
    if message == None:
        return ['None', 0, 0]
    else:
        print('b4', message)
        temp = message.split(':')
        print('aftr', temp)
        temp[1] = int(temp[1])
        temp[2] = int(temp[2])
        return temp

img = '09990:99000:99990:99990:09090'

radio.on()
radio.config(power=4, channel=0, queue=80)
cur_freq = 0
while True:
    message = listen()

    if message[0] == 'ping':
        send('pong', cur_freq)

    if message[0] == 'join':
        dif = cur_time()-message[2]
        if dif in range(-2, 3):
            cur_freq = message[1]
            radio.config(channel=1)
            #print('caught up. cur freq', cur_freq)

    if message[0] == 'code' and message[1] == cur_freq:
        display.show(Image(img))

    if button_a.is_pressed():
        if cur_freq > 0:
            send('code', cur_freq)
        else:
            display.show(Image.NO)
            continue
    
    
    if button_b.was_pressed():
        cur_freq = 0
        radio.config(channel=0)

        sleep(randint(125, 250))
        
        send('pair')
        sleep(500)
        message = listen()
        #print('message', message)
        if message[0] != 'pair':
            display.show(Image.SAD)
            sleep(500)
            continue

        dif = cur_time()-message[2]
        if dif in range(-2, 3):
            msg_bank = []
            radio.config(channel=1)
            send('ping')
            sleep(60)
            while True:
                nxt_msg = listen()
                #print('message', nxt_msg)
                if nxt_msg[0] == 'pong' and nxt_msg[1] not in msg_bank:
                    send('pong', nxt_msg[1])
                    #print('added')
                    msg_bank.append(nxt_msg[1])
                elif nxt_msg[0] == 'None':
                    break

            #print('bank', msg_bank)
            for i in range(1, len(msg_bank)+2):
                #print('i', i)
                if i not in msg_bank:
                    #print('free')
                    display.show(Image.YES)
                    sleep(1000)
                    cur_freq = i
                    #print('cur_freq', i)
                    sleep(500)
                    radio.config(channel=0)
                    send('join')
                    radio.config(channel=1)
                    break
    
    display.clear()    