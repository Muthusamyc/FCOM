import json

from fcom.settings import env
from commons.booking_stages import STAGE_GROUP
from commons.roles import ROLE_CHOICES_MAP


def insert_meta(request):
    meta_data_file = "data/meta_data.json"
    with open(meta_data_file) as json_file:
        all_meta_data = json.load(json_file)
    endpoint = request.path
    url_data = endpoint.split("/")[1]
    if url_data == "":
        return dict(meta_data=all_meta_data["page"]["home"], endpoint=endpoint)

    elif url_data == "services":
        return dict(meta_data=all_meta_data["page"]["services"], endpoint=endpoint)

    elif url_data == "our-story":
        return dict(meta_data=all_meta_data["page"]["our-story"], endpoint=endpoint)

    elif url_data == "my-profile":
        return dict(meta_data=all_meta_data["page"]["my-profile"], endpoint=endpoint)

    elif url_data == "my-bookings":
        return dict(meta_data=all_meta_data["page"]["my-bookings"], endpoint=endpoint)

    else:
        return dict(meta_data=all_meta_data["page"]["home"], endpoint=endpoint)


def paytm_env(request):
    PAYTM_MID = env("PAYTM_MID")
    PAYTM_ENVIRONMENT = env("PAYTM_ENVIRONMENT")
    return dict(mid=PAYTM_MID, paytm_env=PAYTM_ENVIRONMENT)


def bookin_stage(request):
    return dict(booking_stage=STAGE_GROUP)


def get_role_id(request):
    return dict(role=ROLE_CHOICES_MAP)
