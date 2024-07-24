
from flask import Flask, Response
import numpy as np
import time
#pip install flask numpy

app = Flask(__name__)

# Frequências das notas musicais (em Hz)
NOTES = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23
}

# Configurações de áudio
SAMPLE_RATE = 44100  # Taxa de amostragem (em Hz)
DURATION = 1  # Duração de cada nota (em segundos)

def generate_wave(frequency, duration, sample_rate):
    """Gera uma onda senoidal para uma determinada frequência e duração."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return (wave * 32767).astype(np.int16).tobytes()

def audio_generator():
    """Gera uma sequência infinita de tons de 'Dó' a 'Fá'."""
    while True:
        for note in ['C', 'D', 'E', 'F']:
            wave = generate_wave(NOTES[note], DURATION, SAMPLE_RATE)
            yield wave

@app.route('/stream')
def stream():
    """Rota de streaming de áudio."""
    return Response(audio_generator(), mimetype='audio/wav')
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
