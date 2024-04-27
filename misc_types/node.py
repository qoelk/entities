class Node:

    def __init__(self, type, matches):
        self.entity_type = type
        self.matches = matches


    def __repr__(self):
        return ' '.join([token.value for token in self.matches.tokens])
