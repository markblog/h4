import math


class TimeFrequency:
    def _is_last_transaction_day_of_a_week(self, *para):
        last_transaction_day_list = []
        week_number_set = set()
        date_list = self._all_date()
        if para:
            date_list = self._all_date(para)
        for date_tuple in date_list:
            year, week_number, _ = date_tuple[0].isocalendar()
            key = str(year) + '-' + str(week_number)
            if key not in week_number_set:
                week_number_set.add(key)
                last_transaction_day_list.append(date_tuple[0].strftime('%Y-%m-%d'))
        del week_number_set
        return last_transaction_day_list

    def _is_last_transaction_day_of_a_month(self, *para):
        last_transaction_day_list = []
        months_number_set = set()
        date_list = self._all_date()
        if para:
            date_list = self._all_date(para)
        for date_tuple in date_list:
            month_number = date_tuple[0].month
            year = date_tuple[0].year
            key = str(year) + '-' + str(month_number)
            if key not in months_number_set:
                months_number_set.add(key)
                last_transaction_day_list.append(date_tuple[0].strftime('%Y-%m-%d'))

        del months_number_set
        return last_transaction_day_list

    def _is_last_transaction_day_of_a_quarter(self, *para):
        last_transaction_day_list = []
        quarter_number_set = set()
        date_list = self._all_date()
        if para:
            date_list = self._all_date(para)
        for date_tuple in date_list:
            # count the date in which quarter
            quarter_number = math.ceil(date_tuple[0].month / 3.0)
            year = date_tuple[0].year
            key = str(year) + '-' + str(quarter_number)
            if key not in quarter_number_set:
                quarter_number_set.add(key)
                last_transaction_day_list.append(date_tuple[0].strftime('%Y-%m-%d'))

        del quarter_number_set
        return last_transaction_day_list

    def _is_last_transaction_day_of_a_year(self, *para):
        last_transaction_day_list = []
        year_number_set = set()
        date_list = self._all_date()
        if para:
            date_list = self._all_date(para)
        for date_tuple in date_list:
            year_number = date_tuple[0].year
            if year_number not in year_number_set:
                year_number_set.add(year_number)
                last_transaction_day_list.append(date_tuple[0].strftime('%Y-%m-%d'))

        del year_number_set
        return last_transaction_day_list

    def _all_date(self, *para):
        """
        get the date list of whole portfolio order by date descend
        """
        raise NotImplementedError
