from webs import *
import audio
import random
neurons = {(i,t):Node(f'({i},{["Volume","Band 1", "Band 2", "Band 3", "Band 4", "Band 5", "Band 6"].index(t)})') for i in range(10) for t in ["Volume","Band 1", "Band 2", "Band 3", "Band 4", "Band 5", "Band 6"]}
offsets = [[random.randrange(-20,20) for _ in range(10)] for _ in range(7)]
web = Web(list(neurons.values()))
web.fire([neurons[1,"Volume"], neurons[5,"Band 4"]],[0.3,0.7])
print(neurons[1,"Volume"].connected_nodes)
print(neurons[5,"Band 4"].connected_nodes)

count = 0
audio_processor = audio.AudioProcessor()
try:
    while count < 6:
        volumes, band_energies = audio_processor.update()

        print("Volumes:", volumes)
        print("Band Energies:", band_energies)
        time.sleep(0.25)  # Wait for 250 ms before capturing the next set
        fire = []
        charge = []
        for i,volume in enumerate(volumes):
            if volume > 0.5:
                fire.append(neurons[(i,"Volume")])
                charge.append(volume)
        for i,band in enumerate(band_energies):
            print(band,"banddddd")
            for j,value in enumerate(band):
                if value > 0.3:
                    fire.append(neurons[(j,f"Band {i+1}")])
                    charge.append(value)
        web.fire(fire,charge)
        count += 1
    web.draw(offsets=offsets)
except KeyboardInterrupt:
    print("Stopping audio processing.")
finally:
    audio_processor.close()
