# amDg
# +JMJ
import json
import random
from random import choice, random


class User:
    def __init__(self, slider):
        self.loci = None
        self.slider = slider
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

    def slider_choice(self, A, B) -> str:
        """
        From 100% A at slider_value=0 to 0% A at slider_value=6
        """
        # Calculate the probability for A based on the slider value
        prob_A = (6 - self.slider) / 6.0  # From 100% A at slider_value=0 to 0% A at slider_value=6
        prob_B = 1 - prob_A  # Complementary probability for B

        # Randomly choose between A and B based on the calculated probabilities
        return A if random() < prob_A else B




