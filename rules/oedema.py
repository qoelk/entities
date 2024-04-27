from yargy import rule, pipelines

OEDEMA = rule(pipelines.morph_pipeline([
    'отёк',
    'припухлость',
]))
