from omxplayer.player import OMXPlayer


class Omx:
    def __init__(self, media_folder):
        self.player = None
        self.media_folder = media_folder
        self.expects_loading_exit = False
        self.looping = False
        
    def play(self, filename, loop=False):
        if self.player:
            self.expects_loading_exit = True
            self.player.load(filename)
        else:
            args = ['-b', '--no-osd', '-o', 'both']
            
            if loop:
                args += ['--loop']
                self.looping = True
            else:
                self.looping = False
            
            try:
                self.player = OMXPlayer(filename, args=args)
            except SystemError as e:
                print(e)
            
            self.player.stopEvent += self.on_player_stop
            self.player.exitEvent += self.on_player_exit

    def on_player_stop(self, player):
        self.player = None

    def on_player_exit(self, player, exit_status):
        if self.expects_loading_exit:
            self.expects_loading_exit = False
        else:
            self.player = None

    def stop(self):
        if not self.player:
            return
        
        self.player.stop()
        self.player = None
            
    def pause(self):
        if not self.player:
            return
        
        self.player.play_pause()
        
    def seek_fraction(self, fraction):
        if not self.player:
            return
        
        duration = self.player.duration()
        self.player.set_position(fraction * duration)
    
    def set_volume(self, volume):
        if not self.player:
            return
        
        if volume > 10:
            volume = 10
        elif volume < 0:
            volume = 0
        
        self.player.set_volume(volume)
    
    def get_source(self):
        """ Get player source and remove media folder """
        source = self.player.get_source()
        if source.startswith(self.media_folder + "/"):
            return source[len(self.media_folder) + 1:]
        else:
            return source
        
    def status(self):
        if not self.player:
            return {
                'status': 'stopped',
                'source': None,
            }
    
        return {
            'status': self.player.playback_status(),
            'source': self.get_source(),
            'position': self.player.position(),
            'duration': self.player.duration(),
            'volume': self.player.volume(),
            'looping': self.looping,
        }