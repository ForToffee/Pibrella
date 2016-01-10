# Pibrella Steady Hand Game
# By Carl Monk (@ForToffee)

import pibrella
import time, signal
from threading import Timer
 
# setup global variables
state = 'end'		# to track what is happening in the game
startTime = 0		# when the game started
touch = 0			# how many touches of the wire 
idleTimer = None	# timer to show idle animation after win

# idle animation
def idle():
	pibrella.light.red.pulse(1,1,0,0)
	pibrella.light.amber.pulse(0.8,0.8,0,0)
	pibrella.light.green.pulse(0.7,0.7,0,0)
	print "Tap the start point to begin"

# event when the start point is touched
def start(pin):
	global state, startTime, touch, idleTimer
	if state != 'run':	# if game is not running
		if idleTimer != None:	#  cancel timer if one is 
			idleTimer.cancel() 
		startTime = time.time()	#set start time
		touch = 0	# reset touches 
		state = 'run'	# put game into run state 
		pibrella.light.off()
		print "Your time starts now!"

# event when state of the wire is changed (touch / no touch)
def wire(pin):
	global state, touch
	if pin.read():	# wire touched
		if state == 'run':	# if game running
			print 'Touch!'
			touch += 1	# increment touch count and light LEDs
			state = 'touch'
			if touch >= 1:
				pibrella.light.green.on()
			if touch >= 2:
				pibrella.light.amber.on()
			if touch >= 3:
				pibrella.light.red.on()
				state = 'fail'	# too many touches
				
			if state == 'fail':
				print "Game Over"
				pibrella.buzzer.fail()
				idle()
			else:
				pibrella.buzzer.note(0)	# short buzz
				time.sleep(0.5)
				pibrella.buzzer.off()

	else:	# wire no longer touched, reset game state
		if state == 'touch':
			state = 'run'

# event when end point is touched
def home(pin):
	global state, startTime, idleTimer
	if state == 'run':
		endTime = time.time()
		state = 'end'
		print 'You made it in', endTime - startTime, 'seconds!'
		print 'You had', touch, 'touch(es) of the wire'
		pibrella.buzzer.success()

		# the timer allows the player to see how many lives were lost after a win 
		# for 30 secs without blocking the events so if they wish to play again they
		# just go back to the start.  Otherwise the idle animation will start when 
		# the timer elapses
		idleTimer = Timer(30, idle)
		idleTimer.start()


# main program
# set events for input changes
pibrella.input.a.pressed(start)	
pibrella.input.b.changed(wire)	
pibrella.input.c.pressed(home)

#show idle animation
idle()

# wait for the magic to happen
while True:
	try:
		signal.pause()
	except KeyboardInterrupt:
		if idleTimer != None:	#  cancel timer if one is running
			idleTimer.cancel() 
		raise
	

