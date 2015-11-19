from sklearn import datasets

from experiments.base import ReductionExperiment


class ReducingDigitsExperiment(ReductionExperiment):
    title = '3. Reducing Digits'
    plotting = True

    def _run(self):
        digits = datasets.load_digits()

        self.data, self.target = digits.data, digits.target

        # Reduce Digits with PCA
        self.reduction_method = 'pca'

        for dimension in (3, 2):
            self.reduction_params = {'n_components': dimension}
            self.reduce()

        if self.plotting:
            self.displayer.show()


if __name__ == '__main__':
    ReducingDigitsExperiment().start()
