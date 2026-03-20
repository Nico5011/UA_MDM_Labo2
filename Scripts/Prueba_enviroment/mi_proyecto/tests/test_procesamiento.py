import pandas as pd
from mi_proyecto.procesamiento import calcular_eficiencia

def test_calcular_eficiencia():
    df = pd.DataFrame({
        "oil_bpd": [100],
        "inyeccion": [200]
    })

    df = calcular_eficiencia(df)

    assert df["eficiencia"].iloc[0] == 0.5  