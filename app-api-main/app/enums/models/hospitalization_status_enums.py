from enum import StrEnum


class HospitalizationStatus(StrEnum):
    ACTIVE = "active"
    DISCHARGED = "discharged"
    DECEASED = "deceased"
