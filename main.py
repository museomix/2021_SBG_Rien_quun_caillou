from omxplayer.player import OMXPlayer
from pathlib import Path
import time
import RPi.GPIO as GPIO
import wiringpi
import pytweening
import os

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, 2)
wiringpi.pwmSetMode(0)

GPIO.setmode(GPIO.BCM)

# Video 1
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Clean shutdown
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Video 2
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables
vid_1 = Path("/home/pi/video1.mp4")
vid_2 = Path("/home/pi/video2.mp4")

player_fr = OMXPlayer(vid_1, args="--no-osd --no-keys -b --loop", pause = True, dbus_name="org.mpris.MediaPlayer2.omxplayer2")
player_fr.hide_video()
#player_en = OMXPlayer(vid_2, args='--no-osd --no-keys --loop', pause = True, dbus_name='org.mpris.MediaPlayer3.omxplayer1')
#player_en = OMXPlayer(vid_2, args="--no-osd --no-keys -b --loop", pause = False, dbus_name="org.mpris.MediaPlayer2.omxplayer3")
time.sleep(1)
#player_en.hide_video()

led_low = 0
led_high = 1024
pulseDelay = 0.01
pulsePause = 0.5

playerStartupDelay = 2

unlockDuration = 60

# Clear screen
os.system('dd if=/dev/zero of=/dev/fb0')

def playVid(player):
    time.sleep(2)
    player.show_video()
    player.play()
    time.sleep(player.duration())
    player.pause()
    player.hide_video()
    player.set_position(0)




try:
    while True:
        if not GPIO.input(11):
            player_fr.load(vid_1, pause = True)
            playVid(player_fr)
        if not GPIO.input(10):
            player_fr.load(vid_2, pause = True)
            playVid(player_fr)
        time.sleep(0.1)
finally:
    GPIO.cleanup()
