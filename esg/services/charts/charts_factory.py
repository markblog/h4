import os
from collections import OrderedDict

from ruamel import yaml
from esg.models.portfolio_metric_date_model import PortfolioMetricDateModel

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
	generate the order dictionary loader
	"""

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(stream, OrderedLoader)


class ChartFactory(object):
    """docstring for ChartFactory"""

    def __init__(self, charting_rules):
        self.charting_rules = charting_rules

    def get_chart_instance_with_refection(self):
        chart = None

        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'charts_router.yml'), 'r') as config_file:
            try:
                config_chart_str = config_file.read()
                config_chart_dict = ordered_load(config_chart_str, Loader=yaml.SafeLoader)
                for key, value in config_chart_dict['route'].items():
                    if key == 'else' or not self._is_empty(
                            self.charting_rules.dic.get(config_chart_dict['key_tags'][key], None)):
                        for _, module_name in value.items():
                            kls = self._get_class(module_name)
                            if self.charting_rules.check_parameters(kls.parameter_settings()):
                                chart = kls()
                                return chart

            except yaml.YAMLError as e:
                raise e

        return chart

    def _is_empty(self, parameters_list):
        return parameters_list is None or len(parameters_list) == 0

    def _get_class(self, module_name):
        parts = module_name.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
