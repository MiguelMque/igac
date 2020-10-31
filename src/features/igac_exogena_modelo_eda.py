# -*- coding: utf-8 -*-

# import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from zipfile import ZIP_LZMA
from zipfile import ZipFile



# read zip files
zip1 = "/content/drive/My Drive/Informacion_Exogena.zip"
zip2 = "/content/drive/My Drive/data_for_model_v2.zip"

with ZipFile(zip1, mode="r") as zipObj:
    zipObj.extractall()

with ZipFile(zip2, mode="r") as zipObj:
    zipObj.extractall()

# read fincaraiz
fincaraiz = pd.read_csv("fincaraiz-consolidado-venta_vivienda-20201022.csv")

# read data_for_model
homogeneos = pd.read_csv("data_for_model_homogenea_v2.csv")

# read properati
properati = pd.read_csv("co_properties.csv")

# data clean
data_clean = pd.read_csv("/content/drive/My Drive/data_clean.csv")

# # en caso de tener que volver a generar, cargar la informacion y volver a correr
# new data clean
data_clean2 = data_clean.drop(columns="Unnamed: 0")
data_clean2["dataset"] = "igac"

# new fincaraiz
fincaraiz2 = fincaraiz[[
    "Location1", "Location2", "Neighborhood", "Title", "Description",
    "Price", "Area", "Rooms", "Baths", "Latitude", "Longitude"
]]

fincaraiz2.columns = [
    "fr_departamento", "fr_municipio", "fr_barrio", "fr_titulo",
    "fr_descripcion", "fr_valor", "fr_area", "fr_habitaciones", 
    "fr_banios", "fr_lat", "fr_lon"
]

fincaraiz2["fr_type"] = "Habitacional"
fincaraiz2["fr_dataset"] = "fincaraiz"

#geometry_fr2 = gpd.points_from_xy(fincaraiz2.fr_lon, fincaraiz2.fr_lat)
#fincaraiz2 = gpd.GeoDataFrame(fincaraiz2, geometry=geometry_fr2)

# new properati
depts = ["risaralda", "caldas", "cundinamarca", "boyaca", "boyacá", "vichada",]
properati["property_type"] = (
    properati.property_type
    .replace(["Casa", "Lote", "Apartamento", "Finca", "Parqueadero", "PH"], "Habitacional")
    .replace(["Oficina", "Local comercial"], "Comercial")
    .replace("Depósito", "Industrial")
)
properati_temp = properati[properati["l2"].str.lower().isin(depts)]


properati2 = properati_temp[[
    "l2", "l3", "l5", "title", "description", "price", "surface_total",
    "bedrooms", "bathrooms", "lat", "lon", "property_type"
]]

properati2.columns = [
    "pr_departamento", "pr_municipio", "pr_barrio", "pr_titulo", 
    "pr_descripcion", "pr_valor", "pr_area", "pr_habitaciones", 
    "pr_banios", "pr_lat", "pr_lon", "pr_type"
]

properati2["pr_dataset"] = "properati"

#geometry_p2 = gpd.points_from_xy(properati2.pr_lon, properati2.pr_lat)
#properati2 = gpd.GeoDataFrame(properati2, geometry=geometry_p2)

# new concat and save
data_for_model = pd.concat([data_clean2, fincaraiz2, properati2])
#data_for_model.to_csv("data_for_model_v2.csv", index=False)

# homogeneous columns

# clean data
data_clean3 = data_clean[[
    "Departamento", "MUNICIPIO_y", "AVALUO_MILLONES", "AREA_TOTAL", 
    "HABITACIONES_1", "BANOS_1", "lat", "lon", "descripcion_corta"
]]

data_clean3.columns = [
    "ig_departamento", "ig_municipio", "ig_valor", "ig_area",
    "ig_habitaciones", "ig_banios", "ig_lat", "ig_lon", "ig_type"
]

data_clean3["ig_dataset"] = "igac"
data_clean3["ig_valor"] = data_clean3["ig_valor"]*1000000
data_clean3["ig_barrio"] = np.nan
data_clean3["ig_titulo"] = np.nan
data_clean3["ig_descripcion"] = np.nan

