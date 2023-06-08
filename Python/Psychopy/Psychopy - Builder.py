#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on May 30, 2023, at 00:51
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

from pylsl import StreamInfo, StreamOutlet, local_clock
import paho.mqtt as mqtt
import re

mqtt_topic=[("Breathing",0),("Heartbeat",0),("GSR",0),("EEG",0)]


#broker_address="192.168.0.102"

broker = 'broker.emqx.io'
# broker = "mqtt.eclipseprojects.io"
port = 1883

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    val = message.payload.decode("utf-8")
    print("received ", val)
    

    if message.topic == 'Breathing':
        outletStreamResp.push_sample(val)
    elif message.topic == 'Heartbeat':
        outletStreamHeart.push_sample(val)
    elif message.topic == 'GSR':
        outletStreamGSR.push_sample(val)
    elif message.topic == 'EEG':
        # [signal strength, attention, meditation, delta, theta, low alpha, high alpha, low beta, high beta, low gamma, high gamma]
        p = re.compile(r'\d+\.\d+')  # Compile a pattern to capture float values
        EEG = [float(i) for i in p.findall(val)]  # Convert strings to float
        outletStreamEEG.push_sample(EEG)        
 


# Set up LabStreamingLayer stream.
RespStream = StreamInfo('ESP_Breath', 'RBPM', 1, 10, 'float32', 'myuid34234')
HeartStream = StreamInfo('ESP_Heart', 'BPM', 1, 10, 'float32', 'myuid34234')
GSRStream = StreamInfo('ESP_GSR', 'GSR', 1, 10, 'float32', 'myuid34234')
EEGStream = StreamInfo('ESP_EEG', 'EEG', 11, 10, 'float32', 'myuid34234')
infoMarker = StreamInfo(name='Psychopy', type='Markers', channel_count=1,
                  channel_format='int32', source_id='example_stream_001')



outletMarker = StreamOutlet(infoMarker)  # Broadcast the stream.
outletStreamResp = StreamOutlet(RespStream)
outletStreamHeart = StreamOutlet(HeartStream)
outletStreamGSR = StreamOutlet(GSRStream)
outletStreamEEG = StreamOutlet(EEGStream)

# This is not necessary but can be useful to keep track of markers and the
# events they correspond to.
markers = {
    'Start': [90],
    'Session1': [1],
    'Session2': [2],
    'Session3': [3],
    'Session4': [4],
    'End': [99]    
}


client = mqtt.Client("Smartphone")
client.connect(broker, port)

