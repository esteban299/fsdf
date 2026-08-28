#!/usr/bin/env python3

import random
import speech_recognition as sr
import sys
import time

BANCO_FRASES = {
    "A1": [
        "Hello, how are you?",
        "Good morning friend.",
        "I like apples and bananas.",
        "Where is the bathroom?",
        "My name is John.",
        "I have a red car."
    ],
    "A2": [
        "What are you doing today?",
        "I need to buy some groceries.",
        "She works at the hospital.",
        "The weather is very nice outside.",
        "We are going to the park.",
        "Can you help me please?"
    ],
    "B1": [
        "If it rains tomorrow, we will stay at home.",
        "Could you please explain that again?",
        "I have been learning English for six months.",
        "Travelling helps you understand different cultures.",
        "He decided to study computer science.",
        "I am planning a trip for next summer."
    ],
    "B2": [
        "Despite the heavy traffic, we arrived on time.",
        "I completely agree with your point of view.",
        "Technology has drastically changed the way we communicate.",
        "It is essential to maintain a healthy work life balance.",
        "The company expanded its operations globally.",
        "We should consider all available options."
    ],
    "C1": [
        "The subtle nuances of the language are fascinating.",
        "He delivered a remarkable speech that captivated the audience.",
        "It is imperative that we implement sustainable practices immediately.",
        "Her meticulous approach to research yielded unprecedented results.",
        "The ongoing debate reflects deep societal divisions.",
        "Academic rigor requires thorough critical thinking."
    ],
    "C2": [
        "The ubiquitous nature of smartphones has profoundly altered social dynamics.",
        "Philosophical discourse often encapsulates complex existential queries.",
        "Notwithstanding the intricate circumstances, the project proceeded flawlessly.",
        "Eloquence is the ability to express oneself fluently and persuasively.",
        "The delicate ecological equilibrium is threatened by climate change.",
        "Theoretical models must undergo rigorous empirical validation."
    ]
}

NIVELES = ["A1", "A2", "B1", "B2", "C1", "C2"]

def limpiar_pantalla():
    print("\n" * 50)

def mostrar_arte_ascii():
    limpiar_pantalla()
    print(r"""
 ───────────────────────────────
───────────────████─███────────
──────────────██▒▒▒█▒▒▒█───────
─────────────██▒────────█──────
─────────██████──██─██──█──────
────────██████───██─██──█──────
────────██▒▒▒█──────────███────
────────██▒▒▒▒▒▒───▒──██████───
───────██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███─
──────██▒▒▒▒─────▒▒▒▒▒▒▒▒▒▒▒▒█─
──────██▒▒▒───────▒▒▒▒▒▒▒█▒█▒██
───────██▒▒───────▒▒▒▒▒▒▒▒▒▒▒▒█
────────██▒▒─────█▒▒▒▒▒▒▒▒▒▒▒▒█
────────███▒▒───██▒▒▒▒▒▒▒▒▒▒▒▒█
─────────███▒▒───█▒▒▒▒▒▒▒▒▒▒▒█─
────────██▀█▒▒────█▒▒▒▒▒▒▒▒██──
──────██▀██▒▒▒────█████████────
────██▀███▒▒▒▒────█▒▒██────────
█████████▒▒▒▒▒█───██──██───────
█▒▒▒▒▒▒█▒▒▒▒▒█────████▒▒█──────
█▒▒▒▒▒▒█▒▒▒▒▒▒█───███▒▒▒█──────
█▒▒▒▒▒▒█▒▒▒▒▒█────█▒▒▒▒▒█──────
██▒▒▒▒▒█▒▒▒▒▒▒█───█▒▒▒███──────
─██▒▒▒▒███████───██████────────
──██▒▒▒▒▒██─────██─────────────
───██▒▒▒██─────██──────────────
────█████─────███──────────────
────█████▄───█████▄────────────
──▄█▓▓▓▓▓█▄─█▓▓▓▓▓█▄───────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──▀████████▀▀███████▀──────────
 
                                                           
              [ TERMINAL SPEECH EDITION ]
    """)

