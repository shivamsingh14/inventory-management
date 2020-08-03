from django.conf import settings

MAX_LENGTH_DICT = {
    "SMALL": 1
}

ERROR_MESSAGES = {
    "AVERAGE_AREA_MAX_REACHED": "The max average area exceeds permitted value",
    "AVERAGE_VOLUME_MAX_REACHED": "The max average volume exceeds permitted value",
    "BOX_ADDED_THIS_WEEK_MAX_REACHED": "The max number of boxes limit reached for this week",
    "BOX_ADDED_THIS_WEEK_MAX_REACHED_BY_USER": "The max number of boxes added by a user limit reached for this week"
}

THRESHOLD_VALUES = {
    "AREA": settings.A1,
    "VOLUME_ADDED_BY_USER": settings.V1,
    "TOTAL_BOXES_ADDED_IN_WEEK": settings.L1,
    "TOTAL_BOXES_ADDED_IN_WEEK_BY_USER": settings.L2
}
