class ElectionCandidate:
    def __init__(self, candidate_id, candidate_name, candidate_school):
        self._id = candidate_id
        self._name = candidate_name
        self._school = candidate_school

    def id(self):
        return self._id

    def name(self):
        return self._name

    def school(self):
        return self._school

    def __hash__(self):
        return hash((self._id, self._name, self._school))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               (self.id(), self.name(), self.school()) == (other.id(), other.name(), other.school())

    def __str__(self):
        return self._name + " - " + self._school

    def __repr__(self):
        return self._name + " - " + self._school