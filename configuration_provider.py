import configparser


class ConfigurationProvider:

    @staticmethod
    def get_blacklist():
        config = configparser.ConfigParser()
        config.read('config.ini')
        section = config['loan_application']
        return section['blacklist'].split(',')

    @staticmethod
    def get_maximum_applications_per_24_hours():
        config = configparser.ConfigParser()
        config.read('config.ini')
        section = config['loan_application']
        return int(section['maximum_applications_per_24_hours'])

    @staticmethod
    def get_monthly_interest_rate():
        config = configparser.ConfigParser()
        config.read('config.ini')
        section = config['loan_application']
        return float(section['monthly_interest_rate'])
