import pygame
from threading import Thread

# Initialize Pygame
pygame.init()

def play_sound_and_exit():
    try:
        # Load sound
        sound = pygame.mixer.Sound("phonk.mp3")  # Replace with your sound file path

        # Play the sound
        sound.play()

        # Wait for sound to finish before exiting the thread
        while pygame.mixer.get_busy():
            pass

    except:
        return  # Exit gracefully if an exception occurs

# Start a thread to play the sound
thread = Thread(target=play_sound_and_exit)
thread.start()

# Wait for the thread to finish before continuing (optional)
thread.join()
