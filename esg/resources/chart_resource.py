from flask import request, jsonify
from flask_restful import Resource

from ext import db

NUM_TAG_CATEGORIES = 6

PORTFOLIO_TAG_TYPE = 1
COMPANY_TAG_TYPE = 2
ESG_PROVIDER_TAG_TYPE = 3
ESG_METRICS_TAG_TYPE = 4
PORTFOLIO_RESULT_TAG_TYPE = 5
EXPOSURE_RESULT_TAG_TYPE = 6

PORTFOLIO_TYPE_FLAG = 1
COMPANY_TYPE_FLAG = 2
ESG_PROVIDER_TYPE_FLAG = 4
ESG_METRICS_TYPE_FLAG = 8
PORTFOLIO_RESULT_TYPE_FLAG = 16
EXPOSURE_RESULT_TYPE_FLAG = 32

class ChartFromTags(Resource):
    def post(self):
        query = request.get_json()

        # Storing this as a single element list as a quick and dirty way to allow _get_tags_by_type to modify it...
        tag_types_submitted = [0]

        portfolio_id_list = self._get_tags_by_type(query, PORTFOLIO_TAG_TYPE, tag_types_submitted)
        company_id_list = self._get_tags_by_type(query, COMPANY_TAG_TYPE, tag_types_submitted)
        esg_provider_id_list = self._get_tags_by_type(query, ESG_PROVIDER_TAG_TYPE, tag_types_submitted)
        esg_metrics_id_list = self._get_tags_by_type(query, ESG_METRICS_TAG_TYPE, tag_types_submitted)
        portfolio_result_id_list = self._get_tags_by_type(query, PORTFOLIO_RESULT_TAG_TYPE, tag_types_submitted)
        exposure_result_id_list = self._get_tags_by_type(query, EXPOSURE_RESULT_TAG_TYPE, tag_types_submitted)

        tag_types = tag_types_submitted[0]

        if tag_types == PORTFOLIO_TYPE_FLAG + PORTFOLIO_RESULT_TYPE_FLAG:
            result = self._get_portfolio_results_chart(portfolio_id_list, portfolio_result_id_list)
        elif tag_types == PORTFOLIO_TYPE_FLAG + COMPANY_TAG_TYPE:
            result = self._get_company_chart(portfolio_id_list, company_id_list)
        else:
            result = { 'success': False }

        return jsonify(result)

    def _get_portfolio_results_chart(self, portfolio_id_list, portfolio_result_id_list):
        field_sql = "select id, field_name, description from meta.fixed_tag where tag_type_id = " + str(
            PORTFOLIO_RESULT_TAG_TYPE) + " and id in(" + ", ".join(map(str, portfolio_result_id_list)) + ") order by id"
        field_results = db.engine.execute(field_sql)

        db_fields = [{'id': field['id'], 'description': field['description'], 'field_name': field['field_name']} for field in field_results]

        field_name_list = [field['field_name'] for field in db_fields]
        field_desc_list = [field['description'] for field in db_fields]
        field_names = ", ".join(field_name_list)

        filters = []

        portfolio_ids = self._get_portfolio_ids_filter(portfolio_id_list)
        if len(portfolio_ids) > 0:
            filters.append("p.id in(" + portfolio_ids + ")")

        where = self._get_where(filters)

        sql = "select p.name, p.id, r.date_key, " + field_names + \
              " from portfolio_result r join portfolio p on r.portfolio_id = p.id " + \
              where + " order by p.id, r.date_key"
        data_results = [row for row in db.engine.execute(sql)]

        current_id = 0
        current_info = None
        current_series = None
        series_infos = []

        for data_result in data_results:
            portfolio_id = data_result['id']

            if portfolio_id != current_id:
                if current_info is not None:
                    series_infos.append(current_info)

                current_id = portfolio_id
                current_series = []
                current_info = {'name': data_result['name'], 'id': portfolio_id, 'data': current_series}

            data_point = [data_result['date_key']]
            for field_name in field_name_list:
                data_point.append(data_result[field_name])

            current_series.append(data_point)

        if current_series is not None:
            series_infos.append(current_info)

        return {
            'success': True,
            'chart_type': 'bar',
            'measures': db_fields,
            'x_axis': ['Year'],
            'y_axis': field_desc_list,
            'series': series_infos
        }

    def _get_company_chart(self, portfolio_id_list, company_id_list):
        filters = []

        company_ids = ", ".join(["'" + str(id) + "'" for id in company_id_list])
        filters.append("c.id in(" + company_ids + ")")

        portfolio_ids = self._get_portfolio_ids_filter(portfolio_id_list)
        if len(portfolio_ids) > 0:
            filters.append("p.id in(" + portfolio_ids + ")")

        where = self._get_where(filters)

        sql = """
select distinct e.portfolio_id, p.name as portfolio_name, e.date_key, c.id as company_id, c.name as company_name,
  sum(e.base_currency_value) over (partition by e.portfolio_id, e.date_key, c.id) / r.total_exposure_amount as weight
from
  portfolio_security_value e
  join security s on e.security_id = s.id
  join company c on s.company_id = c.id
  join portfolio p on e.portfolio_id = p.id
  join (
    select pv.portfolio_id, pv.date_key, sum(pv.base_currency_value) as total_exposure_amount
    from portfolio_security_value pv
    group by pv.portfolio_id, pv.date_key
  ) r on e.portfolio_id = r.portfolio_id and e.date_key = r.date_key
  """ + where + " order by e.portfolio_id, e.date_key, c.id"

        data_results = [row for row in db.engine.execute(sql)]

        current_id = 0
        current_year = 0
        current_info = None
        current_series = None
        series_infos = []

        #companies = []

        for data_result in data_results:
            portfolio_id = data_result['portfolio_id']

            if portfolio_id != current_id:
                if current_info is not None:
                    series_infos.append(current_info)

                current_id = portfolio_id
                current_series = []
                current_info = { 'name': data_result['portfolio_name'], 'id': portfolio_id, 'data': current_series }

            date = data_result['date']

            #company_id = data_result['company_id']
            #if not any(company_id in d['id'] for d in companies):
            #    companies.append({ 'id': data_result['company_id'], 'description': data_result['company_name'], 'field_name': 'company_name' })

            current_series.append({ 'date': date, 'company_id': data_result['company_id'], 'company_name': data_result['company_name'], 'weight': data_result['weight'] })

        if current_series is not None:
            series_infos.append(current_info)

        return {
            'success': True,
            'chart_type': 'bar',
            'fields': [ { 'description': 'Weight', 'field_name': 'weight' } ],
            'x_axis': ['Date'],
            'y_axis': ['Weight'],
            'series': series_infos
        }

    def _get_where(self, filters):
        sql = " and ".join(filters)

        if len(sql) > 0:
            sql = "where " + sql

        return sql

    def _get_portfolio_ids_filter(self, portfolio_id_list):
        if 0 in portfolio_id_list:
            return ""
        else:
            return ", ".join(map(str, portfolio_id_list))

    def _get_tags_by_type(self, query, tag_type, tag_types_submitted):
        tags = []

        for tag in query:
            if tag['tag_type_id'] == tag_type:
                tags.append(tag['id'])

        if len(tags) > 0:
            if tag_type == PORTFOLIO_TAG_TYPE:
                tag_types_submitted[0] += PORTFOLIO_TYPE_FLAG
            elif tag_type == COMPANY_TAG_TYPE:
                tag_types_submitted[0] += COMPANY_TYPE_FLAG
            elif tag_type == ESG_PROVIDER_TAG_TYPE:
                tag_types_submitted[0] += ESG_PROVIDER_TYPE_FLAG
            elif tag_type == ESG_METRICS_TAG_TYPE:
                tag_types_submitted[0] += ESG_METRICS_TYPE_FLAG
            elif tag_type == PORTFOLIO_RESULT_TAG_TYPE:
                tag_types_submitted[0] += PORTFOLIO_RESULT_TYPE_FLAG
            elif tag_type == EXPOSURE_RESULT_TAG_TYPE:
                tag_types_submitted[0] += EXPOSURE_RESULT_TYPE_FLAG
            else:
                raise Exception("Unknown tag type: " + str(tag_type))

        return tags
