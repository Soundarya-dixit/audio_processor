import os

import librosa
import soundfile as sf

def change_pitch_volume(input_file_path, output_file_path, pitch_shift, volume_factor):
    # Load the input audio file
    audio_signal, sampling_rate = librosa.load(input_file_path, sr=None)

    # Shift the pitch of the audio signal
    audio_signal_pitch_shifted = librosa.effects.pitch_shift(audio_signal, sr=sampling_rate, n_steps=pitch_shift)
    print(f"Pitch shifted by {pitch_shift} semitones")

    # Apply the volume change factor
    audio_signal_changed_volume = audio_signal_pitch_shifted * volume_factor
    print(f"Volume changed by a factor of {volume_factor} and saved to {output_file_path}")

    # Write the pitch-shifted audio to the output file
    sf.write(output_file_path, audio_signal_changed_volume, sampling_rate)



if __name__ == "__main__":
    # Provide input and output file paths
    input_file_path = "C:\\Users\\sound\\OneDrive\\Desktop\\freqGenerator\\input\\titanic_audiotrack.wav"

    volume_factor = 0.01  # Change this to your desired volume factor (0.5 = half volume, 2.0 = double volume)
    pitch_shift = 20  # Change this to your desired pitch shift value (+ for higher pitch, - for lower pitch)

    input_filename = os.path.basename(input_file_path).split('/')[-1]
    output_file_path = input_filename.replace(".wav", "") + "_" + str(volume_factor) + "_" + str(pitch_shift) + ".wav"
    print("The output file name is " + output_file_path)
    # # Change pitch and volume
    change_pitch_volume(input_file_path, output_file_path, pitch_shift, volume_factor)
