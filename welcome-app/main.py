import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import Qt

class BrambleWelcomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Configure Window Properties
        self.setWindowTitle("Welcome to BrambleOS")
        self.setFixedSize(850, 550) 
        
        # 2. Setup Central Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 3. Header Section
        title = QLabel("Choose Your Desktop Style")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #ffffff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        subtitle = QLabel("Select a layout layout. You can change this anytime later.")
        subtitle.setStyleSheet("font-size: 14px; color: #a6adc8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)
        
        main_layout.addSpacing(20)
        
        # 4. Interactive Buttons Layout (Horizontal Row)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(25)
        
        # Define our choices
        self.btn_default = QPushButton("\nBramble Default")
        self.btn_windows = QPushButton("\nWindows Layout")
        self.btn_macos = QPushButton("\nmacOS Layout")
        
        # Apply styling and actions to buttons
        for btn, layout_name in [(self.btn_default, "default"), 
                                 (self.btn_windows, "windows"), 
                                 (self.btn_macos, "macos")]:
            btn.setFixedSize(220, 180)
            button_layout.addWidget(btn)
            # Connect the click event to our backend logic function
            btn.clicked.connect(lambda checked, name=layout_name: self.handle_layout_change(name))
            
        main_layout.addLayout(button_layout)
        
        # 5. Status Footer Bar
        self.status_label = QLabel("Ready to configure workspace.")
        self.status_label.setStyleSheet("font-size: 13px; color: #fab387; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # 6. Global Theme Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #45475a;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45475a;
                border: 2px solid #89b4fa;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #89b4fa;
                color: #11111b;
            }
        """)

    # Backend Logic Execution String
    def handle_layout_change(self, layout_name):
        self.status_label.setText(f"Applying {layout_name.upper()} layout configuration...")
        print(f"[DEBUG] User clicked option: {layout_name}")
        
        # This is where Phase 2, Step 2 maps your pre-staged files!
        if layout_name == "windows":
            # For testing, we print what command will run in production
            print("Executing: xfce4-panel-profiles load layout/themes/windows/windows-panel.xml")
            self.status_label.setText("Windows layout structural rules staged successfully!")
            
        elif layout_name == "macos":
            print("Executing: xfce4-panel-profiles load layout/themes/macos/macos-panel.xml")
            self.status_label.setText("macOS layout structural rules staged successfully!")
            
        else:
            self.status_label.setText("Bramble vanilla desktop configuration restored.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrambleWelcomeApp()
    window.show()
    sys.exit(app.exec())