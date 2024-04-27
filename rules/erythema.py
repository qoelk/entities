from yargy import rule
from yargy import predicates
from yargy import or_, and_, not_
from yargy import pipelines
from yargy.interpretation import fact, attribute
from yargy.predicates import dictionary, gram


Erythema = fact(
    'Erythema',
    []
)

ERYTHEMA = rule(pipelines.morph_pipeline([
    'покраснение',
    'эритема',
    'гиперемия',
    'гиперемирована'
])).interpretation(Erythema)

