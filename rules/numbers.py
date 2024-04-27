from yargy import rule, or_, predicates, and_
from yargy.predicates import gte, lte, in_

INT = rule(predicates.type('INT'))

FLOAT = rule(
    INT,
    predicates.in_({',', '.'}),
    INT
)

DATE_DAY = and_(
    gte(1),
    lte(31))
MONTHS = {
    "январь",
    "февраль",
    "март",
    "апрель",
    "май",
    "июнь",
    "июль",
    "август",
    "сентябрь",
    "октябрь",
    "ноябрь",
    "декабрь"
}
DATE_MONTH = or_(in_(MONTHS), and_(gte(1), lte(12)))