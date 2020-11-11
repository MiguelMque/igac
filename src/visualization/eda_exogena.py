### NEW DEF EDA

# documentacion 
# https://python-graph-gallery.com/
# https://blog.hacemoscontactos.com/2018/08/21/analisis-de-palabras-frecuentes-usando-python/
# https://medium.com/qu4nt/reducir-el-n%C3%BAmero-de-palabras-de-un-texto-lematizaci%C3%B3n-y-radicalizaci%C3%B3n-stemming-con-python-965bfd0c69fa


# importar modulos
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk import SnowballStemmer
import spacy
from nltk.corpus import stopwords
from itertools import chain
nltk.download('stopwords')
sns.set_style("white")


def eda_exogena(data_path, image_path, engine):
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

    # # leer datos
    # df = pd.read_csv(data_path + "data_for_model_clean_places.csv")

    # leer datos 
    df = pd.read_sql("data_for_model_clean_places", engine)

    # crear variables extras
    df["valor_mill"] = df["valor"]/1000000
    df["log_valor"] = np.log(df["valor"] + 1)
    df["valor_m2"] = df["valor"]/df["area"]

    df = df[
        (df["valor"] < np.percentile(df["valor"], 98)) & 
        (df["area"] < np.percentile(df["area"], 98))
    ]
    ## figuras

    # conteo por dataset
    df_count = df.groupby("dataset").count()["tipo"]
    fig = (
        sns
        .barplot(x=[*df_count.index], y=[*df_count.values], palette="Blues")
    )
    fig.set(ylabel="conteo", title="Cantidad de inmuebles por dataset")
    fig.get_figure().savefig(image_path + "exogena_conteo_registros_dataset.png")
    plt.close()

    # distribucion del valor
    fig2 = sns.violinplot(y="valor", data=df, palette="Blues")
    fig2.set(ylabel="valor", title="Distribucion del valor")
    fig2.get_figure().savefig(image_path + "exogena_distribucion_valor.png")
    plt.close()

    # distribucion del valor por dataset
    fig3 = (
        sns.violinplot(x="dataset", y="valor", data=df, palette="Blues")
    )
    fig3.set(
        ylabel="valor", 
        title="Distribucion del valor por dataset"
    )
    fig3.get_figure().savefig(image_path + "exogena_distribucion_valor_dataset.png")
    plt.close()

    # distribucion del valor por municipio
    fig4 = (
        sns.violinplot(x="municipio", y="valor", data=df, palette="Blues")
    )
    fig4.set(
        ylabel="valor", 
        title="Distribucion del valor por municipio"
    )
    fig4.get_figure().savefig(image_path + "exogena_distribucion_valor_municipio.png")
    plt.close()

    # distribucion del valor por municipio
    df_valor = df[df["valor_m2"]<10000000]
    fig5 = (
        sns.boxplot(x="municipio", y="valor_m2", data=df_valor, palette="Blues")
    )
    fig5.set(
        ylabel="valor/m2", 
        title="Distribucion del valor por metro cuadrado por municipio"
    )
    fig5.get_figure().savefig(image_path + "exogena_distribucion_valor_m2_municipio.png")
    plt.close()

    # pairplots
    plot_df = df[[
        'municipio', 'log_valor', 'area', 'habitaciones', 'banios', 
        #'valor', 'valor_m2', 'valor_mill', #'lat', 'lon', 
    ]]
    plot_df.rename(columns={"log_valor":"valor"}, inplace=True)
    fig6 = sns.pairplot(
        plot_df[plot_df["area"]<1000000], 
        hue="municipio",
        markers=["o", "s", "D"],
        palette="Blues",
        height = 3,
        aspect = 1.5
    )
    fig6.savefig(image_path + "exogena_parejas.png")
    plt.close()

    # correlaciones
    corr_df = round(
        df[["valor", "area", "habitaciones", "banios",]].corr(),
        3
    )
    fig7 = sns.heatmap(
        corr_df,
        annot=True,
        cmap="Blues",
        center=0.3,
        linewidths=0.1,
        linecolor="white",
    )
    fig7.set(title="Matriz de correlaciones")
    fig7.get_figure().savefig(image_path + "exogena_correlaciones.png")
    plt.close()

    # pairplots de here
    new_df = df[[
        "log_valor", "municipio", "health", "restaurant", "entertainment", 
        "shop", "education", "transport"
    ]]
    new_df.rename(columns={"log_valor":"valor"}, inplace=True)
    fig8 = sns.pairplot(
        new_df,
        hue="municipio",
        markers=["o", "s", "D"],
        palette="Blues",
        height = 3,
        aspect = 1.5
    )
    fig8.savefig(image_path + "exogena_parejas_here.png")
 
    ### graficos de radar

    ## primer radar

    # crear dataset
    radar_df = (
        df[[
            "municipio", "restaurant", "entertainment", "shop", "education", 
            "park"
        ]]
        .groupby("municipio", as_index=False)
        .mean()*5
    ) 
     
    # numero de variables
    categories = list(radar_df)[1:]
    N = len(categories)
    
    # angulos
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # crear grafico
    ax = plt.subplot(111, polar=True)
    
    # primer eje al frente
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # aniadir angulos y labels
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([25,50,75,100], ["25","50","75","100"], color="grey", size=7)
    plt.ylim(0,105)
    
    # municipio 1
    values = radar_df.loc[0].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="darkblue", linewidth=1, linestyle='solid', 
        label="Fusagasugá"
    )
    ax.fill(angles, values, 'b', alpha=0.1)
    
    # municipio 2
    values = radar_df.loc[1].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="royalblue", linewidth=1, linestyle='solid', 
        label="Manizales"
    )
    ax.fill(angles, values, 'royalblue', alpha=0.1)
    
    # municipio 3
    values = radar_df.loc[2].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="deepskyblue", linewidth=1, linestyle='solid', 
        label="Villavicencio"
    )
    ax.fill(angles, values, 'deepskyblue', alpha=0.1)

    # leyenda
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(image_path + "exogena_radar_here_1.png")
    plt.close()

    ## segundo radar

    # crear dataset
    radar_df = (
        df[[
            "municipio", "health", "police", "transport", 
        ]]
        .groupby("municipio", as_index=False)
        .mean()*5
    ) 
     
    # numero de variables
    categories = list(radar_df)[1:]
    N = len(categories)
    
    # angulos
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # crear grafico
    ax = plt.subplot(111, polar=True)
    
    # primer eje al frente
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # aniadir angulos y labels
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([1.25,2.5,3.75,5], ["25","50","75","100"], color="grey", size=7)
    plt.ylim(0,5)
    
    # municipio 1
    values = radar_df.loc[0].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="darkblue", linewidth=1, linestyle='solid', 
        label="Fusagasugá"
    )
    ax.fill(angles, values, 'b', alpha=0.1)
    
    # municipio 2
    values = radar_df.loc[1].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="royalblue", linewidth=1, linestyle='solid', 
        label="Manizales"
    )
    ax.fill(angles, values, 'royalblue', alpha=0.1)
    
    # municipio 3
    values = radar_df.loc[2].drop('municipio').values.flatten().tolist()
    values += values[:1]
    ax.plot(
        angles, values, color="deepskyblue", linewidth=1, linestyle='solid', 
        label="Villavicencio"
    )
    ax.fill(angles, values, 'deepskyblue', alpha=0.1)

    # leyenda
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(image_path + "exogena_radar_here_2.png")
    plt.close()

    ### nube de palabras

    # carga de palabras en espaniol
    stop_words_sp = set(stopwords.words('spanish'))
    spanishstemmer=SnowballStemmer("spanish")
    try:
        nlp = spacy.load("es")
    except Exception as e:
        raise RuntimeError(
            """¿Ya instaló Spacy Español? 
            Utilice el comando 'python -m spacy download es_core_news_sm'""",
            e
            )
        
    def normalize(text):
        doc = nlp(text)
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        lexical_tokens = [t.lower() for t in words if len(t)>3 and t.isalpha()]
        stems = [spanishstemmer.stem(token) for token in lexical_tokens]
        return stems

    # crear lista de palabras
    new_text = list(map(normalize, df["descripcion"]))
    text = [*chain(*new_text)]
    text = " ".join(text)
    
    # graficar
    wordcloud = WordCloud(
        width=480, height=480, colormap="Blues", stopwords=stop_words_sp,
        background_color="white"
    ).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.savefig(image_path + "exogena_nube_palabras.png")
    plt.close()

    ### scatter de banios y habitaciones
    scat_df = (
        df[(df["banios"]<15)&(df["habitaciones"]<30)]#&(df["municipio"]=="Manizales")]
        .groupby(["municipio", "banios", "habitaciones"], as_index=False)["valor_mill"]
        .mean()
    )

    scat_df["valor"] = scat_df["valor_mill"]

    # graficar
    ax = sns.scatterplot(
        "banios",
        "habitaciones",
        data=scat_df,
        hue="municipio",
        size="valor",
        sizes=(2, 150),
        palette=["darkblue", "royalblue", "deepskyblue"], 
        alpha=0.8,
    )
    
    # mostrar leyenda y guardar
    h,l = ax.get_legend_handles_labels()
    plt.title("Valor por habitaciones y baños")
    plt.legend(h[:4], l[:4], bbox_to_anchor=(1.01, 1),borderaxespad=0)
    plt.grid()
    plt.savefig(image_path + "exogena_scatter_hab_ban.png")
    plt.close()
    
    return None