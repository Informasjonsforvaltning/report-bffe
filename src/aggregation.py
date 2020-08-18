from src.dataset_aggregation import create_dataset_report
from src.utils import ServiceKey, QueryParameter


def get_report(content_type: ServiceKey, args: dict):
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme = args.get(QueryParameter.THEME)
    return report_functions[content_type](orgpath, theme)


report_functions = {
    ServiceKey.DATA_SETS: create_dataset_report
}
