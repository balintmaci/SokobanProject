import driver.color_sensor as clr
import driver.motor as mtr
import driver.gyro as gyro

import control as ctrl
from command_handler import cmdlist
import command_handler as cmd
from command_handler import Command as Cmd
from driver.shutdown import *

from enum import Enum

class States(Enum):
    TURNING = 1
    MOVING = 2
    DEFAULT = 3
    STOPPING = 4

act_st = States.DEFAULT

def setup_next_command():
    global act_st
    if(len(cmd.cmdlist) > 0):
        command = cmd.cmdlist.popleft()
        print("Next command: " + repr(command))
        if(command == Cmd.GO_STRAIGHT):
            act_st = States.MOVING
        elif(command == Cmd.TURN_RIGHT):
            ctrl.turn_setup(90)
            act_st = States.TURNING
        elif(command == Cmd.TURN_LEFT):
            ctrl.turn_setup(-90)
            act_st = States.TURNING
        elif(command == Cmd.TURN_AROUND):
            ctrl.turn_setup(180)
            act_st = States.TURNING
        else:
            print("Error, unrecognized command")
            shutdown()
    else:
        print("No command, stopping...")
        shutdown()
        

def run_states():
    global act_st
    if(act_st == States.MOVING):
        if(ctrl.is_intersection() == False):
            ctrl.line_control()
        else:
            setup_next_command()

    elif(act_st == States.TURNING):
        if(ctrl.is_turn_finished() == False):
            ctrl.turn_control()
        else:
            setup_next_command()
    
    elif(act_st == States.STOPPING):
        mtr.stop()
        setup_next_command()
    else:
        setup_next_command()

