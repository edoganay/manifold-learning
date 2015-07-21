from unittest import TestCase
from sklearn import datasets, manifold
from time import time

from manifold.learning import algorithms
from manifold.infrastructure import Displayer


class ISOMAPTest(TestCase):
    def test_swiss_roll(self):
        samples = 1000
        neighbors = 10
        epsilon = 5
        to_dimension = 2

        data, c = datasets.make_swiss_roll(n_samples=samples, random_state=0)
        displayer = Displayer(title="Isomap algorithms comparison") \
            .load(title="Swiss roll from %i samples." % (samples,), data=data, color=c)

        start = time()
        result = manifold.Isomap(neighbors, to_dimension).fit_transform(data)
        elapsed = time() - start

        displayer \
            .load(
                title="SKLearn's Isomap with %i neighbors, taking %.1fs." % (neighbors, elapsed),
                data=result,
                color=c)

        start = time()
        result = algorithms \
            .Isomap(data, color=c, nearest_method='e', e=epsilon, to_dimension=to_dimension) \
            .run()
        elapsed = time() - start

        displayer.load(
            title="My E-Isomap with epsilon %i, taking %.1fs." % (epsilon, elapsed),
            data=result,
            color=c)

        start = time()
        result = algorithms \
            .Isomap(data, color=c, k=neighbors, to_dimension=to_dimension) \
            .run()
        elapsed = time() - start

        displayer.load(
            title="My K-Isomap with %i neighbors, taking %.1fs." % (neighbors, elapsed),
            data=result,
            color=c)

        displayer.render()