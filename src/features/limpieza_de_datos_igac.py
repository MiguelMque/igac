import pandas as pd
import geopandas as gpd
import numpy as np



def limpieza_datos(data_path,avaluo,general_asp,detail_asp):
    ## read shapefiles
    
    # create iterable files and cities
    municipios_sp = ["Chiquinquira", "Cumaribo", "Ricaurte", "Risaralda", "Tenjo"]
    terrenos_sp = ["R_TERRENO.shp", "U_TERRENO.shp"]
    permutations = [(m, t) for m in municipios_sp for t in terrenos_sp]
    permutations.pop(2) #no hay shape de cumaribo rural
    
    # create file name
    files ="zip://" + data_path.replace("\\", "/")+"/Informacion_Geografica.zip!{}/{}"
    
    # create empty dataframe
    shapes = gpd.GeoDataFrame()
    
    # try to read data
    for m, t in permutations:
    
        # tenjo files are mispelled
        if m == "Tenjo":
            t = t.replace("RR", "RRR")
        
        # create file name
        file = files.format(m, t)
    
        # try reading as some cities are incomplete
        try:
            data = gpd.read_file(file)
            data["origin"] = m                  # add city or department column
            data["file"] = t                    # add file name
            shapes = pd.concat([shapes, data])  # concat files
        except:
            # print filenames that could not be read
            print("Unable to open file {}".format(file)) 
            continue
    
    # create centroid of polygons, latitude and longitude variables
    shapes["centroid"] = shapes["geometry"].centroid
    shapes["lon"] = shapes.centroid.x
    shapes["lat"] = shapes.centroid.y
       
    mun_code = {
        'Pereira':66001,'Apía':66045,'Balboa':66075,'Belén de Umbría':66088,
        'Dosquebradas':66170,'Guática':66318,'La Celia':66383,'La Virginia':66400,
        'Marsella':66440,'Mistratató':66456,'Pueblo Rico':66572,'Quinchia':66594,
        'Santa Rosa de Cabal':66682,'Santuario':66687,'Chiquinquirá':15176, 
        'Cumaribo':99773, 'Ricaurte':25612,'Tenjo':25799,'Manizales':17001
    }
    
    # create a dataframe
    municipio_df = pd.DataFrame(mun_code, index=[0]).T.reset_index()
    
    # rename columns and add Departamento
    municipio_df.columns  = ["MUNICIPIO", "CODIGO_DANE_MUNICIPIO"]
    
    
    municipio_df['Departamento'] = [
        'Risaralda', 'Risaralda', 'Risaralda', 'Risaralda', 'Risaralda', 
        'Risaralda', 'Risaralda', 'Risaralda', 'Risaralda', 'Risaralda',
        'Risaralda', 'Risaralda', 'Risaralda', 'Risaralda', 'Boyacá',
        'Vichada', 'Cundinamarca', 'Cundinamarca', 'Caldas'
    ]
    
    """**Poner nombres de municipios y deptos**"""
    
    avaluo['AVALUO_MILLONES'] = avaluo['AVALUO']/1000000
    
    # merge data
    avaluo = pd.merge(
        avaluo, 
        municipio_df, 
        left_on="MUNICIPIO",
        right_on='CODIGO_DANE_MUNICIPIO'
    )
    
    """**poner detalles al avaluo que tiene nombres de deptos y mun**"""
    
    # merge apraissal with detailed information
    avaluo_detail_asp = pd.merge(avaluo, detail_asp, on='NUMERO_PREDIAL_NACIONAL')
    
    # drop some columns not used
    avaluo_detail_asp.drop(labels=['DEPARTAMENTO_x', 'MUNICIPIO_x','MUNICIPIO'], axis=1,inplace=True)
    
    # create a copy to manipulate
    resume_av_det=avaluo_detail_asp.copy()
    
    ## work with the properties that only have one built area 
    ## and summarize some variables
    
    # total rooms
    resume_av_det['HABITACIONES_2_3'] = resume_av_det['HABITACIONES_2']+resume_av_det['HABITACIONES_3']
    
    # total baths
    resume_av_det['BANOS_2_3']=resume_av_det['BANOS_2']+resume_av_det['BANOS_3']
    
    # total commerce
    resume_av_det['LOCALES_2_3']=resume_av_det['LOCALES_2']+resume_av_det['LOCALES_3']
    
    # these should not be done
    # total floors
    resume_av_det['PISOS_2_3']=resume_av_det['PISOS_2']+resume_av_det['PISOS_3']
    #
    # total stratum
    resume_av_det['ESTRATO_2_3']=resume_av_det['ESTRATO_2']+resume_av_det['ESTRATO_3']
    #
    # total use
    resume_av_det['USO_2_3']=resume_av_det['USO_2']+resume_av_det['USO_3']
    #
    # total score
    resume_av_det['PUNTAJE_2_3']=resume_av_det['PUNTAJE_2']+resume_av_det['PUNTAJE_3']
    
    # total area
    resume_av_det['AREA_CONSTRUIDA_2_3']=resume_av_det['AREA_CONSTRUIDA_2']+resume_av_det['AREA_CONSTRUIDA_3']
    
    # create column to make a filter later
    resume_av_det['Otros'] = (
        resume_av_det['HABITACIONES_2_3'] + resume_av_det['BANOS_2_3'] + 
        resume_av_det['LOCALES_2_3'] + resume_av_det['PISOS_2_3'] + 
        resume_av_det['ESTRATO_2_3'] + resume_av_det['USO_2_3'] + 
        resume_av_det['PUNTAJE_2_3'] + resume_av_det['AREA_CONSTRUIDA_2_3']+
        resume_av_det['ZONA_FISICA_2']+resume_av_det['ZONA_ECONOMICA_2']+resume_av_det['AREA_TERRENO_2']
    )
    
    # drop duplicates until it is cleared how to treat them 
    resume_av_det.drop_duplicates(subset='NUMERO_PREDIAL', keep=False, inplace=True)
    
    # filter the rows that only have one built area
    resume_av_det = resume_av_det[resume_av_det['Otros']==0]
    
    # drop columns related with AREA CONSTRUIDA 2 and AREA CONSTRUIDA 3
    data = resume_av_det[['ZONA',	'NUMERO_PREDIAL',	'NUMERO_PREDIAL_NACIONAL',	'AVALUO',	'AVALUO_MILLONES',	'MUNICIPIO_y',	
        'CODIGO_DANE_MUNICIPIO',	'Departamento',	'DEPARTAMENTO_y','NUMERO_DEL_PREDIO',	'ZONA_FISICA_1','ZONA_ECONOMICA_1',	'AREA_TERRENO_1',	
         'HABITACIONES_1',	'BANOS_1',	'LOCALES_1','PISOS_1',	'ESTRATO_1',	'USO_1',	'PUNTAJE_1',	'AREA_CONSTRUIDA_1']]

    # merge with avaluo table to get the economic destination and adress
    data = pd.merge(data, general_asp, on='NUMERO_PREDIAL_NACIONAL')
    
    # drop some repeated columns
    data.drop(columns=['DEPARTAMENTO', 'MUNICIPIO', 'NUMERO_DEL_PREDIO_y'], inplace=True)
    
    
    """**limpieza**"""
        
    # create function to detect outliers
    def detect_outlier(data_1):
        outliers = []
        threshold = 3
        mean_1 = np.mean(data_1) 
        std_1 = np.std(data_1) 
    
        for y in data_1: 
            z_score = (y - mean_1)/std_1 
            if np.abs(z_score) > threshold: 
                outliers.append(y) 
    
        return outliers
    
    # create outlieres
    data['AREA_TOTAL'] = data['AREA_CONSTRUIDA'] + data['AREA_TERRENO']
    outl = detect_outlier(data['AREA_TOTAL'])
    outavaluo = detect_outlier(data['AVALUO_MILLONES'])
    
    # drop area oultiers
    data = data[~data["AREA_TOTAL"].isin(outl)]
    
    # drop apraissal outliers
    data = data[~data["AVALUO_MILLONES"].isin(outavaluo)]
    
    # create list of indigenous communities
    indigenous_comm = [
        'WAYU', 'KOGUI', 'ARHUACO', 'CHIMILA', 'ARZARIO', 'YUCO', 'YUKPA', 'ZENU',
        'MOTILON', 'BARI', 'TULE', 'EMBERA', 'EMBERA', 'KATIO', 'WUONAAN', 
        'COYAIMA', 'DUJO', 'EPERARA', 'SIAPIDARA', 'MISAK', 'YANACONA', 'NASA',
        'AWA', 'KUAIKER', 'CAMENTSA', 'COREGUAJE', 'COFAN', 'PIJAO', 'DESANO', 
        'UITOTO', 'COCAIMA', 'TANIMUKA', 'TAIWANO', 'NUKAK', 'MAKU', 'TUKANO',
        'BARASANA', 'CURRIPACO', 'ACHAGUA', 'PUINAVE', 'ANDOKE', 'CUBEO', 'SIKUANI',
        'AMORUA', 'CUIBA', 'BETOYE', 'CHIRICOA', 'YUWA', 'GUAHIBO', 'PIAPOCO',
        'GUARATAROS'
    ]
    
    # create empty dataframe
    indigenous = data[
            (data['DIRECCION'].str.contains("INDIGENA", na = False)) | 
            (data['DIRECCION'].str.contains("RESGUARDO"))
        ] 
    
    # create indigenous dataframe
    for x in indigenous_comm:
        y = data[data['DIRECCION'].str.contains(x, na = False)] 
        indigenous = pd.concat([indigenous, y], axis=0)
    
    # drop indigenous data
    data.drop([*indigenous.index], inplace=True)
            
    # merge data
    data_shape = pd.merge(data, shapes[['codigo','lon','lat']],left_on='NUMERO_PREDIAL_NACIONAL', right_on='codigo')
    
    # create some columns
    data_shape['FLAG_AREA_CONSTRUIDA'] = data_shape['AREA_CONSTRUIDA']>0
    data_shape['AREA_TOTAL'] = data_shape['AREA_TERRENO'] + data_shape['AREA_CONSTRUIDA']
    data_shape['PRECIO_POR_M2'] = data_shape['AVALUO_MILLONES']/data_shape['AREA_TOTAL']
    
    # drop some unused columns
    data_shape.drop(
        labels=['codigo','DIRECCION','NUMERO_PREDIAL','AVALUO','NUMERO_DEL_PREDIO_x','DEPARTAMENTO_y','CODIGO_DANE_MUNICIPIO'],
        axis=1,
        inplace=True
    )
    

    # clean some data
    clean = np.where(
        (data_shape["AVALUO_MILLONES"] > 0) & 
        (data_shape["AREA_TOTAL"] > 0) 
    )
    
    data_clean = data_shape.iloc[clean].copy()
        
    data_clean.to_csv(data_path+'/data_clean.csv')
    return data_clean

