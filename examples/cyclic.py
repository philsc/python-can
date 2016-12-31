#!/usr/bin/env python3
"""
This example exercises the periodic sending capabilities.

Expects a vcan0 interface:

    python3 -m examples.cyclic

"""

import logging
import time

import can
logging.basicConfig(level=logging.INFO)


def simple_periodic_send(bus):
    """
    Sends a message every 20ms with no explicit timeout
    Sleeps for 2 seconds then stops the task.
    """
    print("Starting to send a message every 200ms for 2s")
    msg = can.Message(arbitration_id=0x123, data=[1, 2, 3, 4, 5, 6], extended_id=False)
    task = bus.send_periodic(msg, 0.20)
    time.sleep(2)
    task.stop()
    print("stopped cyclic send")


def limited_periodic_send(bus):
    print("Starting to send a message every 200ms for 1s")
    msg = can.Message(arbitration_id=0x12345678, data=[0, 0, 0, 0, 0, 0], extended_id=True)
    bus.send_periodic(msg, 0.20, 1)
    time.sleep(3)
    # task.stop()
    # print("stopped cyclic send")


# def test_periodic_send_with_modifying_data():
#     print("Starting to send a message every 200ms. Initial data is ones")
#     msg = can.Message(arbitration_id=0x0cf02200, data=[1, 1, 1, 1])
#     task = can.send_periodic('vcan0', msg, 0.20)
#     time.sleep(2)
#     print("Changing data of running task to begin with 99")
#     msg.data[0] = 0x99
#     task.modify_data(msg)
#     time.sleep(2)
#
#     task.stop()
#     print("stopped cyclic send")
#     print("Changing data of stopped task to single ff byte")
#     msg.data = bytearray([0xff])
#     task.modify_data(msg)
#     time.sleep(1)
#     print("starting again")
#     task.start()
#     time.sleep(1)
#     task.stop()
#     print("done")
#
#
# def test_dual_rate_periodic_send():
#     """Send a message 10 times at 1ms intervals, then continue to send every 500ms"""
#     msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5])
#     print("Creating cyclic task to send message 10 times at 1ms, then every 500ms")
#     task = can.interface.MultiRateCyclicSendTask('vcan0', msg, 10, 0.001, 0.50)
#     time.sleep(2)
#
#     print("Changing data[0] = 0x42")
#     msg.data[0] = 0x42
#     task.modify_data(msg)
#     time.sleep(2)
#
#     task.stop()
#     print("stopped cyclic send")
#
#     time.sleep(2)
#
#     task.start()
#     print("starting again")
#     time.sleep(2)
#     task.stop()
#     print("done")


if __name__ == "__main__":

    reset_msg = can.Message(arbitration_id=0x00, data=[0, 0, 0, 0, 0, 0], extended_id=False)



    for interface in {
        'socketcan_ctypes',
        #'socketcan_native'
    }:
        print("Carrying out cyclic tests with {} interface".format(interface))
        can.rc['interface'] = interface

        channel = 'vcan0'
        bus = can.interface.Bus(channel=channel)
        bus.send(reset_msg)

        simple_periodic_send(bus)

        bus.send(reset_msg)

        limited_periodic_send(bus)

        #test_periodic_send_with_modifying_data()

        #print("Carrying out multirate cyclic test for {} interface".format(interface))
        #can.rc['interface'] = interface
        #test_dual_rate_periodic_send()


    time.sleep(2)
