from yargy import forward
from yargy import or_
from yargy import rule
from yargy.pipelines import morph_pipeline
from yargy.predicates import dictionary

ANATOMY_STOMACH = rule(
    dictionary({
        "желудок"
    })
)
ANATOMY_ABDOMEN = rule(
    dictionary({
        "живот"
    })
)
ANATOMY_SIDE = rule(
    dictionary(
        {"левый", "правый", "верхний", "нижний", "внешний", "внутренний", "медиальный", "проксимальный", "дистальный",
         "внешний", "внутренний"}
    )
)
ANATOMY_ARM = rule(
    ANATOMY_SIDE,
    dictionary({
        "рука", "верхняя конечность", "плечо", "локоть"
    })
)
ANATOMY_LEG = rule(
    ANATOMY_SIDE,
    dictionary({
        "нога", "нижняя конечность", "бедро", "голень"
    })
)
ANATOMY_HEAD = rule(
    dictionary({
        "голова", "головной"
    })
)
ANATOMY_LNODE = rule(
    dictionary({
        "лимфатический узел"
    })
)
ANATOMY_SPECIFIER = rule(
    dictionary({
        "Поверхность", "Кожа", "Область"
    })
)
ANATOMY_EAR = rule(
    morph_pipeline({
        "Ухо",
        "Ушная раковина"
    })
)
ANATOMY_UNIT = rule(
    or_(
       ANATOMY_HEAD, ANATOMY_LEG, ANATOMY_ARM, ANATOMY_ABDOMEN, ANATOMY_STOMACH, ANATOMY_LNODE, ANATOMY_EAR
    )
)
# ANATOMY_UNIT.define(
#     or_(
#         rule(
#             ANATOMY_SIDE.optional(),
#             or_(
#                 ANATOMY_HEAD, ANATOMY_LEG, ANATOMY_ARM, ANATOMY_ABDOMEN, ANATOMY_STOMACH, ANATOMY_LNODE
#             )
#         ),
#         rule(
#             ANATOMY_SIDE.optional(),
#             ANATOMY_SPECIFIER,
#             ANATOMY_UNIT
#         )
#     )
# )
