def calcular_eficiencia(df):
    df["eficiencia"] = df["oil_bpd"] / df["inyeccion"]
    return df

def clasificar_pozo(df):
    df["categoria"] = df["eficiencia"].apply(
        lambda x: "ALTA" if x > 0.6 else "BAJA"
    )
    return df