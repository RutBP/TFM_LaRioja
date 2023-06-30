import numpy as np
import rasterio
import tifffile

municipalities_path = 'RasterMaps/Municipios.tif'
centers_path = 'RasterMaps/NucleoUrbano.tif'
education_path = 'RasterMaps/Colegios.tif'
inhabitants_path = 'RasterMaps/Habitantes.tif'
roads_path = 'RasterMaps/RedCarreteras.tif'

with rasterio.open(municipalities_path) as dataset:
    matrix_municipalities = dataset.read(1).astype(int)
matrix_municipalities[matrix_municipalities == 255] = 0

with rasterio.open(centers_path) as dataset:
    matrix_populationCenters = dataset.read(1).astype(int)

with rasterio.open(education_path) as dataset:
    matrix_educationalCenters = dataset.read(1).astype(int)
matrix_educationalCenters[matrix_educationalCenters == -128] = 0

with rasterio.open(inhabitants_path) as dataset:
    matrix_inhabitans = dataset.read(1).astype(int)
matrix_inhabitans = np.clip(matrix_inhabitans, 0, None)

with rasterio.open(roads_path) as dataset:
    matrix_roads = dataset.read(1).astype(int)

valores_unicos = np.unique(matrix_roads)

n = matrix_municipalities.shape[0]
m = matrix_municipalities.shape[1]

T = np.random.default_rng()
Tinit = (T.random(size = (800, 1201), dtype = np.float32)*22).astype(int)
 
timeStayed = (Tinit*matrix_populationCenters).astype(int)

def atractor_population(matrix_inhabitans):
    atractor_population = np.empty_like(matrix_inhabitans).astype(float)
    for i in range(atractor_population.shape[0]):
        for j in range(atractor_population.shape[1]):
            if matrix_inhabitans[i, j] >= 10000:
                atractor_population[i,j] = np.random.uniform(0.3, 1)
            elif (matrix_inhabitans[i, j] >= 1000) & (matrix_inhabitans[i, j] < 10000):
                atractor_population[i,j] = np.random.uniform(0.3, 0.8)
            elif (matrix_inhabitans[i, j] >= 1) & (matrix_inhabitans[i, j] < 1000):
                atractor_population[i,j] = np.random.uniform(0.001, 0.4)
            else:
                atractor_population[i,j] = 0
                        
    meanAPob = np.empty_like(atractor_population).astype(float)
    
    for i in range(meanAPob.shape[0]):
        for j in range(meanAPob.shape[1]):
            if i == 0:
                if j == 0:
                    APopulation = atractor_population[0:2, 0:2]
                elif j == m-1:
                    APopulation = atractor_population[0:2, m-2:m]
                else:
                    APopulation = atractor_population[0:2, j-1:j+2]
                    
            elif i == n-1: 
                if j == 0:
                    APopulation = atractor_population[n-2:n, 0:2]
                elif j == n-1:
                    APopulation = atractor_population[n-2:n, m-2:m]
                else:
                    APopulation = atractor_population[n-2:n, j-1:j+2]
            else:
                if j == 0:
                    APopulation = atractor_population[i-1:i+2, 0:2]
                elif j == m-1:
                    APopulation = atractor_population[i-1:i+2, m-2:m]
                else:
                    APopulation = atractor_population[i-1:i+2, j-1:j+2]

            meanAPob[i, j] = APopulation.mean()

    return meanAPob

def atractor_education(matrix_educationalCenters):
    atractor_education = np.empty_like(matrix_educationalCenters).astype(float)
    for i in range(atractor_education.shape[0]):
        for j in range(atractor_education.shape[1]):
            if matrix_educationalCenters[i, j] >= 10:
                atractor_education[i,j] = np.random.uniform(0.3, 1)
            elif (matrix_educationalCenters[i, j] <= 10) & (matrix_educationalCenters[i, j] > 2):
                atractor_education[i,j] = np.random.uniform(0.3, 0.8)
            elif (matrix_educationalCenters[i, j] >= 1) & (matrix_educationalCenters[i, j] <= 2):
                atractor_education[i,j] = np.random.uniform(0.3, 0.6)
            else:
                atractor_education[i,j] = 0
                        
    meanAEducation = np.empty_like(atractor_education).astype(float)
    
    for i in range(meanAEducation.shape[0]):
        for j in range(meanAEducation.shape[1]):
            if i == 0:
                if j == 0:
                    AEducation = atractor_education[0:2, 0:2]
                elif j == m-1:
                    AEducation = atractor_education[0:2, m-2:m]
                else:
                    AEducation = atractor_education[0:2, j-1:j+2]
                    
            elif i == n-1: 
                if j == 0:
                    AEducation = atractor_education[n-2:n, 0:2]
                elif j == n-1:
                    AEducation = atractor_education[n-2:n, m-2:m]
                else:
                    AEducation = atractor_education[n-2:n, j-1:j+2]
            else:
                if j == 0:
                    AEducation = atractor_education[i-1:i+2, 0:2]
                elif j == m-1:
                    AEducation = atractor_education[i-1:i+2, m-2:m]
                else:
                    AEducation = atractor_education[i-1:i+2, j-1:j+2]

            meanAEducation[i, j] = AEducation.mean()

    return meanAEducation

