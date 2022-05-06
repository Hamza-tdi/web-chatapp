import threading
import time

from client.client import Client

c1 = Client('hamza')
c2 = Client('alaami')


def updates_messages():
    msgs = []
    run = True
    while run:
        new_msgs = c1.get_messages()
        msgs.extend(new_msgs)
        for msg in msgs:
            time.sleep(1)
            print(msg)
            if msg == '{quit}':
                run = False
                break


threading.Thread(target=updates_messages).start()

c1.send_message('slm')
time.sleep(1)
c2.send_message('salam')
time.sleep(1)
c1.send_message('feen')
time.sleep(1)
c2.send_message('fzk lfiil')
time.sleep(1)
c1.send_message('{quit}')