client.loop_start()


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'teste2'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\thiag\\Documents\\Git Repos\\CREEproject\\Psychopy\\Psychopy - Builder.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "Session_1" ---
text_countdown = visual.TextStim(win=win, name='text_countdown',
    text='',
    font='Open Sans',
    pos=(0, -0.2), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text_2 = visual.TextStim(win=win, name='text_2',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
text_3 = visual.TextStim(win=win, name='text_3',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0.0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Session_2" ---
text_countdown_2 = visual.TextStim(win=win, name='text_countdown_2',
    text='',
    font='Open Sans',
    pos=(0, -0.2), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text = visual.TextStim(win=win, name='text',
    text='Session 2',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
text_4 = visual.TextStim(win=win, name='text_4',
    text='Session 2',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Session_3" ---
text_countdown_3 = visual.TextStim(win=win, name='text_countdown_3',
    text='',
    font='Open Sans',
    pos=(0, -0.2), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text_5 = visual.TextStim(win=win, name='text_5',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
text_6 = visual.TextStim(win=win, name='text_6',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0.0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# --- Initialize components for Routine "Session_4" ---
text_countdown_4 = visual.TextStim(win=win, name='text_countdown_4',
    text='',
    font='Open Sans',
    pos=(0, -0.2), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text_7 = visual.TextStim(win=win, name='text_7',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
text_8 = visual.TextStim(win=win, name='text_8',
    text='Session 1',
    font='Open Sans',
    pos=(0, 0.0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "Session_1" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
Session_1Components = [text_countdown, text_2, text_3]
for thisComponent in Session_1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1
outletMarker.push_sample(markers['Session1'])

# --- Run Routine "Session_1" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 20.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_countdown* updates
    
    # if text_countdown is starting this frame...
    if text_countdown.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_countdown.frameNStart = frameN  # exact frame index
        text_countdown.tStart = t  # local t and not account for scr refresh
        text_countdown.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_countdown, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_countdown.started')
        # update status
        text_countdown.status = STARTED
        text_countdown.setAutoDraw(True)
    
    # if text_countdown is active this frame...
    if text_countdown.status == STARTED:
        # update params
        text_countdown.setText(str(20-int(t)), log=False)
    
    # if text_countdown is stopping this frame...
    if text_countdown.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_countdown.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_countdown.tStop = t  # not accounting for scr refresh
            text_countdown.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_countdown.stopped')
            # update status
            text_countdown.status = FINISHED
            text_countdown.setAutoDraw(False)
    
    # *text_2* updates
    
    # if text_2 is starting this frame...
    if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_2.frameNStart = frameN  # exact frame index
        text_2.tStart = t  # local t and not account for scr refresh
        text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_2.started')
        # update status
        text_2.status = STARTED
        text_2.setAutoDraw(True)
    
    # if text_2 is active this frame...
    if text_2.status == STARTED:
        # update params
        pass
    
    # if text_2 is stopping this frame...
    if text_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_2.tStop = t  # not accounting for scr refresh
            text_2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.stopped')
            # update status
            text_2.status = FINISHED
            text_2.setAutoDraw(False)
    
    # *text_3* updates
    
    # if text_3 is starting this frame...
    if text_3.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_3.frameNStart = frameN  # exact frame index
        text_3.tStart = t  # local t and not account for scr refresh
        text_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_3.started')
        # update status
        text_3.status = STARTED
        text_3.setAutoDraw(True)
    
    # if text_3 is active this frame...
    if text_3.status == STARTED:
        # update params
        pass
    
    # if text_3 is stopping this frame...
    if text_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_3.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_3.tStop = t  # not accounting for scr refresh
            text_3.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_3.stopped')
            # update status
            text_3.status = FINISHED
            text_3.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Session_1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Session_1" ---
for thisComponent in Session_1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-20.000000)

# --- Prepare to start Routine "Session_2" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
Session_2Components = [text_countdown_2, text, text_4]
for thisComponent in Session_2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1
outletMarker.push_sample(markers['Session2'])

# --- Run Routine "Session_2" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 20.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_countdown_2* updates
    
    # if text_countdown_2 is starting this frame...
    if text_countdown_2.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_countdown_2.frameNStart = frameN  # exact frame index
        text_countdown_2.tStart = t  # local t and not account for scr refresh
        text_countdown_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_countdown_2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_countdown_2.started')
        # update status
        text_countdown_2.status = STARTED
        text_countdown_2.setAutoDraw(True)
    
    # if text_countdown_2 is active this frame...
    if text_countdown_2.status == STARTED:
        # update params
        text_countdown_2.setText(str(20-int(t)), log=False)
    
    # if text_countdown_2 is stopping this frame...
    if text_countdown_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_countdown_2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_countdown_2.tStop = t  # not accounting for scr refresh
            text_countdown_2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_countdown_2.stopped')
            # update status
            text_countdown_2.status = FINISHED
            text_countdown_2.setAutoDraw(False)
    
    # *text* updates
    
    # if text is starting this frame...
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text.started')
        # update status
        text.status = STARTED
        text.setAutoDraw(True)
    
    # if text is active this frame...
    if text.status == STARTED:
        # update params
        pass
    
    # if text is stopping this frame...
    if text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text.tStop = t  # not accounting for scr refresh
            text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.stopped')
            # update status
            text.status = FINISHED
            text.setAutoDraw(False)
    
    # *text_4* updates
    
    # if text_4 is starting this frame...
    if text_4.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_4.frameNStart = frameN  # exact frame index
        text_4.tStart = t  # local t and not account for scr refresh
        text_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_4.started')
        # update status
        text_4.status = STARTED
        text_4.setAutoDraw(True)
    
    # if text_4 is active this frame...
    if text_4.status == STARTED:
        # update params
        pass
    
    # if text_4 is stopping this frame...
    if text_4.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_4.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_4.tStop = t  # not accounting for scr refresh
            text_4.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_4.stopped')
            # update status
            text_4.status = FINISHED
            text_4.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Session_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Session_2" ---
for thisComponent in Session_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-20.000000)

# --- Prepare to start Routine "Session_3" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
Session_3Components = [text_countdown_3, text_5, text_6]
for thisComponent in Session_3Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1
outletMarker.push_sample(markers['Session3'])

# --- Run Routine "Session_3" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 20.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_countdown_3* updates
    
    # if text_countdown_3 is starting this frame...
    if text_countdown_3.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_countdown_3.frameNStart = frameN  # exact frame index
        text_countdown_3.tStart = t  # local t and not account for scr refresh
        text_countdown_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_countdown_3, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_countdown_3.started')
        # update status
        text_countdown_3.status = STARTED
        text_countdown_3.setAutoDraw(True)
    
    # if text_countdown_3 is active this frame...
    if text_countdown_3.status == STARTED:
        # update params
        text_countdown_3.setText(str(20-int(t)), log=False)
    
    # if text_countdown_3 is stopping this frame...
    if text_countdown_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_countdown_3.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_countdown_3.tStop = t  # not accounting for scr refresh
            text_countdown_3.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_countdown_3.stopped')
            # update status
            text_countdown_3.status = FINISHED
            text_countdown_3.setAutoDraw(False)
    
    # *text_5* updates
    
    # if text_5 is starting this frame...
    if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_5.frameNStart = frameN  # exact frame index
        text_5.tStart = t  # local t and not account for scr refresh
        text_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_5.started')
        # update status
        text_5.status = STARTED
        text_5.setAutoDraw(True)
    
    # if text_5 is active this frame...
    if text_5.status == STARTED:
        # update params
        pass
    
    # if text_5 is stopping this frame...
    if text_5.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_5.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_5.tStop = t  # not accounting for scr refresh
            text_5.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_5.stopped')
            # update status
            text_5.status = FINISHED
            text_5.setAutoDraw(False)
    
    # *text_6* updates
    
    # if text_6 is starting this frame...
    if text_6.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_6.frameNStart = frameN  # exact frame index
        text_6.tStart = t  # local t and not account for scr refresh
        text_6.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_6, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_6.started')
        # update status
        text_6.status = STARTED
        text_6.setAutoDraw(True)
    
    # if text_6 is active this frame...
    if text_6.status == STARTED:
        # update params
        pass
    
    # if text_6 is stopping this frame...
    if text_6.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_6.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_6.tStop = t  # not accounting for scr refresh
            text_6.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_6.stopped')
            # update status
            text_6.status = FINISHED
            text_6.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Session_3Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Session_3" ---
for thisComponent in Session_3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-20.000000)

# --- Prepare to start Routine "Session_4" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
Session_4Components = [text_countdown_4, text_7, text_8]
for thisComponent in Session_4Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1
outletMarker.push_sample(markers['Session4'])

# --- Run Routine "Session_4" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 20.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_countdown_4* updates
    
    # if text_countdown_4 is starting this frame...
    if text_countdown_4.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_countdown_4.frameNStart = frameN  # exact frame index
        text_countdown_4.tStart = t  # local t and not account for scr refresh
        text_countdown_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_countdown_4, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_countdown_4.started')
        # update status
        text_countdown_4.status = STARTED
        text_countdown_4.setAutoDraw(True)
    
    # if text_countdown_4 is active this frame...
    if text_countdown_4.status == STARTED:
        # update params
        text_countdown_4.setText(str(20-int(t)), log=False)
    
    # if text_countdown_4 is stopping this frame...
    if text_countdown_4.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_countdown_4.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_countdown_4.tStop = t  # not accounting for scr refresh
            text_countdown_4.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_countdown_4.stopped')
            # update status
            text_countdown_4.status = FINISHED
            text_countdown_4.setAutoDraw(False)
    
    # *text_7* updates
    
    # if text_7 is starting this frame...
    if text_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_7.frameNStart = frameN  # exact frame index
        text_7.tStart = t  # local t and not account for scr refresh
        text_7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_7, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_7.started')
        # update status
        text_7.status = STARTED
        text_7.setAutoDraw(True)
    
    # if text_7 is active this frame...
    if text_7.status == STARTED:
        # update params
        pass
    
    # if text_7 is stopping this frame...
    if text_7.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_7.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_7.tStop = t  # not accounting for scr refresh
            text_7.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_7.stopped')
            # update status
            text_7.status = FINISHED
            text_7.setAutoDraw(False)
    
    # *text_8* updates
    
    # if text_8 is starting this frame...
    if text_8.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
        # keep track of start time/frame for later
        text_8.frameNStart = frameN  # exact frame index
        text_8.tStart = t  # local t and not account for scr refresh
        text_8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_8, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_8.started')
        # update status
        text_8.status = STARTED
        text_8.setAutoDraw(True)
    
    # if text_8 is active this frame...
    if text_8.status == STARTED:
        # update params
        pass
    
    # if text_8 is stopping this frame...
    if text_8.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_8.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_8.tStop = t  # not accounting for scr refresh
            text_8.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_8.stopped')
            # update status
            text_8.status = FINISHED
            text_8.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Session_4Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Session_4" ---
for thisComponent in Session_4Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-20.000000)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
