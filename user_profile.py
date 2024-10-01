# amDg
# +JMJ
import json
import random
from random import choice


class User:
    def __init__(self):
        self.loci = None
        self.set_localization()

    def set_localization(self):
        with open("litcalendar/loci.json", encoding="utf-8") as f:
            loci = json.load(f)


        locis = [(key, value) for key, value in loci.items()]
        abreviatures = []
        for i in range(3):
            abreviatures.extend([x for x in locis[i][1].keys()])

        # self.loci = choice(abreviatures)
        self.loci = "bzy"
