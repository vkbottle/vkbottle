import typing
from ..base import BaseModel
from vkbottle.types import objects


class GetUniversities(BaseModel):
    count: int = None
    items: typing.List[objects.database.University] = None


class GetUniversitiesModel(BaseModel):
    response: GetUniversities = None


class Chair(BaseModel):
    id: int = None
    title: str = None


class GetChairs(BaseModel):
    count: int = None
    items: typing.List[Chair] = None


class GetChairsModel(BaseModel):
    response: GetChairs = None


GetCitiesById = typing.List[objects.base.Object]


class GetCitiesByIdModel(BaseModel):
    response: GetCitiesById = None


class GetCities(BaseModel):
    count: int = None
    items: typing.List[objects.database.City] = None


class GetCitiesModel(BaseModel):
    response: GetCities = None


GetCountriesById = typing.List[objects.base.Country]


class GetCountriesByIdModel(BaseModel):
    response: GetCountriesById = None


class Country(BaseModel):
    id: int = None
    title: str = None


class GetCountries(BaseModel):
    count: int = None
    items: typing.List[Country] = None


class GetCountriesModel(BaseModel):
    response: GetCountries = None


class GetFaculties(BaseModel):
    count: int = None
    items: typing.List[objects.database.Faculty] = None


class GetFacultiesModel(BaseModel):
    response: GetFaculties = None


GetMetroStationsById = typing.List[objects.database.Station]


class GetMetroStationsByIdModel(BaseModel):
    response: GetMetroStationsById = None


class GetMetroStations(BaseModel):
    count: int = None
    items: typing.List[objects.database.Station] = None


class GetMetroStationsModel(BaseModel):
    response: GetMetroStations = None


class GetRegions(BaseModel):
    count: int = None
    items: typing.List[objects.database.Region] = None


class GetRegionsModel(BaseModel):
    response: GetRegions = None


GetSchoolClasses = typing.List[typing.List]


class GetSchoolClassesModel(BaseModel):
    response: GetSchoolClasses = None


class GetSchools(BaseModel):
    count: int = None
    items: typing.List[objects.database.School] = None


class GetSchoolsModel(BaseModel):
    response: GetSchools = None
