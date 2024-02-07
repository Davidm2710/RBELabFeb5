# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Vanessa                                                      #
#   Created:      1/31/2024, 10:11:33 AM                                       #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
#defining motors
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1,True)

## define the colors; we'll use the default sensitivity of 3.0
## you don't have to retrain the camera to use different sensitivities; you can
##just change the value here

#camera constants
Camera_Sensitivity = 2.5
Camera_ResolutionX = 316
Camera_ResolutionY = 212
ORANGE_FRUIT = Signature (3, 6641, 7821, 7231, -2221, -1859, -2040, Camera_Sensitivity, 0)
LIME = Signature (1, -6097, -5119, -5608, -3305, -2567, -2936, Camera_Sensitivity, 0)
LEMON = Signature (2, 2685, 3133, 2909, -3517, -3161, -3339, Camera_Sensitivity, 0)
GRAPEFRUIT = Signature(4, 5137, 5535, 5336, 1175, 1683, 1429, Camera_Sensitivity, 0)
## define the camera on port 3; the library says the colors are optional 
VisionF = Vision (Ports.PORT3, 25, ORANGE_FRUIT, LIME, LEMON, GRAPEFRUIT)

VisionB = Vision (Ports.PORT4, 25, ORANGE_FRUIT, LIME, LEMON, GRAPEFRUIT)

Fruit = [ORANGE_FRUIT, LIME, LEMON]
Held_Fruit_Type = "No Fruit"
Held_Fruit_Num = 0
Max_Fruit = 4

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1
ROBOT_SEARCH_SPECIFIC = 2
ROBOT_CENTERING = 3
ROBOT_DRIVING_VISION = 4
ROBOT_GRAB_FRUIT = 5
ROBOT_SEARCH_BUCKET = 6
ROBOT_B_CENTERING = 7
ROBOT_DRIVING_BUCKET = 8
ROBOT_DUMP_FRUIT = 9
Robot_State = 0

def handleButtonPress():
    global Robot_State
    if(Robot_State == ROBOT_IDLE):
        print('IDLE -> SEARCHING')
        Robot_State = ROBOT_SEARCHING

button5 = Bumper(brain.three_wire_port.g)
button5.pressed(handleButtonPress)
Robot_State = ROBOT_IDLE

def handleObjects():
    global Held_Fruit_Type
    global Robot_State
    VisionF.take_snapshot(Fruit)
    if Held_Fruit_Type == "No Fruit":
        if Fruit == ORANGE_FRUIT:
            print("Orange detected")
            Held_Fruit_Type = ORANGE_FRUIT
            Robot_State = ROBOT_CENTERING
        elif Fruit == LIME:
            print("lime detected")
            Held_Fruit_Type = LIME
            Robot_State = ROBOT_CENTERING
        elif Fruit == LEMON:
            print("lemon detected")
            Held_Fruit_Type = LEMON
            Robot_State = ROBOT_CENTERING
        else:
            print("YOU'RE CRAZY THERE IS NO FRUIT")
    elif Held_Fruit_Type == ORANGE_FRUIT:
        if Fruit == ORANGE_FRUIT:
            print("Another Orange detected")
            Held_Fruit_Type = ORANGE_FRUIT
            Robot_State = ROBOT_CENTERING  
        else:
            Robot_State = ROBOT_SEARCH_SPECIFIC
    elif Held_Fruit_Type == LIME:
        if Fruit == LIME:
            print("Another Lime detected")
            Held_Fruit_Type = LIME
            Robot_State = ROBOT_CENTERING  
        else:
            Robot_State = ROBOT_SEARCH_SPECIFIC
    elif Held_Fruit_Type == LEMON:
        if Fruit == LEMON:
            print("Another Lemon detected")
            Held_Fruit_Type = LEMON
            Robot_State = ROBOT_CENTERING  
    else:
        Robot_State = ROBOT_SEARCH_SPECIFIC
'''
def handleBucketSearch():
    global Held_Fruit_Type
    global Robot_State
    for items in Fruit:
        objects = VisionB.take_snapshot(items)
        G_Fruit = VisionB. take_snapshot(GRAPEFRUIT)
        if objects and G_Fruit:
            if Held_Fruit_Type == ORANGE_FRUIT:
                if objects == ORANGE_FRUIT and G_Fruit:
                    print("Orange Bucket Detected")
                    Robot_State = ROBOT_B_CENTERING
            elif Held_Fruit_Type == LEMON:
                if objects == LEMON and G_Fruit:
                    print("Lemon Bucket Detected")
                    Robot_State = ROBOT_B_CENTERING
            if Held_Fruit_Type == LIME:
                if objects == LIME and G_Fruit:
                    print("Orange Bucket Detected")
                    Robot_State = ROBOT_B_CENTERING
'''             



