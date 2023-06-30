import numpy as np
import rasterio
import tifffile
from scipy import ndimage

altimetria_path = 'RasterMaps/Altimetria.tif'
nucleos_path = 'RasterMaps/NucleoUrbano.tif'
isoyetas_path = 'RasterMaps/Isoyetas.tif'
nitratos_path = 'RasterMaps/ZonasVulnerables.tif'
red2000_path = 'RasterMaps/RedNatura2000.tif'
municipios_path = 'RasterMaps/Municipios.tif'
kfactor_path = 'RasterMaps/Kfactor.tif'
rfactor_path = 'RasterMaps/Rfactor.tif'

#Open raster files
with rasterio.open(altimetria_path) as dataset:
    matriz_altimetria = dataset.read(1).astype(int)
matriz_altimetria = np.delete(matriz_altimetria, 1, axis=1)
matriz_altimetria = np.clip(matriz_altimetria, 0, None)

with rasterio.open(nucleos_path) as dataset:
    matriz_nucleos = dataset.read(1).astype(int)

with rasterio.open(isoyetas_path) as dataset:
    matriz_isoyetas = dataset.read(1).astype(int)
matriz_isoyetas[matriz_isoyetas == 65535] = 0

with rasterio.open(nitratos_path) as dataset:
    matriz_nitratos = dataset.read(1).astype(int)

with rasterio.open(red2000_path) as dataset:
    matriz_red2000 = dataset.read(1).astype(int)

with rasterio.open(municipios_path) as dataset:
    matriz_municipios = dataset.read(1).astype(int)
matriz_municipios[matriz_municipios == 255] = 0

with rasterio.open(kfactor_path) as dataset:
    matriz_Kfactor = dataset.read(1).astype(float)
matriz_Kfactor = np.clip(matriz_Kfactor, 0, None)

with rasterio.open(rfactor_path) as dataset:
    matriz_Rfactor = dataset.read(1).astype(float)
matriz_Rfactor = np.clip(matriz_Rfactor, 0, None)


#Matrix dimension
n = matriz_municipios.shape[0]
m = matriz_municipios.shape[1]

matriz_erosion = np.empty_like(matriz_municipios).astype(float)

matriz_erosion_copy = matriz_erosion.copy()

for iteration in range(50):
    # Initialize matrices and variables
    matriz_Cfactor = matriz_municipios.astype(bool) * np.random.uniform(0.25, 0.46)
    matriz_Cfactor2 = matriz_municipios.astype(bool) * np.random.uniform(0.7, 0.99)
    matriz_Pfactor = matriz_municipios.astype(bool) * np.random.uniform(0.1, 0.3)
    matriz_Pfactor2 = matriz_municipios.astype(bool) * np.random.uniform(0.3, 0.8)
    matriz_randomR = matriz_Rfactor + (matriz_Rfactor * np.random.uniform(-0.2, 0.5))

    matriz_erosion_copy = matriz_erosion.copy()

    # Handle positions where matriz_municipios is not zero
    mask = np.where(matriz_municipios > 0, True, False)

    # Handle positions where matriz_nitratos is one
    nitratos_mask = np.where(matriz_nitratos == 1, True, False)
    iteration_mask = iteration * np.ones_like(matriz_erosion_copy)

    # Handle positions where matriz_altimetria is less than 600
    altimetria_mask = np.where(matriz_altimetria < 600, True, False)

    # Calculate matriz_erosion_copy based on conditions

    # 1. No municipalities
    matriz_erosion_copy = np.where(~mask, 0, matriz_erosion_copy)

    # 2. Matriz_nitratos
    # 2.1 masl < 600
    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask < 15) & altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.6 * matriz_Cfactor * 0.17,
                                   matriz_erosion_copy)

    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask >= 15) & (iteration_mask < 30) & altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.7 * matriz_Cfactor * 0.17,
                                   matriz_erosion_copy)

    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask >= 30) & altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.8 * matriz_Cfactor * 0.17,
                                   matriz_erosion_copy)

    # 2.2 masl > 600
    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask < 15) & ~altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.6 * matriz_Cfactor * 0.93,
                                   matriz_erosion_copy)

    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask >= 15) & (iteration_mask < 30) & ~altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.7 * matriz_Cfactor * 0.93,
                                   matriz_erosion_copy)

    matriz_erosion_copy = np.where(mask & nitratos_mask & (iteration_mask >= 30) & ~altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * 0.8 * matriz_Cfactor * 0.93,
                                   matriz_erosion_copy)

    # 3. No matriz_nitratos & red2000
    # 3.1 masl < 600
    matriz_erosion_copy = np.where(mask & ~nitratos_mask & matriz_red2000 & altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * matriz_Pfactor * matriz_Cfactor2 * 0.17,
                                   matriz_erosion_copy)

    # 3.2 masl > 600
    matriz_erosion_copy = np.where(mask & ~nitratos_mask & matriz_red2000 & ~altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * matriz_Pfactor * matriz_Cfactor2 * 0.93,
                                   matriz_erosion_copy)

    # 4. No matriz_nitratos & no red2000 & nucleos
    matriz_erosion_copy = np.where(mask & ~nitratos_mask & ~matriz_red2000 & matriz_nucleos,
                                   0, matriz_erosion_copy)

    # 5. No matriz nitratos & no red2000 & no nucleos
    # 5.1 masl < 600
    matriz_erosion_copy = np.where(mask & ~nitratos_mask & ~matriz_red2000 & ~matriz_nucleos & altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * matriz_Pfactor2 * matriz_Cfactor * 0.17,
                                   matriz_erosion_copy)

    # 5.2 masl > 600
    matriz_erosion_copy = np.where(mask & ~nitratos_mask & ~matriz_red2000 & ~matriz_nucleos & ~altimetria_mask,
                                   matriz_Kfactor * matriz_randomR * matriz_Pfactor2 * matriz_Cfactor * 0.93,
                                   matriz_erosion_copy)

    # Apply min kernel to matriz_erosion_copy
    matriz_erosion = ndimage.minimum_filter(matriz_erosion_copy, size=3)

    output_directory = 'ResultsErosion'
    tifffile.imwrite(f"{output_directory}/Erosion_{iteration}.tif", matriz_erosion)
    # print('se ha exportado un raster')