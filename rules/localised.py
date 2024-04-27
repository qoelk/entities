from yargy import rule, or_

from rules.erythema import ERYTHEMA
from rules.oedema import OEDEMA
from rules.sensation import SENSATION

LOCALISED = rule(
    or_(
        ERYTHEMA,
        OEDEMA
    )
)