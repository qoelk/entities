from yargy import rule, not_
from yargy.interpretation import fact
from yargy import pipelines
from yargy.predicates import normalized

Sensation = fact(
    'Sensation',
    ['value']
)
SENSATION = rule(
    not_(
        normalized(
                "степень"
        )
    ),
    pipelines.morph_pipeline([
        "боль",
        "тяжесть",
        "дискомфорт",
        "слабость",
        "потливость"
    ]).interpretation(Sensation.value)
).interpretation(Sensation)