# change columns names
data_clean3.columns = [col[3:] for col in data_clean3.columns]
fincaraiz2.columns = [col[3:] for col in fincaraiz2.columns]
properati2.columns = [col[3:] for col in properati2.columns]

# new concat
data_for_model2 = pd.concat([data_clean3, fincaraiz2, properati2])
# data_for_model2.to_csv("data_for_model_homogenea_v2.csv", index=False)

# # crear zip
# with ZipFile("data_for_model_v2.zip", "w", compression=ZIP_LZMA) as zipObj:

#     zipObj.write("data_for_model_v2.csv")
#     zipObj.write("data_for_model_homogenea_v2.csv")

# files.download("data_for_model_v2.zip")

# some basic information
homogeneos.info()

# more basic information
homogeneos.describe()

# show plot per dataset
sns.barplot(
    x=homogeneos["dataset"].value_counts().index,
    y=[*homogeneos["dataset"].value_counts()], 
    palette="PuRd"
)
plt.title("Total of properties per dataset")

# it can be seen that some data may be located out of colombia 
# (around lat [-2, 12], lon [-80, -65])
# also, some properties does not have values, lon, lat, area

hom2 = homogeneos[
    (~homogeneos["valor"].isna()) & 
    (homogeneos["lat"] <= 12) & (homogeneos["lat"] >= -2) &
    (homogeneos["lon"] <= -65) & (homogeneos["lon"] >= -80) &
    (~homogeneos["area"].isna())
]

hom2.describe()

# create new columns
hom2["valor_mill"] = hom2["valor"]/1000000
hom2["log_valor"] = np.log(hom2["valor"] + 1)
hom2["valor_m2"] = hom2["valor"]/hom2["area"]

# show some basic information of valor
sns.violinplot(y="log_valor", data=hom2, palette="RdPu")
plt.ylabel("Log of value")

# show some basic information of valor
sns.violinplot(y="valor_m2", data=hom2[(hom2["valor_m2"] < 100000)], palette="RdPu")
plt.ylabel("Value per square meter")

# information per departamento
plt.figure(figsize=(15, 5))
sns.violinplot(x="departamento", y="log_valor", data=hom2, palette="RdPu")
plt.ylabel("Log of value per Departament")

# show some basic information of valor
plt.figure(figsize=(15, 5))
sns.violinplot(
    x="departamento", 
    y="valor_m2", 
    data=hom2[(hom2["valor_m2"] < 100000) & (hom2["valor_m2"] > 0)],
    palette="RdPu"
)

plt.ylabel("Valor por metro cuadrado del predio")

# information per municipio
plt.figure(figsize=(15, 5))
sns.violinplot(x="dataset", y="log_valor", data=hom2, palette="RdPu")
plt.ylabel("Logaritmo del valor del predio")

# information per municipio
plt.figure(figsize=(15, 5))
sns.violinplot(
    x="dataset", 
    y="valor_m2", 
    data=hom2[(hom2["valor_m2"] < 100000)], 
    palette="RdPu"
)
plt.ylabel("Valor del metro cuadrado del predio")

plot_df = hom2[["log_valor", "area", "habitaciones", "banios", "dataset"]]
sns.pairplot(
    plot_df, 
    hue="dataset",
    markers=["o", "s", "D"],
    palette="PuRd",
    height = 3,
    aspect = 1.5
)

# check outlayers from bathrooms and bedrooms and exclude from EDA
#[*hom2[(hom2["habitaciones"]>250) | (hom2["banios"]>250)]["descripcion"]]
outliers1 = hom2[(hom2["habitaciones"]>250) | (hom2["banios"]>250) | (hom2["area"]>40000000)]
hom3 = hom2[(hom2["habitaciones"]<=250) & (hom2["banios"]<=250) & (hom2["area"]<1000000)]

