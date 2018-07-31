from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import distinct
from sqlalchemy.orm import load_only, aliased
from sqlalchemy.sql import text
from esg.models.geography_model import GeographyModel
from esg.models.sector_model import SectorModel
from esg.models.company_model import CompanyModel
from esg.models.security_model import SecurityModel
from esg.models.portfolio_security_model import PortfolioSecurityModel
from esg.models.data_provider_model import DataProviderModel
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.login_model import LoginModel
from esg.models.organization_model import OrganizationModel
from esg.models.portfolio_model import PortfolioModel
from esg.models.session_model import SessionModel
from esg.models.tag_type_model import TagTypeModel
from esg.models.fixed_tag_model import FixedTagModel
from esg.resources.auth_resource import get_session_info
from esg.request_errors import BadRequest
from ext import db


# The classes below define constants for different tag types. They would have been defined as 
# enums, but enums can't be automatically JSON serialized.

class TagType:
    PORTFOLIO = 1
    ESG_METRICS = 2
    PORTFOLIO_METRICS = 3
    REGION = 4
    SECTOR = 5
    TIME = 6
    REPORTING_SCOPE = 7
    WEIGHT_METHOD = 8
    CONTROL = 9
    DATE = -1


class TimeTagType:
    # DATE = 0 #changes by leo
    YEARLY = 1
    QUARTERLY = 2
    MONTHLY = 3
    WEEKLY = 4
    DAILY = 5


class ScopeTagType:
    ALL_SECURITIES = 1
    ALL_REGIONS = 2
    ALL_COUNTRIES = 3
    ALL_SECTORS = 4
    ALL_INDUSTRIES = 5
    ALL_CONTRIBUTORS = 6
    ESG_DETAILS = 20
    UNGC_DETAILS = 21


class WeightTagType:
    VALUE = 1


class ControlTagType:
    ANALYSIS = 1
    GLOBAL_MAP = 2
    MARGINAL_TOP_20 = 100
    MARGINAL_BOTTOM_20 = 101


class PortfolioResultTagType:
    RETURN_CUMULATIVE = 10
    RETURN_DAILY = 11
    MARKET_VALUE = 12
    NUMBER_OF_SECURITIES = 13


class TagTypeSingleModel(Resource):
    def get(self, id):
        model = TagTypeModel.query.filter_by(id=id).first()
        return jsonify({'result': model.serialize()})


