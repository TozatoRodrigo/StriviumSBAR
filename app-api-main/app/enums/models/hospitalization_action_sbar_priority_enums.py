from enum import StrEnum


class HospitalizationActionSbarPriority(StrEnum):
    ROUTINE = "routine"
    ATTENTION = "attention"
    CRITICAL = "critical"
