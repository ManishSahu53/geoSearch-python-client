import os

# Default EPSG code
defaultEPSG = 'EPSG:4326'

# Primitive endpoint
searchEndpoint= 'http://52.15.146.163:5000/api/v1/search?'
lambdaEndpoint= 'https://j4r5f4hxvd.execute-api.us-west-2.amazonaws.com/prod/api/v1'

# Derived endpoint
visualiseEndpoint=os.path.join(lambdaEndpoint, 'index/{x}/{y}/{z}?')
valueEndpoint=os.path.join(lambdaEndpoint, 'value?')
statsEndpoint=os.path.join(lambdaEndpoint, 'stats?')
boundsEndpoint=os.path.join(lambdaEndpoint, 'bounds?')
timelineValueEndpoint=os.path.join(lambdaEndpoint, 'timeline/value?')
timelineStatsEndpoint=os.path.join(lambdaEndpoint, 'timeline/stats?')
thumbnailEndpoint=os.path.join(lambdaEndpoint, 'thumbnail?')

# Satellite sources
satellite = ['landsat8']
indices={
    satellite[0]: ['ndvi', 'ndwi']
}