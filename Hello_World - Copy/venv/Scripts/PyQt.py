import unittest
from PyQt5.QtWidgets import QApplication, QLineEdit, QComboBox
from your_module_name import BeautyForm  # Replace 'your_module_name' with the actual module name containing the BeautyForm class

class TestBeautyForm(unittest.TestCase):
    def setUp(self):
        # Create a QApplication instance for testing
        self.app = QApplication([])

        # Create an instance of the BeautyForm class
        self.form = BeautyForm()

    def tearDown(self):
        # Clean up after each test
        self.app.quit()

    def test_default_values(self):
        # Test default values of UI elements
        self.assertEqual(self.form.eye_color.text(), "")
        self.assertEqual(self.form.hair_color.text(), "")
        self.assertEqual(self.form.skin_tone.text(), "")
        self.assertEqual(self.form.season.currentText(), "Spring")

    def test_get_makeup_advice(self):
        # Simulate user input
        self.form.eye_color.setText("Brown")
        self.form.hair_color.setText("Black")
        self.form.skin_tone.setText("Fair")
        self.form.season.setCurrentText("Summer")

        # Trigger the get_makeup_advice method
        self.form.get_makeup_advice()

        # Check if the makeup_advice_label has been updated as expected
        self.assertEqual(self.form.makeup_advice_label.text(), "Your makeup advice goes here.")  # Replace with the expected advice

if __name__ == '__main__':
    unittest.main()
