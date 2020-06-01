import harp
from glob import iglob
from os.path import join
from joblib import Parallel, delayed

#Creating a function that processes the L2 products downloaded from the API
#The HARP tool will be used for the conversion
def process_file(file):
    operations=" \
    tropospheric_NO2_column_number_density_validity>50; \
    derive(tropospheric_NO2_column_number_density [Pmolec/cm2]); \
    derive(datetime_stop {time}); \
    latitude > 34.4 [degree_north] ; latitude < 47.7 [degree_north] ; \
    longitude > 5.8 [degree_east] ; longitude < 28.9 [degree_east] ; \
    bin_spatial(1330, 34.4, 0.01, 2310, 5.8, 0.01); \
    derive(latitude {latitude}); derive(longitude {longitude});\
    keep(NO2_column_number_density, tropospheric_NO2_column_number_density,\
    stratospheric_NO2_column_number_density, NO2_slant_column_number_density,\
    tropopause_pressure,absorbing_aerosol_index,cloud_fraction, datetime_start, longitude, latitude)"
    
    
    try:
        harp_L2_L3 = harp.import_product(file, operations = operations)
        export_folder = "{export_path}\{name}".format(export_path='data\L3',
                        name = file.split('\\')[-1].replace('L2', 'L3'))
        harp.export_product(harp_L2_L3, export_folder, file_format='netcdf')
     
    #Some files may not be suitable for processing due to low quality data
    #or other reasons, so we must handle the associated exception  
    except Exception as e:
        print(e)


input_files = sorted(list(iglob(join('data\L2', '*'), recursive=True)))

#The Parallel class utilizes multiple CPU cores during the processing,
#and completes the task signficantly faster
Parallel(n_jobs=8, verbose=10)(delayed(process_file)(file) for file in input_files)

