import configuration_provider
from datetime import datetime, timedelta


class Person:
    def is_person_blacklisted(personal_id):
        return personal_id in configuration_provider.ConfigurationProvider.get_blacklist()

    def has_too_many_applications_in_last_24_hours(personal_id, loans):
        applications = 0
        for loan in loans:
            if loan['personal_id'] == personal_id and datetime.now() - loan['date'] <= timedelta(days=1):
                applications += 1
        return applications >= configuration_provider.ConfigurationProvider.get_maximum_applications_per_24_hours()

    def calculate_monthly_repayement_amount(amount, monthly_interest, term):
        return round(amount * monthly_interest / (1 - (1 / (1 + monthly_interest) ** term)), 2)
