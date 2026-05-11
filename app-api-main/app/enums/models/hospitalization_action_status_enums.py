from enum import StrEnum


class HospitalizationActionStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    CANCELED = "canceled"
