import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton


import pandas as pd

class BeautyForm(QWidget):
    def init(self):
        super().init()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Makeup Advice App')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.eye_color_label = QLabel('Eye Color:')
        self.eye_color = QLineEdit()
        layout.addWidget(self.eye_color_label)
        layout.addWidget(self.eye_color)

        self.hair_color_label = QLabel('Hair Color:')
        self.hair_color = QLineEdit()
        layout.addWidget(self.hair_color_label)
        layout.addWidget(self.hair_color) 
self.skin_tone_label = QLabel('Skin Tone:')
        self.skin_tone = QLineEdit()
        layout.addWidget(self.skin_tone_label)
        layout.addWidget(self.skin_tone)

        self.season_label = QLabel('Season:')
        self.season = QComboBox()
        self.season.addItems(['Spring', 'Summer', 'Fall', 'Winter'])
        layout.addWidget(self.season_label)
        layout.addWidget(self.season)

        self.get_makeup_advice_button = QPushButton('Get Makeup Advice')
        layout.addWidget(self.get_makeup_advice_button)

        self.makeup_advice_label = QLabel('')
        layout.addWidget(self.makeup_advice_label)

        self.setLayout(layout)

        self.get_makeup_advice_button.clicked.connect(self.get_makeup_advice)

    def get_makeup_advice(self):
        # Process user input and provide makeup advice
        eye_color = self.eye_color.text()
        hair_color = self.hair_color.text()
        skin_tone = self.skin_tone.text()
        season = self.season.currentText()

        # Filter the makeup data based on user input
        filtered_data = makeup_data[
            (makeup_data['EyeColor'] == eye_color) &
            (makeup_data['HairColor'] == hair_color) &
            (makeup_data['SkinTone'] == skin_tone) &
            (makeup_data['Season'] == season)
        ]

        # Get makeup advice based on the filtered data
        if not filtered_data.empty:
            makeup_advice_result = filtered_data.iloc[0]['MakeupAdvice']
        else:
            makeup_advice_result = "No makeup advice available for this combination."

        self.makeup_advice_label.setText(makeup_advice_result)

if name == 'main':
    # Load makeup advice data from a CSV file
    makeup_data = pd.read_csv('makeup_data.csv')

    app = QApplication(sys.argv)
    beauty_form = BeautyForm()
    beautyform.show()
    sys.exit(app.exec())