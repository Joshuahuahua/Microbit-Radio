import radio
from microbit import *

img = '09990:99000:99990:99990:09090'

print('Ready')

curr_channel = None
listen_channel = 83

radio.config(queue=83, channel=listen_channel)
radio.on()
while True:
    # If button A is pressed/held, send out a 'ping' to paired microbits
    
    if curr_channel == None and (button_a.is_pressed() or button_b.is_pressed()):
        display.show(Image.NO)
        continue

    # If the bit is paired
    if button_a.is_pressed() and curr_channel != listen_channel:
        radio.send('code')

    if button_b.was_pressed():
        radio.config(channel=listen_channel)
        




    # Listen for incoming messages
    message = radio.receive()

    if message == 'ping':
        radio.config(channel=listen_channel)
        radio.send(curr_channel)
        radio.config(channel=curr_channel)

    # If the message is 'code', display the image on screen
    if message == 'code':
        display.show(Image(img))
    display.clear()