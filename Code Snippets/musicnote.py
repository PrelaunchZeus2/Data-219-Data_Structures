class note(object):
    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration
        
    def __str__(self):
        return self.pitch + " for " + self.duration + " beats"
    