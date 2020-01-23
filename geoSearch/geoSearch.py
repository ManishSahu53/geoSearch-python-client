"""
Main module
"""
import os
import sys
from geoSearch.config import defaultConfig
from geoSearch.src import util
import logging
import requests


class exceptions(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class resource:
    def __init__(self):
        super().__init__()

    def getSatellite(self):
        return defaultConfig.satellite

    def getIndices(self, satellite=None):
        if satellite is None:
            return defaultConfig.indices

        elif satellite in self.getSatellite():
            return defaultConfig.indices[satellite]

        else:
            raise exceptions(
                'Satellite {} is not available. To see available satellites are : {})'
                .format(satellite, self.getSatellite()))


class client(object):
    """
    This is main client class which is input source to get into this API system
    """

    def __init__(self, apikey=None):
        super().__init__()
        self.searchEndpoint = defaultConfig.searchEndpoint

        self.visualiseEndpoint = defaultConfig.visualiseEndpoint
        self.valueEndpoint = defaultConfig.valueEndpoint
        self.statsEndpoint = defaultConfig.statsEndpoint
        self.boundsEndpoint = defaultConfig.boundsEndpoint
        self.timelineValueEndpoint = defaultConfig.timelineValueEndpoint
        self.timelineStatsEndpoint = defaultConfig.timelineStatsEndpoint
        self.thumbnailEndpoint = defaultConfig.thumbnailEndpoint

        self.minCloudCover = 0
        self.maxCloudCover = 50
        self.minCoverage = 0
        self.maxCoverage = 100
        self.apikey = apikey

        if self.checkKey() is False:
            print('Invalid Auth')
            raise exceptions(
                'Invalid Auth key. Get valid Auth key to continue')
        else:
            print('Successfully Authenticated')

    def checkKey(self):
        """
        checkKey is used to check for authentication
        """
        # TO DO for checking API authentication
        if self.apikey is None:
            return False
        else:
            return True

    def update(self):
        """
        This function is used to update API endpoints
        """
        # TO DO for updating urls if changed
        pass

    def getSearch(self, satellite: str,
                startDate: str, endDate: str,
                latitude: float, longitude: float,
                minCloudCover=None, maxCloudCover=None,
                minCoverage=None, maxCoverage=None,
                ) -> list:
        """
        getData is used to get satellite json data from the server.
        Input:
            satellite: landsat8 or l8
            startDate: YYYY-MM-DD
            endDate: YYYY-MM-DD
            latitude: float
            longitude: float
            minCloudCover: int
            maxCloudCover: int
            minCoverage: int
            maxCoverage: int
        output:
            Dict of list of data present at given location
        """
        if satellite.lower() == 'landsat8':
            satellite = 'l8'

        minCloudCover = self.minCloudCover if minCloudCover is None else minCloudCover
        maxCloudCover = self.maxCloudCover if maxCloudCover is None else maxCloudCover
        minCoverage = self.minCoverage if minCoverage is None else minCoverage
        maxCoverage = self.maxCoverage if maxCoverage is None else maxCoverage

        param = {
            'table_name': 'satellite_dataset_prod',
            'satellite': satellite.lower(),
            'start_date': startDate,
            'end_date': endDate,
            'min_cloudcover': int(minCloudCover),
            'max_cloudcover': int(maxCloudCover),
            'min_coverage': int(minCoverage),
            'max_coverage': int(maxCoverage),
            'x': float(longitude),
            'y': float(latitude)
        }
        try:
            response = requests.get(url=self.searchEndpoint, params=param)
        except Exception as e:
            raise exceptions(
                'Unable to reach to server. \
                    Make sure url is correct, updated and \
                        you are connected to Internet. Error : {}'.format(e))

        return response.json()


    def getValue(self, url: str, latitude: list,
                 longitude: list, satellite='l8', index='ndvi'):

        """
        getData is used to get satellite json data from the server.
        Input:
            url: url of json
            latitude: list of float
            longitude: list of float
            satellite: 'l8'
            index: 'ndvi'
        output:
            dict with list of data points
        """
        if type(latitude) is not list:
            latitude = [str(latitude)]
        else:
            latitude = [str(l) for l in latitude]

        if type(longitude) is not list:
            longitude = [str(longitude)]
        else:
            longitude = [str(l) for l in longitude]

        param = {
            'url': url,
            'x': ','.join(longitude),
            'y': ','.join(latitude),
            'satellite': satellite,
            'index': index
        }

        try:
            response = requests.get(url=self.valueEndpoint, params=param)
        except Exception as e:
            raise exceptions(
                'Unable to reach to value endpoint. Error: {}'.format(e))

        return response.json()


    def getStats(self, url: str, latitude: list,
                 longitude: list, satellite='l8', index='ndvi'):
        """
        getData is used to get satellite json data from the server.
        Input:
            url : url of stac json
            satellite: landsat8 or l8
            index: 'ndvi'
            latitude: list of float
            longitude: list of float
        output:
            dict with list of data points for statistics
        """

        if type(latitude) is not list:
                latitude = [str(latitude)]
        else:
            latitude = [str(l) for l in latitude]

        if type(longitude) is not list:
            longitude = [str(longitude)]
        else:
            longitude = [str(l) for l in longitude]

        param = {
            'url': url,
            'x': ','.join(longitude),
            'y': ','.join(latitude),
            'satellite': satellite,
            'index': index
        }

        try:
            response = requests.get(url=self.statsEndpoint, params=param)
        except Exception as e:
            raise exceptions(
                'Unable to reach to statistics endpoint. Error: {}'.format(e))

        return response.json()


    def getTimelineValue(self, url: str, latitude: float,
                         longitude: float, startDate: str, endDate: str,
                         minCloudCover=None, maxCloudCover=None,
                         minCoverage=None, maxCoverage=None,
                         satellite='l8', index='ndvi'):
        """
        getData is used to get satellite json data from the server.
        Input:
            url: url of stac json
            satellite: landsat8 or l8
            index: 'ndvi'
            startDate: YYYY-MM-DD
            endDate: YYYY-MM-DD
            latitude: float
            longitude: float
            minCloudCover: int
            maxCloudCover: int
            minCoverage: int
            maxCoverage: int
        output:
            Dict of list of data present at given location
        """

        latitude = str(latitude)
        longitude = str(longitude)
        minCloudCover = self.minCloudCover if minCloudCover is None else minCloudCover
        maxCloudCover = self.maxCloudCover if maxCloudCover is None else maxCloudCover
        minCoverage = self.minCoverage if minCoverage is None else minCoverage
        maxCoverage = self.maxCoverage if maxCoverage is None else maxCoverage

        param = {
            'url': url,
            'x': str(longitude),
            'y': str(latitude),
            'satellite': satellite.lower(),
            'index': index,
            'start_date': startDate,
            'end_date': endDate,
            'min_cloudcover': int(minCloudCover),
            'max_cloudcover': int(maxCloudCover),
            'min_coverage': int(minCoverage),
            'max_coverage': int(maxCoverage),
        }

        try:
            response = requests.get(url=self.timelineValueEndpoint, params=param)
        except Exception as e:
            raise exceptions(
                'Unable to reach to value endpoint. Error: {}'.format(e))

        return response.json()


    def getTimelineStats(self, url: str, latitude: list,
                         longitude: list, startDate: str, endDate: str,
                         minCloudCover=None, maxCloudCover=None,
                         minCoverage=None, maxCoverage=None,
                         satellite='l8', index='ndvi'):
        """
        getData is used to get satellite json data from the server.
        Input:
            url: str:url of stac json
            satellite: str:landsat8 or l8
            index: str:'ndvi'
            startDate: YYYY-MM-DD
            endDate: YYYY-MM-DD
            latitude: float
            longitude: float
            minCloudCover: int
            maxCloudCover: int
            minCoverage: int
            maxCoverage: int
        output:
            Dict of list of data present at given location
        """

        if type(latitude) is not list:
            latitude = [str(latitude)]
        else:
            latitude = [str(l) for l in latitude]

        if type(longitude) is not list:
            longitude = [str(longitude)]
        else:
            longitude = [str(l) for l in longitude]

        minCloudCover = self.minCloudCover if minCloudCover is None else minCloudCover
        maxCloudCover = self.maxCloudCover if maxCloudCover is None else maxCloudCover
        minCoverage = self.minCoverage if minCoverage is None else minCoverage
        maxCoverage = self.maxCoverage if maxCoverage is None else maxCoverage

        param = {
            'url': url,
            'x': ','.join(longitude),
            'y': ','.join(latitude),
            'satellite': satellite.lower(),
            'index': index,
            'start_date': startDate,
            'end_date': endDate,
            'min_cloudcover': int(minCloudCover),
            'max_cloudcover': int(maxCloudCover),
            'min_coverage': int(minCoverage),
            'max_coverage': int(maxCoverage),
        }

        try:
            response = requests.get(url=self.timelineStatsEndpoint, params=param)
        except Exception as e:
            raise exceptions(
                'Unable to reach to value endpoint. Error: {}'.format(e))

        return response.json()


    # Resources in this framework
    def getSatelliteInfo(self):
        return defaultConfig.satellite


    def getIndicesInfo(self, satellite=None):
        if satellite is None:
            return defaultConfig.indices

        elif satellite in self.getSatelliteInfo():
            return defaultConfig.indices[satellite]

        else:
            raise exceptions(
                'Satellite {} is not available. To see available satellites are : {})'
                .format(satellite, self.getSatelliteInfo()))
