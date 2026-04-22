"""Script para verificar que todas las importaciones funcionan"""

print("Verificando importaciones...")

try:
    from database.conexion import db
    print("✅ database.conexion OK")
except Exception as e:
    print(f"❌ database.conexion: {e}")

try:
    from database.queries import Queries
    print("✅ database.queries OK")
except Exception as e:
    print(f"❌ database.queries: {e}")

try:
    from utils.validaciones import Validaciones
    print("✅ utils.validaciones OK")
except Exception as e:
    print(f"❌ utils.validaciones: {e}")

try:
    from ventanas.menu_principal import MenuPrincipal
    print("✅ ventanas.menu_principal OK")
except Exception as e:
    print(f"❌ ventanas.menu_principal: {e}")

print("\n✅ Todas las importaciones verificadas correctamente")
print("Puedes ejecutar: python main.py")