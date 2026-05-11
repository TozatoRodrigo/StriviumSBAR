from enum import StrEnum


class HospitalizationActionSbarClinicalCourse(StrEnum):
    IMPROVED = "improved"
    STABLE = "stable"
    WORSENED = "worsened"
