from src.dataset_aggregation import create_dataset_report
from src.concept_aggregation import create_concept_report
from src.information_model_aggregation import create_information_model_report
from src.utils import ServiceKey, QueryParameter


def get_report(content_type: ServiceKey, args: dict):
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme = args.get(QueryParameter.THEME)
    theme_profile = args.get(QueryParameter.THEME_PROFILE)
    organization_id = args.get(QueryParameter.ORGANIZATION_ID)
    if content_type == ServiceKey.DATA_SETS:
        return create_dataset_report(orgpath, theme, theme_profile, organization_id)
    elif content_type == ServiceKey.CONCEPTS:
        return create_concept_report(orgpath, organization_id)
    elif content_type == ServiceKey.INFO_MODELS:
        return create_information_model_report(orgpath, organization_id)
    else:
        raise KeyError()
