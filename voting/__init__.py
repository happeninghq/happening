""" Alternative vote. """


class AVVote(object):

    """ Alternative vote. """

    def __init__(self, ignore=None):
        """ Initialize alternative vote. """
        self.preferences = []
        if not ignore:
            ignore = []
        self.ignored = ignore

    def add_preference(self, preference):
        """ Add a user's preferences to the vote (as a list). """
        self.preferences.append(
            [p for p in preference if p not in self.ignored])

    @property
    def winner(self):
        """ Get the winning preference. """
        def _winner(preferences):
            counts = {}

            preferences = [p for p in preferences if len(p) > 0]

            # First count up all first choice votes
            for p in preferences:
                first_choice = p[0]
                if first_choice not in counts:
                    counts[first_choice] = 0
                counts[first_choice] += 1

            # Then turn counts into percentages
            total = len(preferences)
            lowest_percentage = (1, None)

            for c in counts:
                counts[c] = (counts[c] * 1.0) / total
                if counts[c] > 0.5:
                    # We have a winner
                    return c
                elif counts[c] < lowest_percentage[0]:
                    lowest_percentage = (counts[c], c)

            # No winner yet
            def remove_c(key, preference):
                return [p for p in preference if not key == p]

            preferences = [remove_c(lowest_percentage[1], i) for
                           i in preferences]
            return _winner(preferences)
        return _winner(self.preferences)
