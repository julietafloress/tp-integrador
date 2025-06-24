import csv
import json

# Estructura principal
datos = []

# 1. Cargar datos desde un CSV
def cargar_csv(ruta_archivo):
    with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Salta encabezado
        for fila in lector:
            datos.append([
                fila[0],  # Nombre
                fila[1],  # Materia
                float(fila[2]),  # Nota1
                float(fila[3]),  # Nota2
                float(fila[4]),  # Nota3
                float(fila[5])   # NotaFinal
            ])
    print("✔️ Datos cargados desde CSV.\n")

# 2. Cargar datos manualmente
def cargar_manual():
    print("📥 Ingresá un nuevo registro:")
    nombre = input("Nombre y Apellido: ")
    materia = input("Materia: ")

    try:
        nota1 = float(input("Nota 1: "))
        nota2 = float(input("Nota 2: "))
        nota3 = float(input("Nota 3: "))
        nota_final = float(input("Nota final: "))
    except ValueError:
        print("❌ Error: ingresá solo números en las notas.\n")
        return

    nuevo = [nombre, materia, nota1, nota2, nota3, nota_final]
    datos.append(nuevo)
    print("✔️ Registro agregado.\n")

    # Guardar en CSV
    try:
        with open("notas.csv", "a", newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(nuevo)
        print("📄 Registro también guardado en 'notas.csv'\n")
    except Exception as e:
        print(f"⚠️ No se pudo guardar en CSV: {e}")


# 3. Informes
def informes():
    print("\n📊 INFORMES ESTADÍSTICOS")
    if not datos:
        print("No hay datos cargados.")
        return

    total_final = sum([d[5] for d in datos])
    promedio_final = total_final / len(datos)

    aprobados = len([d for d in datos if d[5] >= 6])
    mejores = [d for d in datos if d[5] == max(datos, key=lambda x: x[5])[5]]

    materia_prom = {}
    for d in datos:
        materia = d[1]
        if materia not in materia_prom:
            materia_prom[materia] = []
        materia_prom[materia].append(d[5])

    print(f"📌 Promedio general de nota final: {promedio_final:.2f}")
    print(f"📌 Cantidad de aprobados: {aprobados}")
    print("📌 Mejor(es) nota(s) final(es):")
    for m in mejores:
        print(f"    {m[0]} en {m[1]} con {m[5]}")

    print("📌 Promedio por materia:")
    for materia, notas in materia_prom.items():
        prom = sum(notas) / len(notas)
        print(f"    {materia}: {prom:.2f}")
    print()

    # Guardar resultados en JSON
    resultados = {
        "promedio_general": round(promedio_final, 2),
        "aprobados": aprobados,
        "mejor_nota": {
            "alumnos": [m[0] for m in mejores],
            "nota": mejores[0][5]
        },
        "promedio_por_materia": {materia: round(sum(notas)/len(notas), 2) for materia, notas in materia_prom.items()}
    }

    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("📝 Resultados guardados en 'resultados.json'\n")

def mostrar_resultados_guardados():
    try:
        with open("resultados.json", "r", encoding="utf-8") as f:
            resultados = json.load(f)
        
        print("\n📂 RESULTADOS GUARDADOS (desde JSON)")
        print(f"📌 Promedio general: {resultados['promedio_general']}")
        print(f"📌 Aprobados: {resultados['aprobados']}")
        print("📌 Mejor nota:")
        for alumno in resultados["mejor_nota"]["alumnos"]:
            print(f"   {alumno} con {resultados['mejor_nota']['nota']}")
        print("📌 Promedio por materia:")
        for materia, promedio in resultados["promedio_por_materia"].items():
            print(f"   {materia}: {promedio}")
        print()

    except FileNotFoundError:
        print("❌ No hay resultados guardados. Primero generá los informes.")
    except Exception as e:
        print(f"⚠️ Error al leer el archivo JSON: {e}")

# 4. Métodos de ordenamiento

# Burbuja por NotaFinal
def ordenar_por_nota_final():
    n = len(datos)
    for i in range(n):
        for j in range(0, n-i-1):
            if datos[j][5] > datos[j+1][5]:
                datos[j], datos[j+1] = datos[j+1], datos[j]
    print("🔃 Lista ordenada por Nota Final (burbuja).\n")

# Selección por Nombre
def ordenar_por_nombre():
    n = len(datos)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if datos[j][0].lower() < datos[min_idx][0].lower():
                min_idx = j
        datos[i], datos[min_idx] = datos[min_idx], datos[i]
    print("🔃 Lista ordenada por Nombre (selección).\n")

# 5. Mostrar los datos
def mostrar_datos():
    print("\n📋 LISTADO ACTUAL")
    print(f"{'Nombre y Apellido':<20} {'Materia':<15} {'N1':<6} {'N2':<6} {'N3':<6} {'Final':<6}")
    print("-" * 70)
    for d in datos:
        print(f"{d[0]:<20} {d[1]:<15} {d[2]:<6} {d[3]:<6} {d[4]:<6} {d[5]:<6}")
    print()

# Menú
def menu():
    while True:
        print("📌 MENÚ DE OPCIONES")
        print("1. Cargar datos desde CSV")
        print("2. Cargar registro manualmente")
        print("3. Ver informes")
        print("4. Ordenar por nota final")
        print("5. Ordenar por nombre")
        print("6. Mostrar todos los datos")
        print("7. Mostrar resultados guardados")
        print("0. Salir")

        opcion = input("Elegí una opción: ")
        if opcion == '1':
            ruta = input("Ruta del archivo CSV: ")
            cargar_csv(ruta)
        elif opcion == '2':
            cargar_manual()
        elif opcion == '3':
            informes()
        elif opcion == '4':
            ordenar_por_nota_final()
            mostrar_datos()
        elif opcion == '5':
            ordenar_por_nombre()
            mostrar_datos()
        elif opcion == '6':
            mostrar_datos()
        elif opcion == '7':
            mostrar_resultados_guardados()
        elif opcion == '0':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.\n")


menu()
