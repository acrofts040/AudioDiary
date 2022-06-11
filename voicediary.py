import pyaudio
import wave
import speech_recognition as sr
from os import path
import datetime


#TODO:
# loop with commands (i.e "done" or time limits for repeated entry)
# write with good formatting


#HELPER FUNCTIONS

#audio recorder: stores mic data into wav file 
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# transcribe output.wav file created by recording
def transcribe():                                                      
    AUDIO_FILE = "output.wav"                                       
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the audio file                  
            
            tscript = str(r.recognize_google(audio))
            return tscript



#add transcription to diary in readable manner
def write_to_diary(transcription):
    transcription = transcription[0].upper() + transcription[1:]

    #open read stream to check for repeat entry
    f = open("diary.txt", "r")
    date = str(datetime.date.today())
    sameday = not(date in f.read())
    f.close()

    #write to file
    f = open("diary.txt", "a")

    #add new date if necessary
    if sameday:
        f.write("\n\n")
        f.write(date)
        f.write(": \n")  
    f.write(transcription+". \n")
    f.close()




def main():
    record_audio()
    tscript = transcribe()
    write_to_diary(tscript)

if __name__ == '__main__':
    main()