def limpiar_texto(texto):
    for simbolo in [".", ",", "?", "!", ";", ":", '"', "'"]:
        texto = texto.replace(simbolo, "")
    return texto.lower().split()

def calcular_palabras_correctas(objetivo, escuchado):
    palabras_obj = limpiar_texto(objetivo)
    palabras_esc = limpiar_texto(escuchado)
    
    puntos = 0
    for p_obj, p_esc in zip(palabras_obj, palabras_esc):
        if p_obj == p_esc:
            puntos += 1
            
    es_perfecto = (palabras_obj == palabras_esc)
    return puntos, len(palabras_obj), es_perfecto

def escuchar_micropatron(reconocedor, microfono):
    try:
        with microfono as source:
            print("🔴 ¡Habla ahora! (Tienes tiempo suficiente)...")
            audio = reconocedor.listen(source, phrase_time_limit=15)
            print("⏳ Procesando audio...")
            texto = reconocedor.recognize_google(audio, language="en-US")
            return texto.strip()
    except sr.WaitTimeoutError:
        print("⚠️ Tiempo agotado. No se detectó voz.")
        return None
    except sr.UnknownValueError:
        print("❓ No se logró entender el audio.")
        return None
    except OSError:
        print("❌ Error: No se detectó ningún micrófono conectado.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Error al procesar audio: {e}")
        return None

def test_de_nivel(reconocedor, microfono):
    print("\n--- 📝 PRUEBA DE NIVELACIÓN (7 PREGUNTAS) ---")
    print("Responde las 7 preguntas. Evaluaremos tu porcentaje de precisión para determinar tu nivel.\n")
    
    secuencia_niveles = ["A1", "A2", "B1", "B1", "B2", "C1", "C2"]
    
    palabras_acertadas_totales = 0
    palabras_posibles_totales = 0
    
    for i, niv in enumerate(secuencia_niveles, 1):
        frase = random.choice(BANCO_FRASES[niv])
        print(f"\n[Pregunta {i}/7 - Dificultad {niv}] - Pronuncia:")
        print(f"👉 \"{frase}\"")
        input("Presiona ENTER y habla de inmediato...")
        
        escuchado = escuchar_micropatron(reconocedor, microfono)
        
        if escuchado:
            print(f"   Escuchado: \"{escuchado}\"")
            pts, total, perfecto = calcular_palabras_correctas(frase, escuchado)
            palabras_acertadas_totales += pts
            palabras_posibles_totales += total
            print(f"   📊 Palabras correctas: {pts}/{total}")
        else:
            _, total, _ = calcular_palabras_correctas(frase, "")
            palabras_posibles_totales += total
            print("   ❌ No se obtuvo respuesta válida. (0 puntos)")
            
    porcentaje = (palabras_acertadas_totales / palabras_posibles_totales) if palabras_posibles_totales > 0 else 0
    
    print("\n================ FINALIZANDO PRUEBA ================")
    print(f"Puntuación total: {palabras_acertadas_totales}/{palabras_posibles_totales} palabras correctas ({porcentaje * 100:.1f}%)")
    
    if porcentaje < 0.25:
        nivel_asignado = "A1"
    elif porcentaje < 0.45:
        nivel_asignado = "A2"
    elif porcentaje < 0.65:
        nivel_asignado = "B1"
    elif porcentaje < 0.80:
        nivel_asignado = "B2"
    elif porcentaje < 0.92:
        nivel_asignado = "C1"
    else:
        nivel_asignado = "C2"
        
    return nivel_asignado

