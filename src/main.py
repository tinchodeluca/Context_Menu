
import sys
import os
import winreg
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar la interfaz desde el archivo .ui
        #uic.loadUi("../ui/contextual_menu.ui", self)
        # Get the absolute path to the .ui file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, '..', 'ui', 'contextual_menu.ui')
        
        # Load the UI
        uic.loadUi(ui_path, self)      
        # Conectar botones con sus funciones
        self.btnExaminar.clicked.connect(self.seleccionar_script)
        self.btnAgregar.clicked.connect(self.agregar_menu_contextual)
        
        # Configuración inicial
        self.scriptPath = ""
        
    def seleccionar_script(self):
        fname = QFileDialog.getOpenFileName(self, 'Seleccionar Script Python', 
                                          os.path.expanduser('~'),
                                          'Python files (*.py)')
        if fname[0]:
            self.scriptPath = fname[0]
            self.txtRuta.setText(self.scriptPath)
            
    def agregar_menu_contextual(self):
        if not self.scriptPath:
            self.mostrar_mensaje("Error", "Por favor seleccione un script", QMessageBox.Warning)
            return
            
        if not self.txtMenuText.text():
            self.mostrar_mensaje("Error", "Por favor ingrese el texto para el menú", QMessageBox.Warning)
            return
            
        try:
            # Ruta al ejecutable de Python
            python_exe = sys.executable
            
            # Comando a ejecutar
            comando = f'"{python_exe}" "{self.scriptPath}" "%1"'
            
            # Crear clave para directorios
            key_path = rf"Directory\Background\shell\{self.txtMenuText.text().replace(' ', '_')}"
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
            
            # Establecer nombre que aparecerá en el menú
            winreg.SetValue(key, "", winreg.REG_SZ, self.txtMenuText.text())
            
            # Crear subclave command
            command_key = winreg.CreateKey(key, "command")
            
            # Establecer comando a ejecutar
            winreg.SetValue(command_key, "", winreg.REG_SZ, comando)
            
            winreg.CloseKey(key)
            winreg.CloseKey(command_key)
            
            self.mostrar_mensaje("Éxito", "Menú contextual agregado correctamente!", QMessageBox.Information)
            
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al agregar menú contextual: {str(e)}", QMessageBox.Critical)
    
    def mostrar_mensaje(self, titulo, mensaje, icono):
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()