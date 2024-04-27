from yargy import forward, or_, rule

from rules.erythema import ERYTHEMA
from rules.fever import FEVER
from rules.location import ANATOMY_UNIT
from rules.sensation import SENSATION

SIGN = forward()

SIGN.define(
    or_(
        or_(
            FEVER,
            ERYTHEMA,
            SENSATION

        ),
        rule(
            ANATOMY_UNIT,
            SIGN
        ),
    )
)

