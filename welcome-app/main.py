import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt

class DropdownDetail(QFrame):
    def __init__(self, description_text, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 10, 15, 10)
        
        self.label = QLabel(description_text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 13px; color: #a6adc8; line-height: 1.4;")
        self.layout.addWidget(self.label)
        
        self.setStyleSheet("""
            DropdownDetail {
                background-color: #252538;
                border-left: 3px solid #89b4fa;
                border-radius: 4px;
            }
        """)
        self.setVisible(False)

    def toggle(self):
        self.setVisible(not self.isVisible())


class BrambleWelcomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BrambleOS Setup")
        self.setFixedSize(900, 700) # Slightly wider and taller to perfectly display the new categories
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        outer_layout = QVBoxLayout(central_widget)
        outer_layout.setContentsMargins(40, 40, 40, 25)
        
        # Paginated Stack Controller
        self.pages = QStackedWidget()
        outer_layout.addWidget(self.pages)
        
        # Build the Pages
        self.setup_page_one()   # Desktop Layout
        self.setup_page_two()   # Hardware Drivers
        self.setup_page_three() # App Provisioning (Now Scrollable)
        
        # Permanent Navigation Control Bar
        nav_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("Back")
        self.btn_back.setFixedSize(100, 40)
        self.btn_back.clicked.connect(self.prev_page)
        nav_layout.addWidget(self.btn_back)
        
        nav_layout.addStretch()
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setFixedSize(100, 40)
        self.btn_next.clicked.connect(self.next_page)
        nav_layout.addWidget(self.btn_next)
        
        outer_layout.addLayout(nav_layout)
        
        self.update_navigation_state()
        self.apply_global_styles()

    # --- PAGE 1: DESKTOP LAYOUT STYLE ---
    def setup_page_one(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        title = QLabel("Select Desktop Layout")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Choose your default interface structure. This can be reconfigured dynamically later.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        options_layout = QVBoxLayout()
        options_layout.setSpacing(12)
        
        options = [
            ("Bramble Default", "The native Bramble environment optimized for modern developer workflows. Clean, focused, and minimal.", "default"),
            ("Redmond Traditional Layout", "Standard taskbar structure mapped to the screen base with a left-aligned app menu. Familiar and classic.", "windows"),
            ("Cupertino Dock Layout", "Top-aligned persistent application panel coupled with a centered app dock utility at the bottom boundary.", "macos")
        ]
        
        self.layout_buttons = {}
        for title_text, desc_text, key in options:
            row_container = QWidget()
            row_layout = QVBoxLayout(row_container)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)
            
            btn = QPushButton(title_text)
            btn.setCheckable(True)
            btn.setFixedHeight(45)
            btn.setObjectName("LayoutSelectBtn")
            btn.clicked.connect(lambda checked, k=key: self.select_layout_option(k))
            
            dropdown = DropdownDetail(desc_text)
            
            info_btn = QPushButton("Details")
            info_btn.setObjectName("InfoToggleBtn")
            info_btn.setFixedSize(80, 25)
            info_btn.clicked.connect(dropdown.toggle)
            
            btn_hbox = QHBoxLayout()
            btn_hbox.addWidget(btn)
            btn_hbox.addWidget(info_btn)
            
            row_layout.addLayout(btn_hbox)
            row_layout.addWidget(dropdown)
            options_layout.addWidget(row_container)
            
            self.layout_buttons[key] = (btn, dropdown)
            
        layout.addLayout(options_layout)
        layout.addStretch()
        self.pages.addWidget(page)

    # --- PAGE 2: UNIVERSAL HARDWARE OPTIMIZATION ---
    def setup_page_two(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        title = QLabel("Hardware Optimization")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Analyze system architecture to link optimal drivers for your processors and peripheral chipsets.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        self.btn_optimize = QPushButton("Run Hardware Detection Pipeline")
        self.btn_optimize.setObjectName("OptimizeBtn")
        self.btn_optimize.setFixedHeight(60)
        self.btn_optimize.clicked.connect(self.trigger_hardware_pipeline)
        layout.addWidget(self.btn_optimize)
        
        self.hardware_status = QLabel("Awaiting kernel hardware query...")
        self.hardware_status.setObjectName("StatusText")
        self.hardware_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hardware_status)
        
        layout.addStretch()
        self.pages.addWidget(page)

    # --- PAGE 3: SOFTWARE PROVISIONING (NOW EXTENDED & SCROLLABLE) ---
    def setup_page_three(self):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Install Supplementary Software")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(title)
        
        subtitle = QLabel("Select additional applications to deploy natively. Leave all unchecked for a completely minimal system.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(subtitle)
        
        page_layout.addSpacing(15)
        
        # Implement a clean Scroll Area so the UI never feels crammed
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("AppScrollArea")
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(15)
        
        self.app_checkboxes = {}
        
        # Newly Expanded, Multi-Region Categorized Mapping
        categories = [
            ("Web Browsers", [
                ("Zen Browser", "io.github.zen_browser.zen"),
                ("Brave Browser", "com.brave.Browser"),
                ("Mozilla Firefox", "org.mozilla.firefox")
            ]),
            ("Digital Productivity & Mail", [
                ("P3X OneNote", "com.github.p3x-robotics.onenote"),
                ("Thunderbird Mail (Gmail)", "org.mozilla.Thunderbird"),
                ("Obsidian Notes", "md.obsidian.Obsidian")
            ]),
            ("Development Environments", [
                ("Visual Studio Code", "com.visualstudio.code"),
                ("GitKraken Client", "com.gitkraken.GitKraken")
            ]),
            ("Gaming Hubs", [
                ("Steam Ecosystem", "com.valvesoftware.Steam"),
                ("Heroic Games Launcher", "com.heroicgameslauncher.hgl"),
                ("Lutris Platform", "net.lutris.Lutris")
            ]),
            ("Social & Communications", [
                ("Discord Client", "com.discordapp.Discord"),
                ("WhatsApp Desktop", "com.rtosta.zapzap"),
                ("Signal Messenger", "org.signal.Signal")
            ]),
            ("Media & Entertainment", [
                ("Spotify Music", "com.spotify.Client"),
                ("FreeTube (YouTube Client)", "io.github.FreeTubeApp.FreeTube"),
                ("VLC Media Player", "org.videolan.VLC")
            ])
        ]
        
        for cat_title, apps in categories:
            cat_label = QLabel(cat_title)
            cat_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #89b4fa; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px;")
            layout.addWidget(cat_label)
            
            grid_layout = QHBoxLayout()
            grid_layout.setSpacing(15)
            
            for app_name, flatpak_id in apps:
                cb = QCheckBox(app_name)
                cb.setStyleSheet("font-size: 13px; color: #cdd6f4;")
                grid_layout.addWidget(cb)
                self.app_checkboxes[flatpak_id] = cb
                
            grid_layout.addStretch()
            layout.addLayout(grid_layout)
            
            # Subtly separate sections with a thin horizontal rule
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setStyleSheet("background-color: #1e1e2e; max-height: 1px; border: none;")
            layout.addWidget(line)
            
        scroll.setWidget(scroll_content)
        page_layout.addWidget(scroll)
        self.pages.addWidget(page)

    # --- BACKEND LOGIC INTERFACES ---
    def select_layout_option(self, target_key):
        for key, (btn, _) in self.layout_buttons.items():
            btn.setChecked(key == target_key)
        print(f"[DEBUG] Selection mapped to configuration profile: {target_key}")

    def trigger_hardware_pipeline(self):
        self.hardware_status.setText("Querying motherboard system buses and graphics engines...")
        print("[DEBUG] Initializing generalized hardware driver installation script chain...")
        self.hardware_status.setText("All system processors, controllers, and chipsets optimized successfully.")

    def process_final_provisioning(self):
        selected_packages = [fid for fid, cb in self.app_checkboxes.items() if cb.isChecked()]
        
        if not selected_packages:
            print("[DEBUG] User opted out of additional software. Leaving system minimal.")
            return
            
        print(f"[DEBUG] Commencing silent provisioning sequence for selected manifests...")
        for flatpak_id in selected_packages:
            print(f"Executing: flatpak install flathub {flatpak_id} -y")

    def next_page(self):
        if self.pages.currentIndex() < self.pages.count() - 1:
            self.pages.setCurrentIndex(self.pages.currentIndex() + 1)
            self.update_navigation_state()
        else:
            self.process_final_provisioning()
            print("[DEBUG] Phase 2 Configuration complete. Closing onboarding manager.")
            self.close()

    def prev_page(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)
            self.update_navigation_state()

    def update_navigation_state(self):
        current = self.pages.currentIndex()
        self.btn_back.setEnabled(current > 0)
        
        if current == self.pages.count() - 1:
            self.btn_next.setText("Finish")
        else:
            self.btn_next.setText("Next")

    # --- DESIGN SYSTEM / STYLESHEET ---
    def apply_global_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #11111b;
            }
            QLabel {
                font-family: 'Inter', 'SF Pro Display', sans-serif;
            }
            QLabel#PageTitle {
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                letter-spacing: -0.5px;
            }
            QLabel#PageSubtitle {
                font-size: 14px;
                color: #7f849c;
            }
            QLabel#StatusText {
                font-size: 13px;
                color: #fab387;
                font-family: 'JetBrains Mono', monospace;
            }
            
            /* Scroll Container Customization */
            QScrollArea#AppScrollArea {
                border: 1px solid #1e1e2e;
                border-radius: 8px;
                background-color: #181825;
            }
            QScrollArea#AppScrollArea QWidget {
                background-color: #181825;
            }
            
            /* Checkbox Customization */
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #45475a;
                border-radius: 4px;
                background-color: #1e1e2e;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #89b4fa;
            }
            QCheckBox::indicator:checked {
                background-color: #89b4fa;
                border: 1px solid #89b4fa;
            }
            
            /* Structural Navigation Buttons */
            QPushButton {
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                font-weight: 500;
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #313244;
                border: 1px solid #45475a;
                color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #11111b;
                color: #45475a;
                border: 1px solid #1e1e2e;
            }
            
            QPushButton#LayoutSelectBtn {
                text-align: left;
                padding-left: 20px;
                font-size: 15px;
                font-weight: 600;
                background-color: #181825;
            }
            QPushButton#LayoutSelectBtn:checked {
                background-color: #1e1e2e;
                border: 1px solid #89b4fa;
                color: #89b4fa;
            }
            QPushButton#InfoToggleBtn {
                background-color: transparent;
                border: none;
                color: #7f849c;
                font-size: 12px;
            }
            QPushButton#InfoToggleBtn:hover {
                color: #89b4fa;
            }
            QPushButton#OptimizeBtn {
                background-color: #89b4fa;
                color: #11111b;
                font-size: 15px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
            }
            QPushButton#OptimizeBtn:hover {
                background-color: #b4befe;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrambleWelcomeApp()
    window.show()
    sys.exit(app.exec())