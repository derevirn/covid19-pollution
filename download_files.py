from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson

user = 's5pguest' 
password = 's5pguest' 
#This is GeoJSON coordinates file with a rectangular shape,
#covering the geographic region of Italy and Greece.
area = r'map.geojson'

#Accessing the Sentinel-5P API to download the Nitrogen Dioxide (NO2) products
#for the area specified in the GeoJSON file.
api = SentinelAPI(user, password, 'https://s5phub.copernicus.eu/dhus')
footprint = geojson_to_wkt(read_geojson(area))

#Creating two sets of products for March 2019 and March 2020,
#So we can compare the levels of NO2 in our analysis
products_2019 = api.query(footprint, date = ('20190301', '20190401'),
                     producttype = 'L2__NO2___' )

products_2020 = api.query(footprint, date = ('20200301', '20200401'),
                     producttype = 'L2__NO2___' )

#Downloading all the products in the L2 folder
api.download_all(products_2019, directory_path='data\L2')
api.download_all(products_2020, directory_path='data\L2')
