from yargy import rule, or_

from rules.fever import FEVER
from rules.sensation import SENSATION

GENERAL = rule(
    or_(
        FEVER,
        SENSATION
    )
)