def seleccionar_o_evaluar_nivel(reconocedor, microfono):
    print("Niveles: A1, A2, B1, B2, C1, C2")
    print("Escribe tu nivel directamente o escribe 'test' para evaluarte.")
    
    while True:
        eleccion = input("\nTu opción (A1-C2 / test): ").strip().upper()
        if eleccion in NIVELES:
            return eleccion
        elif eleccion == "TEST":
            nivel_asignado = test_de_nivel(reconocedor, microfono)
            print(f"\n🎉 Nivel asignado definitivamente: {nivel_asignado}")
            time.sleep(3)
            return nivel_asignado
        else:
            print("⚠️ Opción inválida. Intenta de nuevo.")

def jugar_quiz(nivel_actual, reconocedor, microfono):
    puntos_totales = 0
    vidas = 3
    
    print(f"\n🚀 Iniciando Quiz [{nivel_actual}] - Ganas 1 punto por cada palabra pronunciada correctamente")
    
    frases_disponibles = list(BANCO_FRASES[nivel_actual])
    
    while vidas > 0:
        if not frases_disponibles:
            frases_disponibles = list(BANCO_FRASES[nivel_actual])

        frase_objetivo = random.choice(frases_disponibles)
        frases_disponibles.remove(frase_objetivo)
        
        print("\n" + "-" * 40)
        print(f"❤️ Vidas: {vidas} | 🏆 Puntos Totales: {puntos_totales}")
        print(f"Pronuncia: \"{frase_objetivo}\"")
        input("Presiona ENTER y habla de inmediato...")
        
        escuchado = escuchar_micropatron(reconocedor, microfono)
        
        if escuchado:
            print(f"Escuchado: \"{escuchado}\"")
            pts, total_palabras, perfecto = calcular_palabras_correctas(frase_objetivo, escuchado)
            
            puntos_totales += pts
            
            if perfecto:
                print(f"✨ ¡Perfecto! Dominaste la frase (+{pts} pts)")
            elif pts > 0:
                print(f"👍 Buen intento. Pronunciaste {pts} de {total_palabras} palabras bien (+{pts} pts)")
                vidas -= 1
            else:
                vidas -= 1
                print("❌ Ninguna palabra coincidió.")
        else:
            vidas -= 1
            print("❌ Sin respuesta válida.")

    print("\n" + "=" * 40)
    print("💀 GAME OVER - Te has quedado sin vidas.")
    return puntos_totales

def main():
    reconocedor = sr.Recognizer()
    
    # Configuración para permitir pausas más largas al hablar
    reconocedor.pause_threshold = 3.5
    reconocedor.non_speaking_duration = 1.0
    
    try:
        microfono = sr.Microphone()
        with microfono as source:
            mostrar_arte_ascii()
            print("🎙️ Calibrando micrófono...")
            reconocedor.adjust_for_ambient_noise(source, duration=1)
            reconocedor.dynamic_energy_threshold = True
    except OSError:
        print("❌ Error: No se detectó ningún micrófono conectado.")
        sys.exit(1)
        
    record_historico = 0
    nivel_jugador = seleccionar_o_evaluar_nivel(reconocedor, microfono)
    
    while True:
        mostrar_arte_ascii()
        print(f"Nivel actual: {nivel_jugador} | Récord: {record_historico} pts")
        
        puntos_partida = jugar_quiz(nivel_jugador, reconocedor, microfono)
        
        if puntos_partida > record_historico:
            record_historico = puntos_partida
            print(f"\n🎉 ¡NUEVO RÉCORD!: {record_historico} pts")
        else:
            print(f"\nPuntos obtenidos: {puntos_partida}")
            print(f"Récord actual: {record_historico} pts")
            
        print("\n[1] Volver a jugar")
        print("[2] Cambiar de nivel / Repetir prueba")
        print("[3] Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            continue
        elif opcion == "2":
            nivel_jugador = seleccionar_o_evaluar_nivel(reconocedor, microfono)
        elif opcion == "3":
            print("\n¡Gracias por jugar! 👋")
            break
        else:
            print("Opción inválida. Saliendo...")
            break

if __name__ == "__main__":
    main()