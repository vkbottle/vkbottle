import typing
from ..base import BaseModel
from vkbottle.types import objects

UpdateClients = typing.Dict


class UpdateClientsModel(BaseModel):
    response: UpdateClients = None


AddOfficeUsers = typing.Dict


class AddOfficeUsersModel(BaseModel):
    response: AddOfficeUsers = None


CheckLink = objects.ads.LinkStatus


class CheckLinkModel(BaseModel):
    response: CheckLink = None


CreateAds = typing.List[int]


class CreateAdsModel(BaseModel):
    response: CreateAds = None


CreateCampaigns = typing.List[int]


class CreateCampaignsModel(BaseModel):
    response: CreateCampaigns = None


CreateClients = typing.List[int]


class CreateClientsModel(BaseModel):
    response: CreateClients = None


class CreateTargetGroup(BaseModel):
    id: int = None
    pixel: str = None


class CreateTargetGroupModel(BaseModel):
    response: CreateTargetGroup = None


DeleteAds = typing.List[int]


class DeleteAdsModel(BaseModel):
    response: DeleteAds = None


DeleteCampaigns = typing.Dict


class DeleteCampaignsModel(BaseModel):
    response: DeleteCampaigns = None


DeleteClients = typing.Dict


class DeleteClientsModel(BaseModel):
    response: DeleteClients = None


GetAccounts = typing.List[objects.ads.Account]


class GetAccountsModel(BaseModel):
    response: GetAccounts = None


GetAdsLayout = typing.List[objects.ads.AdLayout]


class GetAdsLayoutModel(BaseModel):
    response: GetAdsLayout = None


GetAdsTargeting = typing.List[objects.ads.TargSettings]


class GetAdsTargetingModel(BaseModel):
    response: GetAdsTargeting = None


GetAds = typing.List[objects.ads.Ad]


class GetAdsModel(BaseModel):
    response: GetAds = None


GetBudget = typing.Dict


class GetBudgetModel(BaseModel):
    response: GetBudget = None


GetCampaigns = typing.List[objects.ads.Campaign]


class GetCampaignsModel(BaseModel):
    response: GetCampaigns = None


class GetCategories(BaseModel):
    v1: typing.List[objects.ads.Category] = None
    v2: typing.List[objects.ads.Category] = None


class GetCategoriesModel(BaseModel):
    response: GetCategories = None


GetClients = typing.List[objects.ads.Client]


class GetClientsModel(BaseModel):
    response: GetClients = None


GetDemographics = typing.List[objects.ads.DemoStats]


class GetDemographicsModel(BaseModel):
    response: GetDemographics = None


GetFloodStats = objects.ads.FloodStats


class GetFloodStatsModel(BaseModel):
    response: GetFloodStats = None


GetOfficeUsers = typing.List[objects.ads.Users]


class GetOfficeUsersModel(BaseModel):
    response: GetOfficeUsers = None


GetPostsReach = typing.List[objects.ads.PromotedPostReach]


class GetPostsReachModel(BaseModel):
    response: GetPostsReach = None


GetRejectionReason = objects.ads.RejectReason


class GetRejectionReasonModel(BaseModel):
    response: GetRejectionReason = None


GetStatistics = typing.List[objects.ads.Stats]


class GetStatisticsModel(BaseModel):
    response: GetStatistics = None


GetSuggestions = typing.List[objects.ads.TargSuggestions]


class GetSuggestionsModel(BaseModel):
    response: GetSuggestions = None


GetTargetGroups = typing.List[objects.ads.TargetGroup]


class GetTargetGroupsModel(BaseModel):
    response: GetTargetGroups = None


GetTargetingStats = objects.ads.TargStats


class GetTargetingStatsModel(BaseModel):
    response: GetTargetingStats = None


GetUploadURL = typing.Dict


class GetUploadURLModel(BaseModel):
    response: GetUploadURL = None


GetVideoUploadURL = typing.Dict


class GetVideoUploadURLModel(BaseModel):
    response: GetVideoUploadURL = None


ImportTargetContacts = typing.Dict


class ImportTargetContactsModel(BaseModel):
    response: ImportTargetContacts = None


RemoveOfficeUsers = typing.Dict


class RemoveOfficeUsersModel(BaseModel):
    response: RemoveOfficeUsers = None


UpdateAds = typing.List[int]


class UpdateAdsModel(BaseModel):
    response: UpdateAds = None


UpdateCampaigns = typing.Dict


class UpdateCampaignsModel(BaseModel):
    response: UpdateCampaigns = None
