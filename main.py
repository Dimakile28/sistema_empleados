#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Gestión de Personal - SIGEP
Aplicación de escritorio para la gestión del personal
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ventanas.login import VentanaLogin

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Iniciar con ventana de login
        app = VentanaLogin()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()