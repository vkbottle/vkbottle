import typing
from ..base import BaseModel
from vkbottle.types import objects


class GetUniversities(BaseModel):
    count: int = None
    items: typing.List = None


class GetUniversitiesModel(BaseModel):
    response: GetUniversities = None


class GetChairs(BaseModel):
    count: int = None
    items: typing.List = None


class GetChairsModel(BaseModel):
    response: GetChairs = None


GetCitiesById = typing.List[objects.base.Object]


class GetCitiesByIdModel(BaseModel):
    response: GetCitiesById = None


class GetCities(BaseModel):
    count: int = None
    items: typing.List = None


class GetCitiesModel(BaseModel):
    response: GetCities = None


GetCountriesById = typing.List[objects.base.Country]


class GetCountriesByIdModel(BaseModel):
    response: GetCountriesById = None


class GetCountries(BaseModel):
    count: int = None
    items: typing.List = None


class GetCountriesModel(BaseModel):
    response: GetCountries = None


class GetFaculties(BaseModel):
    count: int = None
    items: typing.List = None


class GetFacultiesModel(BaseModel):
    response: GetFaculties = None


GetMetroStationsById = typing.List[objects.database.Station]


class GetMetroStationsByIdModel(BaseModel):
    response: GetMetroStationsById = None


class GetMetroStations(BaseModel):
    count: int = None
    items: typing.List = None


class GetMetroStationsModel(BaseModel):
    response: GetMetroStations = None


class GetRegions(BaseModel):
    count: int = None
    items: typing.List = None


class GetRegionsModel(BaseModel):
    response: GetRegions = None


GetSchoolClasses = typing.List[typing.List]


class GetSchoolClassesModel(BaseModel):
    response: GetSchoolClasses = None


class GetSchools(BaseModel):
    count: int = None
    items: typing.List = None


class GetSchoolsModel(BaseModel):
    response: GetSchools = None
