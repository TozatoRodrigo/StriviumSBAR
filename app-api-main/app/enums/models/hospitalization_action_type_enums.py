from enum import StrEnum


class HospitalizationActionType(StrEnum):
    HOSPITALIZATION_VISIT = "hospitalization_visit"
    HOSPITALIZATION_DISCHARGE = "hospitalization_discharge"
    HOSPITALIZATION_DECEASED = "hospitalization_deceased"
