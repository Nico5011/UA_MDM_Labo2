import pandas as pd

def generar_datos():
    df = pd.DataFrame({
        "pozo": ["P1", "P2", "P3"],
        "oil_bpd": [120, 80, 150],
        "inyeccion": [200, 180, 220]
    })
    return df