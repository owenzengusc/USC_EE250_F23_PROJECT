import time
import grovepi
import wave
import struct

# Connect the Grove Buzzer to digital port D8
# SIG,NC,VCC,GND
buzzer = 3
audio_data=[]
grovepi.pinMode(buzzer,"OUTPUT")

w = wave.open("recording.wav", "r")
length = w.getnframes()
for i in range(0, length):
    waveData = w.readframes(1)
    data = struct.unpack("<h", waveData)
    audio_data.append(int(data[0]))
print(audio_data)
print("size is:")
print(len(audio_data))

# Function to map amplitude to PWM duty cycle (0-255)
def amplitude_to_duty_cycle(amp):
    min_duty_cycle = 0
    max_duty_cycle = 255
    # Map the amplitude to a duty cycle range
    return int(((amp - min(audio_data)) / (max(audio_data) - min(audio_data))) * (max_duty_cycle - min_duty_cycle) + min_duty_cycle)
cnt =0
# Play each data point on the buzzer
for amp in audio_data:
    try:
        duty_cycle = amplitude_to_duty_cycle(amp)
        # Apply PWM signal
        print(duty_cycle,cnt)
        grovepi.analogWrite(buzzer, duty_cycle)
        #time.sleep(0.01)
        cnt+=1
    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        break

grovepi.digitalWrite(buzzer, 0)


while True:
    try:
        # # Buzz for 1 second
        # grovepi.digitalWrite(buzzer,1)
        # print ('start')
        # time.sleep(1)

        # # Stop buzzing for 1 second and repeat
        # grovepi.digitalWrite(buzzer,0)
        # print ('stop')
        # time.sleep(1)

        # for i in range (1,255):
        #     print(i)
        #     grovepi.analogWrite(buzzer,i)
        #     time.sleep(0.05)
        #     grovepi.digitalWrite(buzzer,0)
        #     time.sleep(0.05)
        pass

    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        break
    except IOError:
        print ("Error")
