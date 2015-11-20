import abc
import multiprocessing
import time
import numpy as np
from scipy.spatial import distance
from sklearn import grid_search, decomposition, svm, manifold
from manifold.infrastructure import Displayer
from manifold.infrastructure.base import kruskal_stress
from manifold.learning.algorithms import Isomap, MDS


class Experiment(metaclass=abc.ABCMeta):
    title = None

    _displayer = None
    plotting = False

    exporting_path = '../report/img/experiments'

    @property
    def displayer(self):
        self._displayer = self._displayer or Displayer(plotting=self.plotting)
        return self._displayer

    def _run(self):
        raise NotImplementedError

    def _dispose(self):
        pass

    def start(self):
        print('%s\n' % self.title)

        self._run()
        self._dispose()


class LearningExperiment(Experiment, metaclass=abc.ABCMeta):
    learner = svm.SVC
    data = target = labels = grid = None

    learning_parameters = [
        {'C': (1, 10, 100, 1000), 'kernel': ('linear',)},
        {'C': (1, 10, 100, 1000), 'gamma': (.001, .01, .1, 1, 10), 'kernel': ('rbf', 'sigmoid')}
    ]

    def learn(self):
        print('Learning...')

        start = time.time()

        self.grid = grid_search.GridSearchCV(self.learner(), self.learning_parameters, n_jobs=-1)
        self.grid.fit(self.data, self.target)

        print('\tAccuracy: %.2f' % self.grid.best_score_)
        print('\tBest parameters: %s' % self.grid.best_params_)
        print('Done. (%.6f s)\n' % (time.time() - start))


class ReductionExperiment(Experiment, metaclass=abc.ABCMeta):
    data = original_data = target = None

    reducer = None
    reduction_method = 'isomap'
    reduction_params = {
        'k': 4,
        'n_components': 3
    }

    def reduce(self):
        assert self.reduction_method in ('pca', 'mds', 'isomap', 'skisomap'), 'Error: unknown reduction method.'

        print('Reducing...')

        to_dimension = self.reduction_params['to_dimension'] if 'to_dimension' in self.reduction_params else \
            self.reduction_params['n_components'] if 'n_components' in self.reduction_params else \
                3

        data = self.original_data

        print('\tMethod: %s' % self.reduction_method)
        print('\tR^%i --> R^%i' % (data.shape[1], to_dimension))

        start = time.time()

        if self.reduction_method == 'pca':
            self.reducer = decomposition.PCA(**self.reduction_params)
            self.data = self.reducer.fit_transform(data)

        elif self.reduction_method == 'mds':
            self.reducer = MDS(**self.reduction_params)
            self.data = self.reducer.transform(data)

        elif self.reduction_method == 'skisomap':
            self.reducer = manifold.Isomap(**self.reduction_params)
            self.data = self.reducer.fit_transform(data)

        else:
            self.reducer = Isomap(**self.reduction_params)
            self.data = self.reducer.transform(data)

        if self.reduction_method in ('mds', 'isomap'):
            print('\tstress: %f' % self.reducer.stress)
        else:
            print('\tstress: %f' % kruskal_stress(
                distance.squareform(distance.pdist(self.original_data)),
                distance.squareform(distance.pdist(self.data))))

        print('\tsize: %f KB' % (self.data.nbytes / 1024))
        print('Done. (%.6f s)\n' % (time.time() - start))

        self.displayer.load(self.data, self.target)
