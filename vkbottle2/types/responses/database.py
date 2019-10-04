from .others import SimpleResponse
from ..base import BaseModel

from ..additional import MetroStation


import typing


class GetChairsResponse(BaseModel):
    count: int = None
    items: typing.List[dict] = None


class GetChairs(BaseModel):
    response: GetChairsResponse = None


class GetCitiesResponse(BaseModel):
    count: int = None
    items: typing.List[dict]


class GetCities(BaseModel):
    response: GetCitiesResponse = None


class GetCitiesByIdResponse(BaseModel):
    id: int = None
    title: str = None


class GetCitiesById(BaseModel):
    response: typing.List[GetCitiesByIdResponse] = None


class GetCountriesResponse(BaseModel):
    count: int = None
    items: typing.List[GetCitiesByIdResponse] = None


class GetCountries(BaseModel):
    response: GetCountriesResponse = None


class GetCountriesById(BaseModel):
    response: typing.List[GetCitiesByIdResponse] = None


class GetFaculties(GetCountries):
    pass


class GetMetroStationsResponse(BaseModel):
    count: int = None
    items: typing.List[MetroStation] = None


class GetMetroStations(BaseModel):
    response: GetMetroStationsResponse = None


class GetMetroStationsById(BaseModel):
    response: typing.List[MetroStation] = None


class GetRegions(BaseModel):
    response: GetCountriesResponse = None


class GetSchoolClasses(BaseModel):
    response: typing.List = None


class GetSchools(BaseModel):
    response: typing.List[GetCountriesResponse] = None


class GetUniversities(BaseModel):
    response: typing.List[GetCountriesResponse] = None
