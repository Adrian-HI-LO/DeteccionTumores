"""
Script de prueba para verificar las funciones de modelos simulados
"""
import numpy as np
import sys
import os

# Añadir el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_color_overlay():
    """Prueba la función create_overlay con diferentes colores"""
    print("🧪 Probando create_overlay con diferentes colores...")
    
    try:
        from model import create_overlay
        
        # Crear imagen y máscara de prueba
        img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        mask = np.random.randint(0, 2, (256, 256), dtype=np.uint8) * 255
        
        # Probar con diferentes colores
        overlay_red = create_overlay(img, mask, color=[255, 0, 0])
        overlay_green = create_overlay(img, mask, color=[0, 255, 0])
        overlay_blue = create_overlay(img, mask, color=[0, 150, 255])
        
        assert overlay_red.shape == (256, 256, 3), "Forma incorrecta para overlay rojo"
        assert overlay_green.shape == (256, 256, 3), "Forma incorrecta para overlay verde"
        assert overlay_blue.shape == (256, 256, 3), "Forma incorrecta para overlay azul"
        
        print("✅ create_overlay funciona correctamente con todos los colores")
        return True
    except Exception as e:
        print(f"❌ Error en create_overlay: {e}")
        return False

def test_alexnet_simulation():
    """Prueba la simulación de AlexNet"""
    print("\n🧪 Probando simulate_alexnet_processing...")
    
    try:
        from model import simulate_alexnet_processing
        
        img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        mask = np.random.randint(0, 2, (256, 256), dtype=np.uint8) * 255
        base_prob = 0.95
        
        prob, mask_result, overlay_result = simulate_alexnet_processing(img, mask, base_prob)
        
        # Verificar que la probabilidad se redujo correctamente
        assert 0.85 * base_prob <= prob <= 0.95 * base_prob, \
            f"Probabilidad fuera de rango: {prob} (esperado entre {0.85*base_prob} y {0.95*base_prob})"
        
        assert mask_result.shape == (256, 256, 3), "Forma incorrecta para máscara AlexNet"
        assert overlay_result.shape == (256, 256, 3), "Forma incorrecta para overlay AlexNet"
        
        print(f"✅ AlexNet: probabilidad ajustada de {base_prob:.2f} a {prob:.2f} ({prob/base_prob*100:.1f}%)")
        return True
    except Exception as e:
        print(f"❌ Error en simulate_alexnet_processing: {e}")
        return False

def test_vggnet_simulation():
    """Prueba la simulación de VGGNet"""
    print("\n🧪 Probando simulate_vggnet_processing...")
    
    try:
        from model import simulate_vggnet_processing
        
        img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        mask = np.random.randint(0, 2, (256, 256), dtype=np.uint8) * 255
        base_prob = 0.95
        
        prob, mask_result, overlay_result = simulate_vggnet_processing(img, mask, base_prob)
        
        # Verificar que la probabilidad se redujo correctamente
        assert 0.90 * base_prob <= prob <= 0.98 * base_prob, \
            f"Probabilidad fuera de rango: {prob} (esperado entre {0.90*base_prob} y {0.98*base_prob})"
        
        assert mask_result.shape == (256, 256, 3), "Forma incorrecta para máscara VGGNet"
        assert overlay_result.shape == (256, 256, 3), "Forma incorrecta para overlay VGGNet"
        
        print(f"✅ VGGNet: probabilidad ajustada de {base_prob:.2f} a {prob:.2f} ({prob/base_prob*100:.1f}%)")
        return True
    except Exception as e:
        print(f"❌ Error en simulate_vggnet_processing: {e}")
        return False

def main():
    print("=" * 60)
    print("🔬 PRUEBAS DE MODELOS SIMULADOS")
    print("=" * 60)
    
    results = []
    
    results.append(test_color_overlay())
    results.append(test_alexnet_simulation())
    results.append(test_vggnet_simulation())
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
