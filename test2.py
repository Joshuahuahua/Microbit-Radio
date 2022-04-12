import radio
from microbit import *
from random import randint

# Returns the time (in seconds) the microbit has been running.
def cur_time():
    return round(running_time()/1000)

# Formats the message to be sent (separates the 3 components with a ':')
def send(type, value = 0):
    radio.send(type+':'+str(value)+':'+str(cur_time()))

# Listens for sent messages and formats them into a 3-part array, delimiting by ':'
def listen():
    message = radio.receive()
    if message == None:
        return ['None', 0, 0]
    else:
        temp = message.split(':')
        temp[1] = int(temp[1])
        temp[2] = int(temp[2])
        return temp

# Turn on and configure the radio. Microbits join channel 0 when they are NOT paired.
radio.on()
radio.config(power=4, channel=0, queue=80)
# Set the current frequeny to 0. This represents the "frequency" the microbits pairs will communicate on.
cur_freq = 0

while True:
    # Listen for messages.
    message = listen()

    # If a ping is recieved, send back the frequency the microbit is running on.
    if message[0] == 'ping':
        send('pong', cur_freq)

    # If the microbit is instructed to join a channel;
    if message[0] == 'join':
        # Check the difference in runtimes.
        dif = cur_time()-message[2]
        # If the runtimes are the same (they have been paired)
        if dif in range(-2, 3):
            # Set the frequency to the one recieved.
            cur_freq = message[1]
            radio.config(channel=1)
            display.show(Image.YES)
            sleep(500)

    # If morse code was sent from a paired microbit (a microbit on the same frequency)
    if message[0] == 'code' and message[1] == cur_freq:
        # Light up :)
        display.show(Image('99999:99999:99999:99999:99999'))

    # If the user presses the left button (A)
    if button_a.is_pressed():
        # If the microbit has NOT been paired (frequency is 0)
        if cur_freq > 0:
            send('code', cur_freq)
        else:
            # If the microbit has NOT been paired (frequency is 0)
            display.show(Image.NO)
            continue
    
    # If the right button is pressed (B)
    if button_b.was_pressed():
        # (re)set the frequency and channel to 0
        cur_freq = 0
        radio.config(channel=0)

        # Sleep for a random duration of time.
        # This causes the microbits to desynchronize to avoid sending/recieving at the same time.
        sleep(randint(125, 250))
        
        # Send out a "pair" message tied with its internal clock
        send('pair')
        sleep(500)
        # Listen for the "pair" message.
        message = listen()
        # If it doesnt recieve the message, reset.
        if message[0] != 'pair':
            display.show(Image.SAD)
            sleep(500)
            continue
        
        # If the microbit receives the pair request
        dif = cur_time()-message[2]
        # Check if the clock times are the same (assumed to have been reset together)
        if dif in range(-2, 3):
            # Create an empty list and join channel 1
            msg_bank = []
            radio.config(channel=1)
            # Send out a ping to see what channels are being used.
            send('ping')
            sleep(60)
            while True:
                # Listen for responses and add the responses to the list.
                nxt_msg = listen()
                if nxt_msg[0] == 'pong' and nxt_msg[1] not in msg_bank:
                    send('pong', nxt_msg[1])
                    msg_bank.append(nxt_msg[1])
                elif nxt_msg[0] == 'None':
                    break

            # Pick a frequency that isn't being used.
            for i in range(1, len(msg_bank)+2):
                if i not in msg_bank:
                    display.show(Image.YES)
                    cur_freq = i
                    sleep(500)
                    
                    # Incase only one of the microbits finds a valid frequency, let the other one know.
                    radio.config(channel=0)
                    send('join', cur_freq)
                    radio.config(channel=1)
                    break
    
    display.clear()    