import time
from mplayer import Player
import Settings
import subprocess
import logging

log = logging.getLogger('root')

PANIC_ALARM = '/usr/share/scratch/Media/Sounds/Music Loops/GuitarChords2.mp3'
FX_DIRECTORY = '/root/sounds/'

class MediaPlayer:

   def __init__(self):
      self.settings = Settings.Settings()
      self.player = False
      self.effect = False

   def playerActive(self):
      return self.player!=False

   def soundAlarm(self):
      log.info("Playing alarm")
      self.playStation()
      log.debug("Alarm process opened")

      # Wait a few seconds and see if the mplayer instance is still running
      time.sleep(self.settings.getInt('radio_delay'))

      # Fetch the number of mplayer processes running
      processes = subprocess.Popen('ps aux | grep mplayer | egrep -v "grep" | wc -l',
         stdout=subprocess.PIPE,
         shell=True
      )
      num = int(processes.stdout.read())

      if num < 2 and self.player is not False:
         log.error("Could not find mplayer instance, playing panic alarm")
         self.stopPlayer()
         time.sleep(2)
         self.playMedia(PANIC_ALARM,0)

   def playStation(self,station=-1):
      if station==-1:
         station = self.settings.getInt('station')

      station = Settings.STATIONS[station]

      log.info("Playing station %s", station['name'])
      self.player = Player()
      self.player.loadlist(station['url'])
      self.player.loop = 0

   def playMedia(self,file,loop=-1):
      log.info("Playing file %s", file)
      self.player = Player()
      self.player.loadfile(file)
      self.player.loop = loop

   # Play some speech. None-blocking equivalent of playSpeech, which also pays attention to sfx_enabled setting
   def playVoice(self,text): 
      if self.settings.get('sfx_enabled')==0:
         # We've got sound effects disabled, so skip
         log.info("Sound effects disabled, not playing voice")
         return
      log.info("Playing voice: '%s'" % (text))
      play = subprocess.Popen('/usr/bin/googletts "%s"' % (text), shell=True)

   # Play some speech. Warning: Blocks until we're done speaking
   def playSpeech(self,text):
      log.info("Playing speech: '%s'" % (text))
      play = subprocess.Popen('/usr/bin/googletts "%s"' % (text), shell=True)
      play.wait()

   def stopPlayer(self):
      if self.player:
         self.player.quit()
         self.player = False
         log.info("Player process terminated")