def atractor_road(matrix_roads):
    atractor_road = np.empty_like(matrix_roads).astype(float)

    for i in range(atractor_road.shape[0]):
        for j in range(atractor_road.shape[1]):
            if matrix_roads[i, j] == 1:
                atractor_road[i,j] = np.random.uniform(0.4, 1)
            else:
                atractor_road[i,j] = 0
                        
    meanARoad = np.empty_like(atractor_road).astype(float)
    
    for i in range(meanARoad.shape[0]):
        for j in range(meanARoad.shape[1]):
            if i == 0:
                if j == 0:
                    ACarreteras = atractor_road[0:2, 0:2]
                elif j == m-1:
                    ACarreteras = atractor_road[0:2, m-2:m]
                else:
                    ACarreteras = atractor_road[0:2, j-1:j+2]
                    
            elif i == n-1: 
                if j == 0:
                    ACarreteras = atractor_road[n-2:n, 0:2]
                elif j == n-1:
                    ACarreteras = atractor_road[n-2:n, m-2:m]
                else:
                    ACarreteras = atractor_road[n-2:n, j-1:j+2]
            else:
                if j == 0:
                    ACarreteras = atractor_road[i-1:i+2, 0:2]
                elif j == m-1:
                    ACarreteras = atractor_road[i-1:i+2, m-2:m]
                else:
                    ACarreteras = atractor_road[i-1:i+2, j-1:j+2]

            meanARoad[i, j] = ACarreteras.mean()

    return meanARoad

Atractor = 0.5 * atractor_road(matrix_roads) + 1.5*atractor_education(matrix_educationalCenters) + 0.9 * atractor_population(matrix_inhabitans)

#Movimiento de la poblacion para 50 iteraciones de tiempo 

for iteration in range(50):
    matrix_inhabitants_copy = matrix_inhabitans.copy()

    available_positions = np.argwhere(matrix_municipalities != 0)
    num_inhabitants = 200

    random_indices = np.random.choice(available_positions.shape[0], num_inhabitants, replace=False)
    random_positions = available_positions[random_indices]

    for position in random_positions:
        rand_i, rand_j = position
        matrix_inhabitants_copy[rand_i, rand_j] += 1

    for i in range(1, matrix_inhabitants_copy.shape[0] - 1):
        for j in range(1, matrix_inhabitants_copy.shape[1] - 1):
            if matrix_municipalities[i, j] != 0: 
                if (10 < timeStayed[i,j]) & (timeStayed[i,j] < 21):
                    if Atractor[i,j] < 0.9:
                        possible_locations = [[i-1, j-1],[i-1, j],[i-1, j+1],[i, j-1],[i, j+1],[i+1, j-1],[i+1, j],[i+1, j+1]]

                        rng = np.random.default_rng() 
                        movement = rng.integers(low=0, high=7, endpoint=True)

                        new_pos = possible_locations[movement]

                        if matrix_inhabitants_copy[i, j] > 0:
                            matrix_inhabitants_copy[i, j] -= 1
                            matrix_inhabitants_copy[new_pos[0], new_pos[1]] += 1
                        
                        timeStayed[i,j] = 0
                    
                    else:
                        matrix_inhabitants_copy[i,j]

                elif timeStayed[i,j] == 21:
                    if Atractor[i,j] < 2.0:
                        possible_locations = [[i-1, j-1],[i-1, j],[i-1, j+1],[i, j-1],[i, j+1],[i+1, j-1],[i+1, j],[i+1, j+1]]

                        rng = np.random.default_rng() 
                        movement = rng.integers(low=0, high=7, endpoint=True)

                        new_pos = possible_locations[movement]

                        if matrix_inhabitants_copy[i, j] > 0:
                            matrix_inhabitants_copy[i, j] -= 1
                            matrix_inhabitants_copy[new_pos[0], new_pos[1]] += 1

                        timeStayed[i,j] = 0
                            
                    else:
                        matrix_inhabitants_copy[i,j]
                
                else:
                    matrix_inhabitants_copy[i,j]

            else:
                matrix_inhabitants_copy[i,j] = 0

    matrix_inhabitans = matrix_inhabitants_copy
    timeStayed += 1
    timeStayed = timeStayed % 22    

    output_directory = 'ResultsPopulation'
    tifffile.imwrite(f"{output_directory}/PopulationMigration_{iteration}.tif", matrix_inhabitans)
