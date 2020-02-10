from .others import SimpleResponse
from ..base import BaseModel

from ..additional import MetroStation


from typing import List


class GetChairsResponse(BaseModel):
    count: int = None
    items: List[dict] = []


class GetChairs(BaseModel):
    response: GetChairsResponse = None


class GetCitiesResponse(BaseModel):
    count: int = None
    items: List[dict] = []


class GetCities(BaseModel):
    response: GetCitiesResponse = None


class GetCitiesByIdResponse(BaseModel):
    id: int = None
    title: str = None


class GetCitiesById(BaseModel):
    response: List[GetCitiesByIdResponse] = []


class GetCountriesResponse(BaseModel):
    count: int = None
    items: List[GetCitiesByIdResponse] = []


class GetCountries(BaseModel):
    response: GetCountriesResponse = None


class GetCountriesById(BaseModel):
    response: List[GetCitiesByIdResponse] = []


class GetFaculties(GetCountries):
    pass


class GetMetroStationsResponse(BaseModel):
    count: int = None
    items: List[MetroStation] = []


class GetMetroStations(BaseModel):
    response: GetMetroStationsResponse = None


class GetMetroStationsById(BaseModel):
    response: List[MetroStation] = []


class GetRegions(BaseModel):
    response: GetCountriesResponse = None


class GetSchoolClasses(BaseModel):
    response: List = []


class GetSchools(BaseModel):
    response: List[GetCountriesResponse] = []


class GetUniversities(BaseModel):
    response: List[GetCountriesResponse] = []