# data distributions and pairplots
plot_df = hom3[["log_valor", "area", "habitaciones", "banios", "dataset"]]
sns.pairplot(
    plot_df, 
    hue="dataset",
    markers=["o", "s", "D"],
    palette="PuRd",
    height = 3,
    aspect = 1.5
)

# dataframe
corr_df = round(
    hom3[[
        "valor", "log_valor", "area", "habitaciones", "banios", 
        "dataset", "valor_m2"
    ]].corr(),
     3
)

# mask = np.array([
#     [0,1,0,0,0,1],
#     [1,0,0,0,0,1],
#     [0,0,0,0,0,1],
#     [0,0,0,0,0,0],
#     [0,0,0,0,0,0],
#     [1,1,1,0,0,0]
# ])

# plot
sns.heatmap(
    corr_df,
    annot=True,
    cmap="PuRd",
    center=0.3,
    linewidths=0.1,
    linecolor="white",
    #mask=mask
)

plt.title("Correlation matrix")

# plot for each dataset
fig, axs = plt.subplots(1, 3, figsize=(18,4))
i = 0

for dataset in hom3["dataset"].unique():
    
    corr_df = round(
        hom3[hom3["dataset"]==dataset][
            ["valor", "log_valor", "area", "habitaciones", "banios", "dataset", "valor_m2"]
        ].corr(),
        3
    )
    axs[i].title.set_text("Matriz de correlaciones de {}".format(dataset))
    # plot
    sns.heatmap(
        corr_df,
        annot=True,
        cmap="PuRd",
        center=0.3,
        linewidths=0.1,
        linecolor="white",
        ax=axs[i],
        #mask=mask
    )
    i += 1

homogeneos.isna().any()

hom3.isna().any()

hom3
geometry_p2 = gpd.points_from_xy(hom3.lon, hom3.lat)
hom3 = gpd.GeoDataFrame(hom3, geometry=geometry_p2)

fjoin = gpd.sjoin(data, hom3, op="contains")

print(fjoin.shape)
print(hom3.shape)

fjoin.head()

data = data.to_crs("EPSG:4326")

fjoin[["NOMBRE_DPT", "NOMBRE_MPI"]+[*hom3.columns]]

pd.crosstab(fjoin["NOMBRE_DPT"], fjoin["departamento"])
#pd.crosstab(fjoin["NOMBRE_MPI"], fjoin["municipio"])

hom3["municipio"].fillna("NA", inplace=True)

hom3.drop(columns=["barrio", "titulo", "descripcion"], inplace=True)

hom3.head()

depts = pd.get_dummies(hom3["departamento"])
muns = pd.get_dummies(hom3["municipio"].str.lower().str.replace("á","a").str.replace("é","e").str.replace("í","i").str.replace("ó","o").str.replace("ú","u").str.replace(" d.c","").str.capitalize())
types = pd.get_dummies(hom3["type"].str.lower().str.replace("á","a").str.replace("é","e").str.replace("í","i").str.replace("ó","o").str.replace("ú","u").str.replace(" d.c","").str.capitalize())

hom4 = pd.concat([depts, muns, types, hom3.drop(columns=["departamento", "municipio", "type", "log_valor", "valor_mill"])], axis=1)

hom4.shape

with ZipFile("data_for_model_v3.zip", "w", compression=ZIP_LZMA) as zipObj:

    zipObj.write("datos_pulpitos_modelo.csv")
#     zipObj.write("data_for_model_homogenea_v2.csv")

hom4.to_csv("datos_pulpitos_modelo.csv", index=False)

hom3["type"].unique()

data_clean

dest = pd.read_csv("destino_economico.csv", sep=";")

data_clean = data_clean.merge(dest.drop(columns="descripcion_larga"), left_on="DESTINO_ECONOMICO", right_on="destino_economico")

data_clean

dest.descripcion_corta.unique()

properati.property_type.unique()

properati["property_type"] = properati.property_type.replace(["Casa", "Lote", "Apartamento", "Finca", "Parqueadero", "PH"], "Habitacional").replace(["Oficina", "Local comercial"], "Comercial").replace("Depósito", "Industrial")

homogeneos = data_for_model2.copy()

