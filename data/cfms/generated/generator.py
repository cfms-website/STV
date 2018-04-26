import json
import random
import time
import numpy
import os

RACES = {
    "ontario_rep": "1",
    "vpsa": "2"
}
RACES_CANDIDATES = {}
RACE_CANDIDATES = 5
VOTERS = 43


class PushID(object):
    # Modeled after base64 web-safe chars, but ordered by ASCII.
    PUSH_CHARS = ('-0123456789'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  '_abcdefghijklmnopqrstuvwxyz')

    def __init__(self):

        # Timestamp of last push, used to prevent local collisions if you
        # pushtwice in one ms.
        self.lastPushTime = 0

        # We generate 72-bits of randomness which get turned into 12
        # characters and appended to the timestamp to prevent
        # collisions with other clients.  We store the last characters
        # we generated because in the event of a collision, we'll use
        # those same characters except "incremented" by one.
        self.lastRandChars = numpy.empty(12, dtype=int)

    def next_id(self):
        now = int(time.time() * 1000)
        duplicateTime = (now == self.lastPushTime)
        self.lastPushTime = now
        timeStampChars = numpy.empty(8, dtype=str)

        for i in range(7, -1, -1):
            timeStampChars[i] = self.PUSH_CHARS[now % 64]
            now = int(now / 64)

        if (now != 0):
            raise ValueError('We should have converted the entire timestamp.')

        uid = ''.join(timeStampChars)

        if not duplicateTime:
            for i in range(12):
                self.lastRandChars[i] = int(random.random() * 64)
        else:
            # If the timestamp hasn't changed since last push, use the
            # same random number, except incremented by 1.
            for i in range(11, -1, -1):
                if self.lastRandChars[i] == 63:
                    self.lastRandChars[i] = 0
                else:
                    break
            self.lastRandChars[i] += 1

        for i in range(12):
            uid += self.PUSH_CHARS[self.lastRandChars[i]]

        if len(uid) != 20:
            raise ValueError('Length should be 20.')
        return uid


uid_generator = PushID()


def main():
    base_path = os.path.join(os.path.dirname(__file__))
    with open(os.path.normpath(os.path.join(base_path, "./data/firstname.json"))) as firstname_file:
        first_names = json.loads(firstname_file.read())
    with open(os.path.normpath(os.path.join(base_path, "./data/lastname.json"))) as lastname_file:
        last_names = json.loads(lastname_file.read())

    return_candidate_data = {}
    return_ballot_data = {}

    candidate_id = 1

    for race in RACES:
        # Generate candidates in race.
        return_candidate_data[race] = []
        RACES_CANDIDATES[RACES[race]] = []
        for x in range(RACE_CANDIDATES):
            race_candidate = {
                "name": random.choice(first_names) + " " + random.choice(last_names),
                "number": str(candidate_id),
                "school": random.choice(first_names) + " School"
            }
            RACES_CANDIDATES[RACES[race]].append(str(race_candidate["number"]))
            candidate_id += 1
            return_candidate_data[race].append(race_candidate)

    for x in range(VOTERS):
        ballot = {}
        for race in RACES_CANDIDATES:
            ballot[race] = random.sample(RACES_CANDIDATES[race], random.randint(1, len(RACES_CANDIDATES[race])))
        return_ballot_data[uid_generator.next_id()] = ballot

    with open(os.path.normpath(os.path.join(base_path, "./candidates.json")), "w") as candidates_out:
        json.dump(return_candidate_data, candidates_out)

    with open(os.path.normpath(os.path.join(base_path, "./ballots.json")), "w") as ballots_out:
        json.dump(return_ballot_data, ballots_out)


if __name__ == "__main__":
    main()
