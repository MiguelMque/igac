import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")


def eda_exogena(data_path, image_path):
    """
    Análisis Exploratorio de los Datos exógenos

    Crea figuras y gráficas relacionadas con una descripción general del
    Dataset exógena
    """

    if not isinstance(data_path, str):
        raise TypeError("Error, data_path debe ser de tipo string")
    if not isinstance(image_path, str):
        raise TypeError("Error, weblink debe ser de tipo string")

    data_path += "\\"
    image_path += "\\"


    ## datos

    # leer datos
    df = pd.read_csv(data_path + "data_for_model_clean.csv")

    # crear variables extras
    df["valor_mill"] = df["valor"]/1000000
    df["log_valor"] = np.log(df["valor"] + 1)
    df["valor_m2"] = df["valor"]/df["area"]

    ## figuras

    # conteo por dataset
    df_count = df.groupby("dataset").count()["tipo"]
    fig = (
        sns
        .barplot(x=[*df_count.index], y=[*df_count.values], palette="PuRd")
    )
    fig.set(ylabel="conteo", title="Cantidad de inmuebles por dataset")
    fig.get_figure().savefig(image_path + "exogena_conteo_registros_dataset.png")
    plt.close()
    del fig

    # distribucion del valor
    fig2 = sns.violinplot(y="log_valor", data=df, palette="RdPu")
    fig2.set(ylabel="log(valor)", title="Distribucion del logaritmo del valor")
    fig2.get_figure().savefig(image_path + "exogena_ditribucion_log_valor.png")
    plt.close()
    del fig2

    # distribucion del valor por dataset
    fig3 = (
        sns.violinplot(x="dataset", y="log_valor", data=df, palette="RdPu")
    )
    fig3.set(
        ylabel="log(valor)", 
        title="Distribucion del logaritmo del valor por dataset"
    )
    fig3.get_figure().savefig(image_path + "exogena_ditribucion_log_valor_dataset.png")
    plt.close()
    del fig3

    # distribucion del valor por municipio
    fig4 = (
        sns.violinplot(x="municipio", y="log_valor", data=df, palette="RdPu")
    )
    fig4.set(
        ylabel="log(valor)", 
        title="Distribucion del logaritmo del valor por municipio"
    )
    fig4.get_figure().savefig(image_path + "exogena_ditribucion_log_valor_municipio.png")
    plt.close()
    del fig4

    # distribucion del valor por municipio
    df_valor = df[df["valor_m2"]<10000000]
    fig5 = (
        sns.boxplot(x="municipio", y="valor_m2", data=df_valor, palette="RdPu")
    )
    fig5.set(
        ylabel="valor/m2", 
        title="Distribucion del valor por metro cuadrado por municipio"
    )
    fig5.get_figure().savefig(image_path + "exogena_ditribucion_valor_m2_municipio.png")
    plt.close()
    del fig5

    # correlaciones
    corr_df = round(
        df[[
            "valor_m2", "log_valor", "area", "habitaciones", "banios", # "valor"
        ]].corr(),
        3
    )
    fig6 = sns.heatmap(
            corr_df,
            annot=True,
            cmap="PuRd",
            center=0.3,
            linewidths=0.1,
            linecolor="white",
    )
    fig6.set(title="Matriz de correlaciones")
    fig6.get_figure().savefig(image_path + "exogena_correlaciones.png")
    plt.close()
    del fig6

    # pairplots
    plot_df = df[[
        'municipio', 'log_valor', 'area', 'habitaciones', 'banios', 
        #'valor', 'valor_m2', 'valor_mill', #'lat', 'lon', 
    ]]
    fig7 = sns.pairplot(
            plot_df[plot_df["area"]<1000000], 
            hue="municipio",
            markers=["o", "s", "D"],
            palette="PuRd",
            height = 3,
            aspect = 1.5
    )
    fig7.savefig(image_path + "exogena_parejas.png")
    plt.close()
    del fig7

    return None

