# client/test_pyqt.py - Test PyQt5 environment

import os
import sys

def test_pyqt5():
    print("🔍 Kiểm tra PyQt5 environment...")
    
    # Get correct PyQt5 path
    import PyQt5
    pyqt5_path = os.path.dirname(PyQt5.__file__)
    qt_plugin_path = os.path.join(pyqt5_path, 'Qt5', 'plugins')
    
    print(f"🔧 PyQt5 path: {pyqt5_path}")
    print(f"🔧 Plugin path: {qt_plugin_path}")
    print(f"🔧 Plugin exists: {os.path.exists(qt_plugin_path)}")
    
    # Set QT plugin path
    os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
    
    try:
        print("📦 Importing PyQt5...")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        print("✅ PyQt5 imported successfully!")
        
        # Test QApplication
        print("🖥️ Testing QApplication...")
        app = QApplication(sys.argv)
        print("✅ QApplication created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_pyqt5()
