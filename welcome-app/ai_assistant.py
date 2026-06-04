import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget, QFrame)
from PyQt6.QtCore import Qt

class CodeInspectorDrawer(QFrame):
    """Collapsible panel that cleanly reveals the raw command structure for learning."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("InspectorDrawer")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 12, 15, 12)
        self.layout.setSpacing(8)
        
        # Section Header
        header_layout = QHBoxLayout()
        title = QLabel("💻 Safe-Shell Inspection Matrix")
        title.setStyleSheet("font-size: 12px; font-weight: 600; color: #a6e3a1; font-family: 'Inter';")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.btn_copy = QPushButton("Copy Code")
        self.btn_copy.setObjectName("DrawerCopyBtn")
        self.btn_copy.setFixedSize(80, 22)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        header_layout.addWidget(self.btn_copy)
        self.layout.addLayout(header_layout)
        
        # Display Box for the command string
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setFixedHeight(50)
        self.code_display.setObjectName("DrawerCodeDisplay")
        self.layout.addWidget(self.code_display)
        
        self.setStyleSheet("""
            QFrame#InspectorDrawer {
                background-color: #181825;
                border: 1px solid #a6e3a1;
                border-radius: 6px;
                margin-top: 5px;
            }
            QTextEdit#DrawerCodeDisplay {
                background-color: #11111b;
                border: 1px solid #313244;
                border-radius: 4px;
                color: #f5e0dc;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
            }
            QPushButton#DrawerCopyBtn {
                background-color: #313244;
                color: #cdd6f4;
                font-size: 11px;
                border: 1px solid #45475a;
                border-radius: 4px;
            }
            QPushButton#DrawerCopyBtn:hover {
                background-color: #45475a;
                color: #ffffff;
            }
        """)
        self.setVisible(False)

    def update_code(self, raw_command):
        self.code_display.setPlainText(raw_command)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_display.toPlainText())
        self.btn_copy.setText("Copied!")


class BrambleAIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BrambleOS AI Terminal Assistant")
        self.setFixedSize(950, 680)
        
        self.snapshot_history = []
        self.snapshot_counter = 0
        self.current_pending_command = ""
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # =================================================================
        # LEFT COLUMN: INTERACTIVE AI CHAT ENGINE
        # =================================================================
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)
        
        # Header
        title = QLabel("AI Terminal Safeguard")
        title.setObjectName("WidgetTitle")
        left_layout.addWidget(title)
        
        # AI Reliability Disclaimer Banner
        warning_banner = QLabel("⚠️ DISCLAIMER: This engine utilizes non-deterministic generative AI. Output models are experimental, "
                                "not guaranteed to work perfectly, and should be verified before processing.")
        warning_banner.setObjectName("WarningBanner")
        warning_banner.setWordWrap(True)
        left_layout.addWidget(warning_banner)
        
        # Chat Display Window
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setObjectName("ChatDisplay")
        self.chat_display.append("🤖 System: Automated fail-safe tracking is operational.\nDescribe the environment issue you are experiencing below:")
        left_layout.addWidget(self.chat_display)
        
        # 💻 Expandable Code Inspector Toggle Row
        inspector_control_layout = QHBoxLayout()
        self.btn_toggle_inspector = QPushButton("Show Proposed Code Structure")
        self.btn_toggle_inspector.setObjectName("InspectorToggleBtn")
        self.btn_toggle_inspector.setFixedHeight(28)
        self.btn_toggle_inspector.setEnabled(False)
        self.btn_toggle_inspector.clicked.connect(self.toggle_inspector_drawer)
        inspector_control_layout.addWidget(self.btn_toggle_inspector)
        left_layout.addLayout(inspector_control_layout)
        
        # Insert the actual Code Inspector Drawer inside the stack layout
        self.inspector_drawer = CodeInspectorDrawer()
        left_layout.addWidget(self.inspector_drawer)
        
        # Prompt User Input Line
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., 'Configure a local firewall blocking port 8080'...")
        self.input_field.setObjectName("InputField")
        self.input_field.returnPressed.connect(self.submit_request)
        
        self.btn_submit = QPushButton("Analyze")
        self.btn_submit.setFixedSize(90, 38)
        self.btn_submit.setObjectName("SubmitBtn")
        self.btn_submit.clicked.connect(self.submit_request)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.btn_submit)
        left_layout.addLayout(input_layout)
        
        # System Apply Execution Command
        self.btn_apply = QPushButton("Apply Proposed Changes")
        self.btn_apply.setFixedHeight(45)
        self.btn_apply.setObjectName("ApplyBtn")
        self.btn_apply.setEnabled(False)
        self.btn_apply.clicked.connect(self.execute_safeguard_pipeline)
        left_layout.addWidget(self.btn_apply)
        
        main_layout.addWidget(left_column, stretch=2)
        
        # =================================================================
        # RIGHT COLUMN: MULTI-STATE SNAPSHOT HISTORY TIMELINE
        # =================================================================
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        panel_title = QLabel("System Save States")
        panel_title.setObjectName("PanelTitle")
        right_layout.addWidget(panel_title)
        
        panel_desc = QLabel("Select any historical capture slice below to completely roll back the environment state storage layers.")
        panel_desc.setObjectName("PanelDesc")
        panel_desc.setWordWrap(True)
        right_layout.addWidget(panel_desc)
        
        # Core History List Widget
        self.history_list = QListWidget()
        self.history_list.setObjectName("HistoryList")
        self.history_list.itemClicked.connect(self.enable_rollback_action)
        right_layout.addWidget(self.history_list)
        
        # Rollback Interaction Button
        self.btn_rollback = QPushButton("Rollback to Selected State")
        self.btn_rollback.setFixedHeight(40)
        self.btn_rollback.setObjectName("RollbackBtn")
        self.btn_rollback.setEnabled(False)
        self.btn_rollback.clicked.connect(self.trigger_snapshot_rollback)
        right_layout.addWidget(self.btn_rollback)
        
        main_layout.addWidget(right_column, stretch=1)
        
        self.apply_premium_styles()
        self.last_proposed_fix = ""

    # --- SIMULATED LOCAL AI BACKEND LOGIC ---
    def submit_request(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return
            
        self.chat_display.append(f"\n👤 User: {user_text}")
        self.input_field.clear()
        
        self.last_proposed_fix = user_text if len(user_text) < 22 else f"{user_text[:20]}..."
        
        # Simulated Ollama local delivery strings split out cleanly
        simulated_ai_response = {
            "description": "Restricting ingress traffic vectors by shifting default firewall input rules.",
            "command": "sudo ufw deny 8080/tcp"
        }
        
        self.current_pending_command = simulated_ai_response["command"]
        
        # Feed the generated code snippet right down into our inspector storage cache
        self.inspector_drawer.update_code(self.current_pending_command)
        self.inspector_drawer.btn_copy.setText("Copy Code") # Reset button state
        
        self.chat_display.append(f"\n🤖 AI Analysis: {simulated_ai_response['description']}")
        self.chat_display.append("✨ An operational shell sequence has been staged. Expand the code explorer panel to audit the script.")
        
        self.btn_toggle_inspector.setEnabled(True)
        self.btn_apply.setEnabled(True)

    def toggle_inspector_drawer(self):
        is_visible = self.inspector_drawer.isVisible()
        self.inspector_drawer.setVisible(not is_visible)
        self.btn_toggle_inspector.setText("Hide Proposed Code Structure" if not is_visible else "Show Proposed Code Structure")

    def execute_safeguard_pipeline(self):
        self.snapshot_counter += 1
        snapshot_comment = f"Pre-{self.last_proposed_fix if self.last_proposed_fix else 'AI Fix'}"
        snapshot_label = f"Snapshot #{self.snapshot_counter} ({snapshot_comment})"
        
        self.snapshot_history.append(snapshot_label)
        
        self.chat_display.append(f"\n⚡ Core Snapshot captured: sudo timeshift --create --comments '{snapshot_comment}'...")
        self.chat_display.append(f"✔️ Save state stored securely as index point.")
        
        self.chat_display.append(f"⚡ Running command sequence target: {self.current_pending_command}...")
        self.chat_display.append("✔️ System configuration successfully adjusted.")
        
        self.history_list.addItem(snapshot_label)
        
        # Clean down transient inputs
        self.btn_apply.setEnabled(False)
        self.inspector_drawer.setVisible(False)
        self.btn_toggle_inspector.setEnabled(False)
        self.btn_toggle_inspector.setText("Show Proposed Code Structure")

    def enable_rollback_action(self):
        self.btn_rollback.setEnabled(True)

    def trigger_snapshot_rollback(self):
        selected_item = self.history_list.currentItem()
        if not selected_item:
            return
            
        target_state = selected_item.text()
        self.chat_display.append(f"\n🚨 RESTORE PIPELINE COMMAND ISSUED 🚨")
        self.chat_display.append(f"Executing storage state extraction: sudo timeshift --restore -> Target: '{target_state}'...")
        self.chat_display.append("✔️ Filesystem snapshot rolled back seamlessly. System environment safely restored.")
        
        row = self.history_list.row(selected_item)
        self.history_list.takeItem(row)
        self.btn_rollback.setEnabled(False)

    def apply_premium_styles(self):
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #11111b; 
            }
            QLabel { 
                font-family: 'Inter', sans-serif; 
            }
            QLabel#WidgetTitle { 
                font-size: 22px; 
                font-weight: 600; 
                color: #ffffff; 
                letter-spacing: -0.5px; 
            }
            QLabel#PanelTitle { 
                font-size: 15px; 
                font-weight: 600; 
                color: #89b4fa; 
            }
            QLabel#PanelDesc { 
                font-size: 12px; 
                color: #7f849c; 
                line-height: 1.3; 
            }
            
            QLabel#WarningBanner {
                font-size: 12px;
                font-weight: 500;
                color: #f38ba8;
                background-color: #251e2e;
                border: 1px solid #f38ba8;
                border-radius: 6px;
                padding: 10px;
                line-height: 1.4;
            }
            
            QTextEdit#ChatDisplay {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 8px;
                color: #cdd6f4;
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
                padding: 10px;
            }
            
            QListWidget#HistoryList {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
                padding: 5px;
            }
            QListWidget#HistoryList::item {
                padding: 10px;
                border-bottom: 1px solid #1e1e2e;
                border-radius: 4px;
                color: #a6adc8;
            }
            QListWidget#HistoryList::item:hover {
                background-color: #1e1e2e;
                color: #ffffff;
            }
            QListWidget#HistoryList::item:selected {
                background-color: #313244;
                border-left: 3px solid #f38ba8;
                color: #f38ba8;
                font-weight: 600;
            }
            
            QLineEdit#InputField {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 6px;
                color: #ffffff;
                font-size: 13px;
                padding-left: 15px;
                height: 36px;
            }
            QLineEdit#InputField:focus { 
                border: 1px solid #89b4fa; 
            }
            
            QPushButton { 
                font-family: 'Inter', sans-serif; 
                font-size: 13px; 
                font-weight: 500; 
                border-radius: 6px; 
            }
            
            QPushButton#InspectorToggleBtn {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                color: #a6adc8;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton#InspectorToggleBtn:hover {
                background-color: #313244;
                color: #ffffff;
            }
            QPushButton#InspectorToggleBtn:disabled {
                background-color: #11111b;
                color: #45475a;
                border: 1px solid #1e1e2e;
            }
            
            QPushButton#SubmitBtn { 
                background-color: #1e1e2e; 
                color: #cdd6f4; 
                border: 1px solid #313244; 
            }
            QPushButton#SubmitBtn:hover { 
                background-color: #313244; 
                color: #ffffff; 
            }
            
            QPushButton#ApplyBtn { 
                background-color: #89b4fa; 
                color: #11111b; 
                font-weight: 600; 
                border: none; 
            }
            QPushButton#ApplyBtn:hover { 
                background-color: #b4befe; 
            }
            QPushButton#ApplyBtn:disabled { 
                background-color: #1e1e2e; 
                color: #45475a; 
                border: 1px solid #11111b; 
            }
            
            QPushButton#RollbackBtn { 
                background-color: #f38ba8; 
                color: #11111b; 
                font-weight: 600; 
                border: none; 
            }
            QPushButton#RollbackBtn:hover { 
                background-color: #eba0ac; 
            }
            QPushButton#RollbackBtn:disabled { 
                background-color: #1e1e2e; 
                color: #45475a; 
                border: 1px solid #11111b; 
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrambleAIAssistant()
    window.show()
    sys.exit(app.exec())