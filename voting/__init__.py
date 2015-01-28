class AVVote(object):
    def __init__(self):
        self.preferences = []

    def add_preference(self, preference):
        self.preferences.append(preference)

    @property
    def winner(self):
        def _winner(preferences):
            counts = {}

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
