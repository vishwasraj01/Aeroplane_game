import pygame
import numpy as np
import os
import wave
import struct

# Initialize Pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def generate_crash_sound():
    # Generate a crash sound (noise with decreasing amplitude)
    duration = 0.5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    envelope = np.exp(-5 * t)  # Exponential decay
    sound = noise * envelope
    sound = np.clip(sound, -1, 1)
    sound = (sound * 32767).astype(np.int16)
    return sound

def generate_powerup_sound():
    # Generate a powerup sound (rising tone)
    duration = 0.3
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = 440 * np.exp(2 * t)  # Rising frequency
    sound = 0.5 * np.sin(2 * np.pi * frequency * t)
    sound = np.clip(sound, -1, 1)
    sound = (sound * 32767).astype(np.int16)
    return sound

def generate_background_music():
    # Generate simple background music (repeating pattern)
    duration = 2.0
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a simple melody
    notes = [440, 523.25, 587.33, 659.25]  # A, C, D, E
    sound = np.zeros_like(t)
    for i, note in enumerate(notes):
        start = i * duration / len(notes)
        end = (i + 1) * duration / len(notes)
        mask = (t >= start) & (t < end)
        sound[mask] = 0.3 * np.sin(2 * np.pi * note * t[mask])
    
    sound = np.clip(sound, -1, 1)
    sound = (sound * 32767).astype(np.int16)
    return sound

def save_wav(filename, sound_data):
    with wave.open(filename, 'w') as wav_file:
        # Set the parameters
        nchannels = 1
        sampwidth = 2
        framerate = 44100
        nframes = len(sound_data)
        comptype = 'NONE'
        compname = 'not compressed'
        
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        
        # Write the audio data
        for sample in sound_data:
            wav_file.writeframes(struct.pack('h', sample))

def main():
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Generate and save sounds
    crash_sound = generate_crash_sound()
    powerup_sound = generate_powerup_sound()
    background_music = generate_background_music()
    
    save_wav(os.path.join("assets", "crash.wav"), crash_sound)
    save_wav(os.path.join("assets", "powerup.wav"), powerup_sound)
    save_wav(os.path.join("assets", "background.wav"), background_music)

if __name__ == "__main__":
    main() 