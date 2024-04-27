from yargy import rule, and_, or_
from yargy.interpretation import fact
from yargy.predicates import gte, lte, dictionary

DAY = and_(
    gte(1),
    lte(31))
MONTH = and_(
    gte(1),
    lte(12))
YEAR = and_(
    gte(1),
    lte(2040))
HOUR = and_(
    gte(1),
    lte(23))
MINUTE = and_(
    gte(1),
    lte(59))
Date = fact(
    'Date',
    ['day', 'month', 'year']
)
Time = fact(
    'Time',
    ['hour', 'minute']
)
DATE = rule(
    DAY.interpretation(Date.day),
    '.',
    MONTH.interpretation(Date.month),
    '.',
    YEAR.interpretation(Date.year)
).interpretation(Date)
TIME = rule(
    HOUR.interpretation(Time.hour),
    ':',
    MINUTE.interpretation(Time.minute)
).interpretation(Time)
RELATIVE_TIME = rule(
    dictionary({
        "затем", "позже"
    })
)
DATETIME = rule(
    or_(
        rule(
            DATE,
            TIME.optional()

        ),
        RELATIVE_TIME
    )
)
GENERAL_DATETIME = rule(
    'Дата',
    ':',
    DATETIME
)
