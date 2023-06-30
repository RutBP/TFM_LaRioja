import numpy as np
import rasterio
import tifffile
from scipy import ndimage

altimetria_path = 'RasterMaps/Altimetria.tif'
nucleos_path = 'RasterMaps/NucleoUrbano.tif'
isoterma_path = 'RasterMaps/Isotermas.tif'
isoyetas_path = 'RasterMaps/Isoyetas.tif'
litoestratigrafia_path = 'RasterMaps/Litologia.tif'
municipios_path = 'RasterMaps/Municipios.tif'
hidrologia_path = 'RasterMaps/Hidrologia.tif'
caudal_path = 'RasterMaps/Caudales.tif'

with rasterio.open(altimetria_path) as dataset:
    matriz_altimetria = dataset.read(1).astype(int)
matriz_altimetria = np.delete(matriz_altimetria, 1, axis=1)
matriz_altimetria = np.clip(matriz_altimetria, 0, None)

with rasterio.open(nucleos_path) as dataset:
    matriz_nucleos = dataset.read(1).astype(int)

with rasterio.open(isoyetas_path) as dataset:
    matriz_isoyetas = dataset.read(1).astype(int)
matriz_isoyetas[matriz_isoyetas == 65535] = 0

with rasterio.open(municipios_path) as dataset:
    matriz_municipios = dataset.read(1).astype(int)
matriz_municipios[matriz_municipios == 255] = 0

with rasterio.open(isoterma_path) as dataset:
    matriz_isoterma = dataset.read(1).astype(float)
matriz_isoterma[matriz_isoterma == 15] = 0

with rasterio.open(hidrologia_path) as dataset:
    matriz_hidrologia = dataset.read(1).astype(int)

with rasterio.open(caudal_path) as dataset:
    matriz_caudal = dataset.read(1).astype(float)
matriz_caudal = np.clip(matriz_caudal, 0, None)
matriz_caudal[matriz_caudal == 1.400e+04] = 0

matriz_climatologia = np.empty_like(matriz_municipios).astype(float)

for iteration in range(50):

    water_level = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))
    water_level[matriz_caudal == 0] = 0
    water_level[matriz_caudal == 402.4] = np.random.uniform(3.5, 4.5, size=np.sum(matriz_caudal == 402.4))
    water_level[(matriz_caudal >= 15.) & (matriz_caudal < 402.4)] = np.random.uniform(0.5, 2, size=np.sum((matriz_caudal >= 15.) & (matriz_caudal < 402.4)))
    water_level[(matriz_caudal > 0.) & (matriz_caudal < 15.)] = np.random.uniform(0.2, 1, size=np.sum((matriz_caudal > 0) & (matriz_caudal < 15.0)))

    precipitation_random = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))
    precipitation_random[matriz_altimetria == 0] = 0
    precipitation_random[matriz_altimetria > 300] = np.random.uniform(-0.2, 0.2, size=np.sum(matriz_altimetria > 300))

    precipitation = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))
    precipitation = matriz_isoyetas + precipitation_random * matriz_isoyetas

    temperatura_random = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))
    temperatura_random[matriz_altimetria == 0] = 0
    temperatura_random[matriz_altimetria > 300] =  np.random.uniform(-0.2, 0.2, size=np.sum(matriz_altimetria > 300))

    temperatura = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))
    temperatura= matriz_isoterma + temperatura_random * matriz_isoterma

    evapotranspiracion_random = np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))

    evapotranspiracion_random[matriz_altimetria == 0] = 0
    evapotranspiracion_random[(matriz_altimetria > 300) & (matriz_altimetria <= 600)] = np.random.uniform(-20, 20, size=np.sum((matriz_altimetria > 300) & (matriz_altimetria <= 600)))
    evapotranspiracion_random[(matriz_altimetria > 600)] = np.random.uniform(-100, 100, size=np.sum(matriz_altimetria > 600)) 

    evapotranspiracion= np.zeros((matriz_climatologia.shape[0], matriz_climatologia.shape[1]))

    evapotranspiracion[matriz_altimetria == 0] = 0
    evapotranspiracion[(matriz_altimetria > 300) & (matriz_altimetria <= 600)] = 40 + evapotranspiracion_random[(matriz_altimetria > 300) & (matriz_altimetria <= 600)]
    evapotranspiracion[matriz_altimetria > 600] = 400 + evapotranspiracion_random[matriz_altimetria > 600]
    
    matriz_climatologia_copy = np.copy(matriz_climatologia)

    for i in range(1, matriz_climatologia_copy.shape[0]-1):
        for j in range(1, matriz_climatologia_copy.shape[1]-1):

            if matriz_municipios[i, j] != 0:
                if matriz_hidrologia[i, j] == 1:
                    if matriz_altimetria[i, j] <= 500: 
                        matriz_climatologia_copy[i, j] = precipitation[i, j] + water_level[i, j] - matriz_caudal[i, j] - 90 * temperatura[i, j]
                        
                    else:
                        matriz_climatologia_copy[i, j] = precipitation[i, j] + water_level[i, j] - matriz_caudal[i, j] - 90 * temperatura[i, j] + 300
                        
                else: 
                    matriz_climatologia_copy[i, j] = precipitation[i, j] - evapotranspiracion[i, j]
            else: matriz_climatologia_copy[i, j] = 0

    matriz_climatologia = ndimage.minimum_filter(matriz_climatologia_copy, size=3)

    output_directory = 'ResultsFlux'
    tifffile.imwrite(f"{output_directory}/WaterFlow_{iteration}.tif", matriz_climatologia)