## start in the idle Robot_State
while True: 
    
    while Robot_State == ROBOT_IDLE:
        left_motor.stop()
        right_motor.stop()
        arm_motor.spin_to_position(140 * 5,30)


                  
    while Robot_State == ROBOT_SEARCHING:
        left_motor.spin(FORWARD, 30)
        right_motor.spin(REVERSE, 30)
        for items in Fruit:
            objects = VisionF.take_snapshot(items)
            if objects and Robot_State == ROBOT_SEARCHING:
                handleObjects()      
    offset = 15
    Center_Camera = Camera_ResolutionX / 2


    while Robot_State == ROBOT_SEARCH_SPECIFIC:
        left_motor.spin(FORWARD, 30)
        right_motor.spin(REVERSE, 30)
        objects = VisionF.take_snapshot(Held_Fruit_Type)
        if objects and Robot_State == ROBOT_SEARCH_SPECIFIC:
            handleObjects() 


    while Robot_State == ROBOT_CENTERING:
        objects = VisionF.take_snapshot(Held_Fruit_Type)
        if VisionF.largest_object().centerX > Center_Camera + offset: #half of the camera resolution
            right_motor.spin(REVERSE,30)
            left_motor.spin(FORWARD, 30)
        elif VisionF.largest_object().centerX < Center_Camera - offset: #half of the camera resolution
            right_motor.spin(FORWARD,30)
            left_motor.spin(REVERSE, 30)
        else:
            print("ROBOT CENTERED")
            right_motor.stop()
            left_motor.stop()

            Robot_State = ROBOT_DRIVING_VISION
        wait(50)


    while Robot_State == ROBOT_DRIVING_VISION:
        FRUIT_TARGET_HEIGHT = 205
        FRUIT_TARGET_SIDE = Center_Camera
        objects = VisionF.take_snapshot(Held_Fruit_Type)
        if VisionF.largest_object().height < FRUIT_TARGET_HEIGHT: #change to desired number to change distance away
            errorForward = FRUIT_TARGET_HEIGHT - VisionF.largest_object().height
            effortForward = errorForward * 2
            errorSIDE = VisionF.largest_object().centerX - FRUIT_TARGET_SIDE
            effortSIDE = errorSIDE * 1
            left_motor.spin(FORWARD, effortForward + effortSIDE)
            right_motor.spin(FORWARD, effortForward + effortSIDE)
            sleep(20)
        else:
            print("ARRIVED AT FRUIT")
            left_motor.stop()
            right_motor.stop()
            Robot_State = ROBOT_GRAB_FRUIT


    while Robot_State == ROBOT_GRAB_FRUIT:
        Initial_Torque = arm_motor.torque()    
        Torque_Diff = .25 
        while Initial_Torque < Initial_Torque + Torque_Diff :
            arm_motor.spin(REVERSE,15)
        print("TOUCHED FRUIT YAY")
        left_motor.spin_for(REVERSE, 10, TURNS, 100)
        right_motor.spin_for(REVERSE, 10, TURNS, 100)
        Held_Fruit_Num += 1
        wait(2000)
        arm_motor.spin_to_position(150, DEGREES, 30)
        if Held_Fruit_Num < Max_Fruit:
            Robot_State = ROBOT_SEARCH_SPECIFIC
        else:
            Robot_State = ROBOT_SEARCH_BUCKET


    while Robot_State == ROBOT_SEARCH_BUCKET:
        
        left_motor.spin(FORWARD, 30)
        right_motor.spin(REVERSE, 30)
        for items in Fruit:
            HeldObject = VisionB.take_snapshot(Held_Fruit_Type)
            G_Fruit = VisionB. take_snapshot(GRAPEFRUIT)
            if HeldObject and G_Fruit and Robot_State == ROBOT_SEARCH_BUCKET:
                print(Held_Fruit_Type,"BUCKET FOUND")
                Robot_State = ROBOT_B_CENTERING


    while Robot_State == ROBOT_B_CENTERING:
        HeldObject = VisionB.take_snapshot(Held_Fruit_Type)
        G_Fruit = VisionB. take_snapshot(GRAPEFRUIT)
        if VisionB.largest_object.centerX > Center_Camera + offset: #half of the camera resolution
            right_motor.spin(REVERSE,30)
            left_motor.spin(FORWARD, 30)
        elif VisionB.largest_object().centerX < Center_Camera - offset: #half of the camera resolution
            right_motor.spin(FORWARD,30)
            left_motor.spin(REVERSE, 30)
        else:
            print("ROBOT CENTERED")
            right_motor.stop()
            left_motor.stop()
            Robot_State = ROBOT_DRIVING_BUCKET
        wait(500)

    while Robot_State == ROBOT_DRIVING_BUCKET:
        FRUIT_TARGET_HEIGHT = 205
        FRUIT_TARGET_SIDE = Center_Camera
        objects = VisionB.take_snapshot(Held_Fruit_Type)
        if VisionB.largest_object().height < FRUIT_TARGET_HEIGHT: #change to desired number to change distance away
            errorForward = FRUIT_TARGET_HEIGHT - VisionB.largest_object().height
            effortForward = errorForward * 2
            errorSIDE = VisionB.largest_object().centerX - FRUIT_TARGET_SIDE
            effortSIDE = errorSIDE * 1
            left_motor.spin(FORWARD, effortForward + effortSIDE)
            right_motor.spin(FORWARD, effortForward + effortSIDE)
            sleep(20)
        else:
            print("ARRIVED AT BUCKET")
            left_motor.stop()
            right_motor.stop()
            Robot_State = ROBOT_DUMP_FRUIT

    while Robot_State == ROBOT_DUMP_FRUIT:
        arm_motor.spin_to_position(200 * 5, DEGREES, 20)
        print("FRUIT DUMPED")
        Held_Fruit_Num = 0
        Held_Fruit_Type = "No Fruit"
        Robot_State = ROBOT_SEARCHING


        
