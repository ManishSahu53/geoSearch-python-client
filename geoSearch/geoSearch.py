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


class search:
    """
    """
    def __init__(self):
        super().__init__()
        self.endpoint = defaultConfig.searchEndpoint
        self.minCloudCover = 0
        self.maxCloudCover = 50
        self.minCoverage = 0
        self.maxCoverage = 100

    def update(self):
        # TO DO for updating urls if changed
        pass

    def getData(self, satellite,
                startDate, endDate,
                latitude, longitude,
                minCloudCover=None, maxCloudCover=None,
                minCoverage=None, maxCoverage=None,
                ):
        """
        getData is used to get satellite json data from the server.
        Input:
            satellite:
            startDate:
            endDate:
            latitude:
            longitude:
            minCloudCover:
            maxCloudCover:
            minCoverage:
            maxCoverage:
            
        """
        if satellite == 'landsat8':
            satellite = 'l8'

        minCloudCover = self.minCloudCover if minCloudCover is None else minCloudCover
        maxCloudCover = self.maxCloudCover if maxCloudCover is None else maxCloudCover
        minCoverage = self.minCoverage if minCoverage is None else minCoverage
        maxCoverage = self.maxCoverage if maxCoverage is None else maxCoverage

        url = self.endpoint

        param = {
            'table_name': 'satellite_dataset_prod',
            'satellite': satellite,
            'start_date': '2018-01-01',
            'end_date': '2019-07-01',
            'min_cloudcover': minCloudCover,
            'max_cloudcover': maxCloudCover,
            'min_coverage': minCoverage,
            'max_coverage': maxCoverage,
            'x': longitude,
            'y': latitude
        }
        try:
            response = requests.get(url=url, params=param)
        except:
            raise exceptions(
                'Unable to reach to server. Make sure url is correct and you are connected to Internet')

        if response.status_code == 200:
            return response.json()
        else:
            return []