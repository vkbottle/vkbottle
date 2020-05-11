from . import base
import typing
from enum import Enum
from ..base import BaseModel


class AccessRole(Enum):
    admin = "admin"
    manager = "manager"
    reports = "reports"


class Accesses(BaseModel):
    client_id: str = None
    role: "AccessRole" = None


class Account(BaseModel):
    access_role: "AccessRole" = None
    account_id: int = None
    account_status: "base.BoolInt" = None
    account_type: "AccountType" = None


class AccountType(Enum):
    general = "general"
    agency = "agency"


class Ad(BaseModel):
    ad_format: int = None
    ad_platform: typing.Union[int, str] = None
    all_limit: int = None
    approved: int = None
    campaign_id: int = None
    category1_id: int = None
    category2_id: int = None
    cost_type: int = None
    cpc: int = None
    cpm: int = None
    cpa: int = None
    disclaimer_medical: "base.BoolInt" = None
    disclaimer_specialist: "base.BoolInt" = None
    disclaimer_supplements: "base.BoolInt" = None
    id: int = None
    impressions_limit: int = None
    impressions_limited: "base.BoolInt" = None
    name: str = None
    status: int = None
    video: "base.BoolInt" = None


class AdLayout(BaseModel):
    ad_format: int = None
    campaign_id: int = None
    cost_type: int = None
    description: str = None
    id: int = None
    image_src: str = None
    image_src_2x: str = None
    link_domain: str = None
    link_url: str = None
    preview_link: typing.Union[int, str] = None
    title: str = None
    video: "base.BoolInt" = None


class Campaign(BaseModel):
    all_limit: str = None
    day_limit: str = None
    id: int = None
    name: str = None
    start_time: int = None
    status: int = None
    stop_time: int = None
    type: "CampaignType" = None


class CampaignType(Enum):
    normal = "normal"
    vk_apps_managed = "vk_apps_managed"
    mobile_apps = "mobile_apps"
    promoted_posts = "promoted_posts"


class Category(BaseModel):
    id: int = None
    name: str = None
    subcategories: typing.List = None


class Client(BaseModel):
    all_limit: str = None
    day_limit: str = None
    id: int = None
    name: str = None


class Criteria(BaseModel):
    age_from: int = None
    age_to: int = None
    apps: str = None
    apps_not: str = None
    birthday: int = None
    cities: str = None
    cities_not: str = None
    country: int = None
    districts: str = None
    groups: str = None
    interest_categories: str = None
    interests: str = None
    paying: "base.BoolInt" = None
    positions: str = None
    religions: str = None
    retargeting_groups: str = None
    retargeting_groups_not: str = None
    school_from: int = None
    school_to: int = None
    schools: str = None
    sex: "CriteriaSex" = None
    stations: str = None
    statuses: str = None
    streets: str = None
    travellers: "base.PropertyExists" = None
    uni_from: int = None
    uni_to: int = None
    user_browsers: str = None
    user_devices: str = None
    user_os: str = None


class CriteriaSex(Enum):
    no = 0
    female = 1
    male = 2


class DemoStats(BaseModel):
    id: int = None
    stats: "DemostatsFormat" = None
    type: "ObjectType" = None


class DemostatsFormat(BaseModel):
    age: typing.List = None
    cities: typing.List = None
    day: str = None
    month: str = None
    overall: int = None
    sex: typing.List = None
    sex_age: typing.List = None


class FloodStats(BaseModel):
    left: int = None
    refresh: int = None


class LinkStatus(BaseModel):
    description: str = None
    redirect_url: str = None
    status: str = None


class ObjectType(Enum):
    ad = "ad"
    campaign = "campaign"
    client = "client"
    office = "office"


class Paragraphs(BaseModel):
    paragraph: str = None


class PromotedPostReach(BaseModel):
    hide: int = None
    id: int = None
    join_group: int = None
    links: int = None
    reach_subscribers: int = None
    reach_total: int = None
    report: int = None
    to_group: int = None
    unsubscribe: int = None
    video_views_100p: int = None
    video_views_25p: int = None
    video_views_3s: int = None
    video_views_50p: int = None
    video_views_75p: int = None
    video_views_start: int = None


class RejectReason(BaseModel):
    comment: str = None
    rules: typing.List = None


class Rules(BaseModel):
    paragraphs: typing.List = None
    title: str = None


class Stats(BaseModel):
    id: int = None
    stats: "StatsFormat" = None
    type: "ObjectType" = None


class StatsAge(BaseModel):
    clicks_rate: int = None
    impressions_rate: int = None
    value: str = None


class StatsCities(BaseModel):
    clicks_rate: float = None
    impressions_rate: float = None
    name: str = None
    value: int = None


class StatsFormat(BaseModel):
    clicks: int = None
    day: str = None
    impressions: int = None
    join_rate: int = None
    month: str = None
    overall: int = None
    reach: int = None
    spent: int = None
    video_clicks_site: int = None
    video_views: int = None
    video_views_full: int = None
    video_views_half: int = None


class StatsSex(BaseModel):
    clicks_rate: float = None
    impressions_rate: float = None
    value: "StatsSexValue" = None


class StatsSexAge(BaseModel):
    clicks_rate: float = None
    impressions_rate: float = None
    value: str = None


class StatsSexValue(Enum):
    f = "f"
    m = "m"


class TargSettings(Criteria):
    id: int = None
    campaign_id: int = None


class TargStats(BaseModel):
    audience_count: int = None
    recommended_cpc: float = None
    recommended_cpm: float = None


class TargSuggestions(BaseModel):
    id: int = None
    name: str = None


class TargSuggestionsCities(BaseModel):
    id: int = None
    name: str = None
    parent: str = None


class TargSuggestionsRegions(BaseModel):
    id: int = None
    name: str = None
    type: str = None


class TargSuggestionsSchools(BaseModel):
    desc: str = None
    id: int = None
    name: str = None
    parent: str = None
    type: "TargSuggestionsSchoolsType" = None


class TargSuggestionsSchoolsType(Enum):
    school = "school"
    university = "university"
    faculty = "faculty"
    chair = "chair"


class TargetGroup(BaseModel):
    audience_count: int = None
    domain: str = None
    id: int = None
    lifetime: int = None
    name: str = None
    pixel: str = None


class Users(BaseModel):
    accesses: typing.List = None
    user_id: int = None


Accesses.update_forward_refs()
Account.update_forward_refs()
Ad.update_forward_refs()
AdLayout.update_forward_refs()
Campaign.update_forward_refs()
Category.update_forward_refs()
Client.update_forward_refs()
Criteria.update_forward_refs()
DemoStats.update_forward_refs()
DemostatsFormat.update_forward_refs()
FloodStats.update_forward_refs()
LinkStatus.update_forward_refs()
Paragraphs.update_forward_refs()
PromotedPostReach.update_forward_refs()
RejectReason.update_forward_refs()
Rules.update_forward_refs()
Stats.update_forward_refs()
StatsAge.update_forward_refs()
StatsCities.update_forward_refs()
StatsFormat.update_forward_refs()
StatsSex.update_forward_refs()
StatsSexAge.update_forward_refs()
TargSettings.update_forward_refs()
TargStats.update_forward_refs()
TargSuggestions.update_forward_refs()
TargSuggestionsCities.update_forward_refs()
TargSuggestionsRegions.update_forward_refs()
TargSuggestionsSchools.update_forward_refs()
TargetGroup.update_forward_refs()
Users.update_forward_refs()
