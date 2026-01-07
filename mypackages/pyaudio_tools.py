
import pyaudio
import wave
import os

# Good tkinter ref: https://realpython.com/playing-and-recording-sound-python/#pyaudio_1

# Following script works perfectly !

def audio_recorder():

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "C:\Cagri_Workspace\\temp\pyaudio_test.wav"
    stopfilename = "C:\Cagri_Workspace\\temp\stop_recording.txt"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording from mic...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    #for i in range(0, int(fs / chunk * seconds)):     # Store data in chunks for 3 seconds
    while not os.path.isfile(stopfilename):
        data = stream.read(chunk)
        frames.append(data)

    # Stop file was detected. Delete it to confirm !
    os.remove(stopfilename)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
