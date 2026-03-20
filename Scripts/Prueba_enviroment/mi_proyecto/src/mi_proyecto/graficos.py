import matplotlib.pyplot as plt

def graficar_eficiencia(df):
    plt.bar(df["pozo"], df["eficiencia"])
    plt.title("Eficiencia por pozo")
    plt.xlabel("Pozo")
    plt.ylabel("Eficiencia")
    plt.show()