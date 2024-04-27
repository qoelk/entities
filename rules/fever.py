from yargy import pipelines, or_
from yargy import predicates
from yargy import rule
from yargy.interpretation import fact

INT = rule(predicates.type('INT'))

FLOAT = rule(
    INT,
    predicates.in_({',', '.'}),
    predicates.in_('123456789')  # не больше одного знака после запятой
)

# { signs: { location, timeline }}
Fever = fact(
    'Temperature',
    ['value', 'type']
)
INT_OR_FLOAT = rule(or_(INT, FLOAT)).interpretation(Fever.value)
TEMPERATURE = rule(
    pipelines.morph_pipeline([
        'повышение',
        "понижение",
        "снижение"
    ]).optional(),
    pipelines.morph_pipeline([
        'температура',
        'темп.'
    ]),
    predicates.gram('PREP').repeatable().optional(),
    INT_OR_FLOAT.optional()
)
FEVER = rule(or_(
    TEMPERATURE,
    pipelines.morph_pipeline([
        'жар',
        'озноб',
        'познабливание'
    ]).interpretation(Fever.type).repeatable()
)).interpretation(Fever)