class TagsByTags(Resource):
    """Class used to query available tags given a list of tags currently selected by the user.
    """

    def post(self):
        """Returns tags available to the user based on currently input tags

        This method accepts a JSON list of currently selected tags. All tags passed in should 
        include a tag_type_id property to identify what category of tag it is. Tags such as region 
        and geography should include the level property.
        If no tags are provided (meaning the user has selected no tags yet) only portfolio tags will 
        be returned.

        Returns:
            A dicts containing Portfolio, PortfolioMetrics, ESGMetrics and Properties dicts, each
            with child dicts by type containing allowed tags.
        """
        result = {}

        self._organization_id, self._is_master_org, _ = get_session_info(request)

        json = request.get_json()
        if json is None:
            raise BadRequest('JSON POST was expected')

        self._portfolio_list = self._get_tags_by_type(json, TagType.PORTFOLIO)
        self._geography_list = self._get_tags_by_type(json, TagType.REGION)
        self._sector_list = self._get_tags_by_type(json, TagType.SECTOR)
        self._esg_factor_list = self._get_tags_by_type(json, TagType.ESG_METRICS)
        self._time_list = self._get_tags_by_type(json, TagType.TIME)
        self._scope_list = self._get_tags_by_type(json, TagType.REPORTING_SCOPE)
        self._weight_list = self._get_tags_by_type(json, TagType.WEIGHT_METHOD)
        self._result_list = self._get_tags_by_type(json, TagType.PORTFOLIO_METRICS)
        self._control_list = self._get_tags_by_type(json, TagType.CONTROL)

        self._contains_all_portfolios = self._check_list_contains(self._portfolio_list, 0)
        self._contains_daily_result_tag = self._check_list_contains(self._result_list, PortfolioResultTagType.RETURN_DAILY)
        self._contains_all_securities_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_SECURITIES)
        self._contains_all_regions_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_REGIONS)
        self._contains_all_sectors_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_SECTORS)
        self._contains_all_countries_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_COUNTRIES)
        self._contains_all_industries_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_INDUSTRIES)
        self._contains_all_contributors_tag = self._check_list_contains(self._scope_list, ScopeTagType.ALL_CONTRIBUTORS)
        self._contains_details_tag = self._check_list_contains(self._scope_list, ScopeTagType.ESG_DETAILS) or \
            self._check_list_contains(self._scope_list, ScopeTagType.UNGC_DETAILS)
        self._contains_analysis_tag = self._check_list_contains(self._control_list, ControlTagType.ANALYSIS)
        self._contains_global_map_tag = self._check_list_contains(self._control_list, ControlTagType.GLOBAL_MAP)
        self._contains_marginal_contributon_tag = self._check_list_contains(self._control_list, ControlTagType.MARGINAL_BOTTOM_20) or \
            self._check_list_contains(self._control_list, ControlTagType.MARGINAL_TOP_20)
        self._contains_control_tag = self._contains_analysis_tag or self._contains_global_map_tag or self._contains_marginal_contributon_tag

        self._time_scope = self._get_time_scope()

        portfolio_tags = self._get_portfolio_tags()
        result['Portfolio'] = TagsByTags._wrap_tags_dict(TagType.PORTFOLIO, 'Portfolio', portfolio_tags)

        if len(json) > 0:
            portfolio_metrics_tags = self._get_results_metrics_tags()
            esg_metrics_tags = self._get_esg_metrics_tags()

            geography_tags, sector_tags = self._get_geography_and_sector_tags()
            time_tags = self._get_time_tags()
            scope_tags = self._get_scope_tags()
            weight_tags = self._get_weight_method_tags()
            control_tags = self._get_control_tags()

            # Move 'ESG details' and 'UNGC details' to ESG metrics tags
            esg_scope_tags = [t for t in scope_tags if t['id'] == ScopeTagType.ESG_DETAILS or t['id'] == ScopeTagType.UNGC_DETAILS]
            for t in esg_scope_tags:
                esg_metrics_tags.insert(0, t)
                scope_tags.remove(t)

            properties_tags = [
                TagsByTags._wrap_tags_dict(TagType.REGION, 'Region', geography_tags),
                TagsByTags._wrap_tags_dict(TagType.SECTOR, 'Sector', sector_tags),
                TagsByTags._wrap_tags_dict(TagType.TIME, 'Time', time_tags),
                TagsByTags._wrap_tags_dict(TagType.REPORTING_SCOPE, 'Reporting Scope', scope_tags),
                TagsByTags._wrap_tags_dict(TagType.WEIGHT_METHOD, 'Weighting Method', weight_tags),
                TagsByTags._wrap_tags_dict(TagType.CONTROL, 'Other', control_tags)
            ]

            result['PortfolioMetrics'] = TagsByTags._wrap_tags_dict(TagType.PORTFOLIO_METRICS, 'Portfolio Metrics', portfolio_metrics_tags)
            result['ESGMetrics'] = TagsByTags._wrap_tags_dict(TagType.ESG_METRICS, 'ESG Metrics', esg_metrics_tags)
            result['Properties'] = properties_tags

        return jsonify(result)

    @staticmethod
    def _check_list_contains(list, tag_id):
        """Checks whether the given list contains the given tag id.
        """
        return any(t['id'] == tag_id for t in list)

    @staticmethod
    def _wrap_tags_dict(tag_type_id, description, tags):
        """Wraps the given tag list in a dict containing tag type and description properties.

        Args:
            tag_type_id: The tag type of the tags in the tags parameter.
            description: Description of the tag type for display to the user.
            tags: List of tags to wrap.

        Returns:
            A dict containing tags that the user may select.
        """
        return {
            'tag_type_id': tag_type_id,
            'description': description,
            'tags': tags
            }

    def _get_time_scope(self):
        """Returns a TimeTagType value to indicate a particular period has been selected, or 0 if not yet selected.

        Returns:
             A TimeTagType value or 0.
        """
        if len(self._time_list) > 0:
            return self._time_list[0]['id']
        elif self._contains_daily_result_tag:
            return TimeTagType.DAILY
        else:
            return 0

    def _get_portfolio_tags(self):
        """Returns available portfolio tags given a list of currently selected portfolio tags.

        Returns:
            A list of available portfolio tags the user may select.
        """
        portfolio_ids = [tag['id'] for tag in self._portfolio_list]
        portfolio_tags = []

        if not self._contains_all_portfolios and not self._contains_all_securities_tag and not self._contains_all_contributors_tag:
            # Global View tag only allows a single portfolio
            if len(portfolio_ids) == 0 or (not self._contains_global_map_tag and not self._contains_marginal_contributon_tag):
                if len(portfolio_ids) > 0:
                    query = PortfolioModel.query.filter(~PortfolioModel.id.in_(portfolio_ids))
                else:
                    query = PortfolioModel.query

                if not self._is_master_org:
                    query = query.filter((PortfolioModel.owner_id == self._organization_id) | (PortfolioModel.owner_id == None))

                query = query.order_by(PortfolioModel.name)

                portfolios = [portfolio for portfolio in query]

                #if len(portfolio_ids) == 0:
                #    portfolio_tags.append({'id': 0, 'tag_type_id': TagType.PORTFOLIO, 'name': '< All Portfolios >'})

                portfolio_tags.extend([{'id': portfolio.id, 'tag_type_id': TagType.PORTFOLIO, 'name': portfolio.name} for portfolio in portfolios])

        return portfolio_tags

    def _get_geography_and_sector_tags(self):
        """Returns available geography and sector tags given lists of currently selected tags.

        Returns:
            A list of available geography tags and a list of available sector tags the user may select.
        """
        if self._contains_control_tag or self._contains_all_securities_tag or \
            (self._contains_all_contributors_tag and len(self._geography_list) + len(self._sector_list) > 0) or \
            self._contains_marginal_contributon_tag:
            return [], []

        geography_ids = [tag['id'] for tag in self._geography_list]
        sector_ids = [tag['id'] for tag in self._sector_list]

        geography_tags = []
        sector_tags = []

        query = PortfolioSecurityModel.query.join(PortfolioSecurityModel.security).join(SecurityModel.company)

        if len(self._portfolio_list) > 0:
            portfolio_ids = [tag['id'] for tag in self._portfolio_list]

            if not self._contains_all_portfolios:
                query = query.join(PortfolioSecurityModel.portfolio).filter(PortfolioModel.id.in_(portfolio_ids))

        region_selected_tags, country_selected_tags, sector_selected_tags, industry_selected_tags = \
            TagsByTags._get_region_sector_lists(self._geography_list, self._sector_list)

        geography_query = query
        sector_query = query

        # If a region and sector is selected, can't select anything else
        if not (len(region_selected_tags) > 0 and len(sector_selected_tags) > 0):
            # Add sector level tags
            if len(industry_selected_tags) == 0 and not self._contains_all_sectors_tag and not self._contains_all_countries_tag:
                if len(sector_selected_tags) == 0 or not self._contains_all_regions_tag:
                    if len(region_selected_tags) == 1:
                        # Filter sectors by region
                        sector_query = query.join(CompanyModel.geography).filter(GeographyModel.parent_id.in_(geography_ids))

                    if len(region_selected_tags) == 1 or len(self._geography_list) == 0:
                        SectorParent = aliased(SectorModel, name='sector_parent')

                        sector_level_query = sector_query.join(CompanyModel.sector).join(SectorParent, SectorModel.parent_id == SectorParent.id)
                        sectors = [exposure.security.company.sector.parent for exposure in
                                    sector_level_query.distinct(SectorModel.parent_id).all()]
                        sectors.sort(key=lambda s: s.name)

                        sector_tags = [{
                            'id': sector.id,
                            'tag_type_id': TagType.SECTOR,
                            'level': sector.level,
                            'name': sector.name}
                            for sector in sectors if sector.id not in sector_ids]

            # Add region level tags
            if len(country_selected_tags) == 0 and not self._contains_all_regions_tag and not self._contains_all_industries_tag:
                if len(region_selected_tags) == 0 or not self._contains_all_sectors_tag:
                    if len(sector_selected_tags) == 1:
                        # Filter regions by sector
                        geography_query = query.join(CompanyModel.sector).filter(SectorModel.parent_id.in_(sector_ids))

                    if len(sector_selected_tags) == 1 or len(self._sector_list) == 0:
                        GeographyParent = aliased(GeographyModel, name='geography_parent')

                        region_query = geography_query.join(CompanyModel.geography).join(GeographyParent, GeographyModel.parent_id == GeographyParent.id)
                        regions = [exposure.security.company.geography.parent for exposure in
                                   region_query.distinct(GeographyModel.parent_id).all()]
                        regions.sort(key=lambda g: g.name)

                        geography_tags = [{
                            'id': geography.id,
                            'tag_type_id': TagType.REGION,
                            'level': geography.level,
                            'name': geography.name}
                            for geography in regions if geography.id not in geography_ids]

            if len(region_selected_tags) == 0 and len(sector_selected_tags) == 0 and \
                not self._contains_all_regions_tag and not self._contains_all_sectors_tag and \
                not self._contains_all_countries_tag and not self._contains_all_industries_tag:
                # Add country level tags
                if len(industry_selected_tags) == 0:
                    countries = [exposure.security.company.geography for exposure in
                                 geography_query.distinct(CompanyModel.geography_id).all()
                                 if exposure.security.company.geography is not None]
                    countries.sort(key=lambda c: c.name)

                    geography_tags.extend([{
                        'id': geography.id,
                        'tag_type_id': TagType.REGION,
                        'level': geography.level,
                        'name': geography.name}
                        for geography in countries if geography.id not in geography_ids])

                # Add industry level tags
                if len(country_selected_tags) == 0:
                    industries = [exposure.security.company.sector for exposure in
                                  sector_query.distinct(CompanyModel.sector_id).all()
                                  if exposure.security.company.sector is not None]
                    industries.sort(key=lambda i: i.name)

                    sector_tags.extend([{
                        'id': sector.id,
                        'tag_type_id': TagType.SECTOR,
                        'level': sector.level,
                        'name': sector.name}
                        for sector in industries if sector is not None and sector.id not in sector_ids])

        return geography_tags, sector_tags

    def _get_esg_metrics_tags(self):
        """Returns available ESG metrics tags given currently selected ESG tags.

        Returns:
            A list of available ESG metrics tags the user may select.
        """
        tags = []

        query = EsgFactorModel.query

        # User can select analysis/global_view tag + 1 ESG factor
        if not self._contains_details_tag and (not self._contains_control_tag or len(self._esg_factor_list) == 0):
            esg_factor_ids = [tag['id'] for tag in self._esg_factor_list]

            # If an ESG Factor has already been selected, limit the choices to factors with the same data provider id.

            if len(esg_factor_ids) > 0:
                if self._contains_all_securities_tag or self._contains_all_contributors_tag:
                    esg_factors = []
                else:
                    factor_id = esg_factor_ids[0]

                    SelectedFactor = aliased(EsgFactorModel, name='selected_factor')

                    # Select only the ESG Factors that match the provider of the selected factor. Exclude any selected factors.
                    esg_factors = query.join(SelectedFactor, EsgFactorModel.data_provider_id == SelectedFactor.data_provider_id) \
                        .filter(SelectedFactor.id == factor_id, ~EsgFactorModel.id.in_(esg_factor_ids)) \
                        .order_by(EsgFactorModel.name)
            else:
                esg_factors = query.order_by(EsgFactorModel.name).all()

            tags = [{ 'id': factor.id, 'tag_type_id': TagType.ESG_METRICS, 'provider_name': factor.data_provider.name, 'name': factor.name } for factor in esg_factors]

        return tags

    def _get_results_metrics_tags(self):
        """Returns available results tags given currently selected results tags.

        Returns:
            A list of available results tags the user may select.
        """
        results_tags = []

        fixed_tags = FixedTagModel.query.order_by(FixedTagModel.description).all()

        if not self._contains_all_securities_tag and not self._contains_all_contributors_tag and not self._contains_global_map_tag and not self._contains_marginal_contributon_tag:
            for tag in fixed_tags:
                if tag.tag_type_id == TagType.PORTFOLIO_METRICS:
                    if len([t for t in self._result_list if t['id'] == tag.id]) == 0:
                        if self._time_scope == 0 or self._time_scope == TimeTagType.DAILY or tag.id != PortfolioResultTagType.RETURN_DAILY:
                            results_tags.append({'id': tag.id, 'tag_type_id': TagType.PORTFOLIO_METRICS, 'name': tag.description})

        return results_tags

    def _get_scope_tags(self):
        available_tags = []

        # 1) All counties, All regions, All sectors, and All industries cannot appear in the search bar at the same time. User can either choose one of them or not choose
        if len(self._scope_list) == 0 and not self._contains_control_tag:
            if len(self._portfolio_list) <= 1 and len(self._esg_factor_list) <= 1 and len(self._time_list) == 0 and len(self._result_list) == 0:
                if (len(self._geography_list) + len(self._sector_list)) <= 1:
                    available_tags.append({'id': ScopeTagType.ALL_CONTRIBUTORS, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Contributors'})

                if len(self._geography_list) == 0 and len(self._sector_list) == 0:
                    available_tags.append({'id': ScopeTagType.ALL_SECURITIES, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Securities'})

            region_tags, country_tags, sector_tags, industry_tags = \
                TagsByTags._get_region_sector_lists(self._geography_list, self._sector_list)

            if len(country_tags) == 0 and len(industry_tags) == 0:
                if len(region_tags) == 0 and len(sector_tags) < 2:
                    available_tags.append({'id': ScopeTagType.ALL_REGIONS, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Regions'})
                if len(country_tags) == 0 and len(self._sector_list) == 0:
                    available_tags.append({'id': ScopeTagType.ALL_COUNTRIES, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Countries'})
                if len(sector_tags) == 0 and len(region_tags) < 2:
                    available_tags.append({'id': ScopeTagType.ALL_SECTORS, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Sectors'})
                if len(industry_tags) == 0 and len(self._geography_list) == 0:
                    available_tags.append({'id': ScopeTagType.ALL_INDUSTRIES, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'All Industries'})

            if len(self._esg_factor_list) == 0:
                available_tags.extend([
                    {'id': ScopeTagType.UNGC_DETAILS, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'UNGC Details'},
                    {'id': ScopeTagType.ESG_DETAILS, 'tag_type_id': TagType.REPORTING_SCOPE, 'name': 'ESG Details'}
                ])

        available_tags.sort(key=lambda t: (t['tag_type_id'], t['name']))

        return available_tags

    @staticmethod
    def _get_region_sector_lists(geography_list, sector_list):
        region_tags = [t for t in geography_list if t['level'] == 1]
        country_tags = [t for t in geography_list if t['level'] == 2]
        sector_tags = [t for t in sector_list if t['level'] == 1]
        industry_tags = [t for t in sector_list if t['level'] == 2]

        return region_tags, country_tags, sector_tags, industry_tags

    def _get_time_tags(self):
        available_tags = []

        if len(self._time_list) == 0:
            if not self._contains_all_securities_tag and not self._contains_all_contributors_tag and not self._contains_global_map_tag and not self._contains_marginal_contributon_tag:
                if self._time_scope > 0:
                    available_tags = [
                        {'id': self._time_scope, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(self._time_scope)},
                    ]
                else:
                    available_tags = [
                        # changes by leo
                        # {'id': TimeTagType.DATE, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.DATE)},
                        {'id': TimeTagType.DAILY, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.DAILY)},
                        {'id': TimeTagType.WEEKLY, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.WEEKLY)},
                        {'id': TimeTagType.MONTHLY, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.MONTHLY)},
                        {'id': TimeTagType.QUARTERLY, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.QUARTERLY)},
                        {'id': TimeTagType.YEARLY, 'tag_type_id': TagType.TIME, 'name': TagsByTags._getTimeTagDesc(TimeTagType.YEARLY)}
                    ]

        return available_tags

    @staticmethod
    def _getTimeTagDesc(time_scope):
        period = ''

        # if time_scope == TimeTagType.DATE:
        #     period = 'Date'
        if time_scope == TimeTagType.YEARLY:
            period = 'Yearly'
        elif time_scope == TimeTagType.QUARTERLY:
            period = 'Quarterly'
        elif time_scope == TimeTagType.MONTHLY:
            period = 'Monthly'
        elif time_scope == TimeTagType.WEEKLY:
            period = 'Weekly'
        elif time_scope == TimeTagType.DAILY:
            period = 'Daily'

        return 'Time' if period == '' else 'Time (' + period + ')'

    def _get_weight_method_tags(self):
        available_tags = []

        if len(self._weight_list) == 0 and not self._contains_all_securities_tag and not self._contains_all_contributors_tag and not self._contains_control_tag:
            available_tags = [
                {'id': WeightTagType.VALUE, 'tag_type_id': TagType.WEIGHT_METHOD, 'name': 'Weight by value'}
            ]

        return available_tags

    def _get_control_tags(self):
        available_tags = []

        if len(self._control_list) == 0 and len(self._geography_list) == 0 and len(self._sector_list) == 0 and \
            len(self._esg_factor_list) < 2 and len(self._scope_list) == 0 and len(self._weight_list) == 0:
            available_tags = [
                {'id': ControlTagType.ANALYSIS, 'tag_type_id': TagType.CONTROL, 'name': 'Analysis'}
            ]

            # Global View tag only allows a single portfolio
            if len(self._portfolio_list) <= 1 and not self._contains_all_portfolios and len(self._time_list) == 0 and len(self._result_list) == 0:
                available_tags.append({
                    'id': ControlTagType.GLOBAL_MAP,
                    'tag_type_id': TagType.CONTROL,
                    'name': 'Global Map'
                })
                available_tags.append({
                    'id': ControlTagType.MARGINAL_TOP_20,
                    'tag_type_id': TagType.CONTROL,
                    'name': 'Top 20 marginal contributors'
                })
                available_tags.append({
                    'id': ControlTagType.MARGINAL_BOTTOM_20,
                    'tag_type_id': TagType.CONTROL,
                    'name': 'Bottom 20 marginal contributors'
                })

        return available_tags

    @staticmethod
    def _get_tags_by_type(json, tag_type):
        """Given a list of tags (represented as dicts), returns all tags matching the given tag type.

        Args:
            json: JSON object.
            tag_type: The type of tags to select.

        Returns:
            A list of matching tags.
        """
        return [tag for tag in json if tag['tag_type_id'] == tag_type]
