import sys
import os
import librosa
import soundfile as sf
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QDial, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class AudioProcessorWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, input_file_path, output_file_path, pitch_shift, volume_factor):
        super().__init__()
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.pitch_shift = pitch_shift
        self.volume_factor = volume_factor

    def run(self):
        try:
            # Load the input audio file
            audio_signal, sampling_rate = librosa.load(self.input_file_path, sr=None)

            # Shift the pitch of the audio signal
            audio_signal_pitch_shifted = librosa.effects.pitch_shift(audio_signal, sr=sampling_rate, n_steps=self.pitch_shift)

            # Apply the volume change factor
            volume_factor = self.volume_factor / 100
            audio_signal_changed_volume = audio_signal_pitch_shifted * volume_factor

            # Save the processed audio to the output file
            sf.write(self.output_file_path, audio_signal_changed_volume, sampling_rate)
        except Exception as e:
            print(f"An error occurred: {e}")

        self.finished.emit()

class AudioProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Processor")
        self.setGeometry(100, 100, 400, 300)
        self.pitch_shift = 0
        self.volume_factor = 100
        self.input_file_path = ""
        self.output_file_path = ""

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.pitch_label = QLabel("Pitch Shift:")
        layout.addWidget(self.pitch_label)

        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setMinimum(-30)
        self.pitch_slider.setMaximum(30)
        self.pitch_slider.setValue(0)
        self.pitch_slider.setTickInterval(1)
        self.pitch_slider.setTickPosition(QSlider.TicksBelow)
        self.pitch_slider.valueChanged.connect(self.on_pitch_change)
        layout.addWidget(self.pitch_slider)

        self.pitch_value_label = QLabel("0")
        layout.addWidget(self.pitch_value_label)

        self.volume_label = QLabel("Volume:")
        layout.addWidget(self.volume_label)

        self.volume_dial = QDial()
        self.volume_dial.setMinimum(0)
        self.volume_dial.setMaximum(200)
        self.volume_dial.setValue(100)
        self.volume_dial.setNotchesVisible(True)
        self.volume_dial.valueChanged.connect(self.on_volume_change)
        layout.addWidget(self.volume_dial)

        self.volume_value_label = QLabel("100%")
        layout.addWidget(self.volume_value_label)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.process_button = QPushButton("Process Audio")
        self.process_button.clicked.connect(self.process_audio)
        layout.addWidget(self.process_button)

        self.output_file_label = QLabel("")
        layout.addWidget(self.output_file_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_pitch_change(self, value):
        self.pitch_shift = value
        self.pitch_value_label.setText(str(value))

    def on_volume_change(self, value):
        self.volume_factor = value
        self.volume_value_label.setText(f"{value}%")

    def browse_file(self):
        file_dialog = QFileDialog()
        self.input_file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio files (*.wav *.mp3)")
        if self.input_file_path:
            QMessageBox.information(self, "File Selected", f"Selected file: {self.input_file_path}")

    def process_audio(self):
        if not self.input_file_path:
            QMessageBox.critical(self, "Error", "Please select an input audio file.")
            return

        # Output file name based on input file name
        input_filename, input_file_extension = os.path.splitext(os.path.basename(self.input_file_path))
        output_filename = f"{input_filename}_pitch_{self.pitch_shift}_volume_{self.volume_factor}{input_file_extension}"
        self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), output_filename)

        self.worker = AudioProcessorWorker(self.input_file_path, self.output_file_path, self.pitch_shift, self.volume_factor)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.start()

    def on_processing_finished(self):
        QMessageBox.information(self, "Success", f"Audio processing complete!\nOutput file: {self.output_file_path}")
        self.output_file_label.setText(f"Output file: {self.output_file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioProcessorGUI()
    window.show()
    sys.exit(app.exec_())
