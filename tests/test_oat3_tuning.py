import unittest

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit

from oat3_tuning import criar_buscas_random_forest, descrever_variacao_percentual


class Oat3TuningTests(unittest.TestCase):
    def test_grid_search_usa_random_forest_e_validacao_temporal(self):
        grid, _ = criar_buscas_random_forest(random_state=42)

        self.assertIsInstance(grid.estimator, RandomForestRegressor)
        self.assertIsInstance(grid.cv, TimeSeriesSplit)
        self.assertIn("n_estimators", grid.param_grid)
        self.assertIn("max_depth", grid.param_grid)
        self.assertIn("min_samples_split", grid.param_grid)

    def test_random_search_usa_mesmo_espaco_temporal_e_limite_de_iteracoes(self):
        grid, random = criar_buscas_random_forest(random_state=42, n_iter=10)

        self.assertIsInstance(random.estimator, RandomForestRegressor)
        self.assertIsInstance(random.cv, TimeSeriesSplit)
        self.assertEqual(random.n_iter, 10)
        self.assertEqual(random.param_distributions, grid.param_grid)
        self.assertEqual(random.scoring, grid.scoring)

    def test_variacao_de_erro_distingue_melhoria_de_piora(self):
        self.assertEqual(
            descrever_variacao_percentual(12.70, 12.60),
            "reduziu em 0.79%",
        )
        self.assertEqual(
            descrever_variacao_percentual(12.70, 12.80),
            "aumentou em 0.79%",
        )


if __name__ == "__main__":
    unittest.main()
