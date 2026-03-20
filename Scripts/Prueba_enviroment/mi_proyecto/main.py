from mi_proyecto.data_loader import generar_datos
from mi_proyecto.procesamiento import calcular_eficiencia, clasificar_pozo
from mi_proyecto.graficos import graficar_eficiencia

def main():
    df = generar_datos()
    
    df = calcular_eficiencia(df)
    df = clasificar_pozo(df)
    
    print(df)
    
    graficar_eficiencia(df)

if __name__ == "__main__":
    main()