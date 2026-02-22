import pygame
from logtofile import log_to_file

errors = ["80010X10","80020X10","80030X10","80040X10","80050X10","80060x10"]

def play_sound(path,volume,state_sound,start_time_):
    if volume == None:
        volume = 50.0
    if state_sound:
        try:
            sound = pygame.mixer.Sound("sound//click.mp3")
            sound.set_volume(volume)  # <--- вот это!
            sound.play()
            log_to_file('Sound played sucessfully', start_time_=start_time_)
        except Exception as e:
            log_to_file(f"{errors[3]} error with music: {e}", level="error",start_time_=start_time_)