# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class DatabaseGetChairs(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, faculty_id: int, offset: int = None, count: int = None
    ) -> responses.database.GetChairs:
        """ database.getChairs
        From Vk Docs: Returns list of chairs on a specified faculty.
        Access from user, service token(s)
        :param faculty_id: id of the faculty to get chairs from
        :param offset: offset required to get a certain subset of chairs
        :param count: amount of chairs to get
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getChairs",
            params,
            response_model=responses.database.GetChairsModel,
        )


class DatabaseGetCities(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        country_id: int,
        region_id: int = None,
        q: str = None,
        need_all: bool = None,
        offset: int = None,
        count: int = None,
    ) -> responses.database.GetCities:
        """ database.getCities
        From Vk Docs: Returns a list of cities.
        Access from user token(s)
        :param country_id: Country ID.
        :param region_id: Region ID.
        :param q: Search query.
        :param need_all: '1' — to return all cities in the country, '0' — to return major cities in the country (default),
        :param offset: Offset needed to return a specific subset of cities.
        :param count: Number of cities to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getCities",
            params,
            response_model=responses.database.GetCitiesModel,
        )


class DatabaseGetCitiesById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, city_ids: typing.List = None
    ) -> responses.database.GetCitiesById:
        """ database.getCitiesById
        From Vk Docs: Returns information about cities by their IDs.
        Access from user, service token(s)
        :param city_ids: City IDs.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getCitiesById",
            params,
            response_model=responses.database.GetCitiesByIdModel,
        )


class DatabaseGetCountries(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        need_all: bool = None,
        code: str = None,
        offset: int = None,
        count: int = None,
    ) -> responses.database.GetCountries:
        """ database.getCountries
        From Vk Docs: Returns a list of countries.
        Access from user token(s)
        :param need_all: '1' — to return a full list of all countries, '0' — to return a list of countries near the current user's country (default).
        :param code: Country codes in [vk.com/dev/country_codes|ISO 3166-1 alpha-2] standard.
        :param offset: Offset needed to return a specific subset of countries.
        :param count: Number of countries to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getCountries",
            params,
            response_model=responses.database.GetCountriesModel,
        )


class DatabaseGetCountriesById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, country_ids: typing.List = None
    ) -> responses.database.GetCountriesById:
        """ database.getCountriesById
        From Vk Docs: Returns information about countries by their IDs.
        Access from user, service token(s)
        :param country_ids: Country IDs.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getCountriesById",
            params,
            response_model=responses.database.GetCountriesByIdModel,
        )


class DatabaseGetFaculties(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, university_id: int, offset: int = None, count: int = None
    ) -> responses.database.GetFaculties:
        """ database.getFaculties
        From Vk Docs: Returns a list of faculties (i.e., university departments).
        Access from user, service token(s)
        :param university_id: University ID.
        :param offset: Offset needed to return a specific subset of faculties.
        :param count: Number of faculties to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getFaculties",
            params,
            response_model=responses.database.GetFacultiesModel,
        )


class DatabaseGetMetroStations(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, city_id: int, offset: int = None, count: int = None, extended: bool = None
    ) -> responses.database.GetMetroStations:
        """ database.getMetroStations
        From Vk Docs: Get metro stations by city
        Access from user, service token(s)
        :param city_id: 
        :param offset: 
        :param count: 
        :param extended: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getMetroStations",
            params,
            response_model=responses.database.GetMetroStationsModel,
        )


class DatabaseGetMetroStationsById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, station_ids: typing.List = None
    ) -> responses.database.GetMetroStationsById:
        """ database.getMetroStationsById
        From Vk Docs: Get metro station by his id
        Access from user, service token(s)
        :param station_ids: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getMetroStationsById",
            params,
            response_model=responses.database.GetMetroStationsByIdModel,
        )


class DatabaseGetRegions(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, country_id: int, q: str = None, offset: int = None, count: int = None
    ) -> responses.database.GetRegions:
        """ database.getRegions
        From Vk Docs: Returns a list of regions.
        Access from user, service token(s)
        :param country_id: Country ID, received in [vk.com/dev/database.getCountries|database.getCountries] method.
        :param q: Search query.
        :param offset: Offset needed to return specific subset of regions.
        :param count: Number of regions to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getRegions",
            params,
            response_model=responses.database.GetRegionsModel,
        )


class DatabaseGetSchoolClasses(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, country_id: int = None
    ) -> responses.database.GetSchoolClasses:
        """ database.getSchoolClasses
        From Vk Docs: Returns a list of school classes specified for the country.
        Access from user, service token(s)
        :param country_id: Country ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getSchoolClasses",
            params,
            response_model=responses.database.GetSchoolClassesModel,
        )


class DatabaseGetSchools(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, city_id: int, q: str = None, offset: int = None, count: int = None
    ) -> responses.database.GetSchools:
        """ database.getSchools
        From Vk Docs: Returns a list of schools.
        Access from user, service token(s)
        :param q: Search query.
        :param city_id: City ID.
        :param offset: Offset needed to return a specific subset of schools.
        :param count: Number of schools to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getSchools",
            params,
            response_model=responses.database.GetSchoolsModel,
        )


class DatabaseGetUniversities(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        q: str = None,
        country_id: int = None,
        city_id: int = None,
        offset: int = None,
        count: int = None,
    ) -> responses.database.GetUniversities:
        """ database.getUniversities
        From Vk Docs: Returns a list of higher education institutions.
        Access from user, service token(s)
        :param q: Search query.
        :param country_id: Country ID.
        :param city_id: City ID.
        :param offset: Offset needed to return a specific subset of universities.
        :param count: Number of universities to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "database.getUniversities",
            params,
            response_model=responses.database.GetUniversitiesModel,
        )


class Database:
    def __init__(self, request):
        self.get_chairs = DatabaseGetChairs(request)
        self.get_cities = DatabaseGetCities(request)
        self.get_cities_by_id = DatabaseGetCitiesById(request)
        self.get_countries = DatabaseGetCountries(request)
        self.get_countries_by_id = DatabaseGetCountriesById(request)
        self.get_faculties = DatabaseGetFaculties(request)
        self.get_metro_stations = DatabaseGetMetroStations(request)
        self.get_metro_stations_by_id = DatabaseGetMetroStationsById(request)
        self.get_regions = DatabaseGetRegions(request)
        self.get_school_classes = DatabaseGetSchoolClasses(request)
        self.get_schools = DatabaseGetSchools(request)
        self.get_universities = DatabaseGetUniversities(request)
