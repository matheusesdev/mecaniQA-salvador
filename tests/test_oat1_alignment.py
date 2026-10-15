import unittest

import numpy as np
import pandas as pd

from oat1_processing import (
    criar_baselines,
    tratar_dados_mecaniqa,
)


class Oat1AlignmentTests(unittest.TestCase):
    def test_limpeza_interpola_ausentes_e_remove_outlier_sem_quebrar_linha_do_tempo(self):
        datas = pd.date_range("2026-01-01", periods=9, freq="D")
        dados = pd.DataFrame(
            {
                "Data": datas,
                "Trocas_Oleo": [10.0, 11.0, np.nan, 12.0, 150.0, 13.0, 12.0, 11.0, 10.0],
                "Manutencao_Motor": [2.0, 3.0, -5.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0],
            }
        )

        limpos, relatorio = tratar_dados_mecaniqa(dados)

        self.assertEqual(limpos.index.tolist(), datas.tolist())
        self.assertFalse(limpos.isna().any().any())
        self.assertNotEqual(limpos.loc["2026-01-05", "Trocas_Oleo"], 150.0)
        self.assertGreaterEqual(limpos["Manutencao_Motor"].min(), 0.0)
        self.assertEqual(relatorio["ausentes_trocas_oleo"], 1)
        self.assertEqual(relatorio["outliers_trocas_oleo"], 1)
        self.assertEqual(relatorio["negativos_manutencao_motor"], 1)

    def test_baselines_naive_sete_e_trinta_dias_usam_apenas_o_passado(self):
        indice = pd.date_range("2026-01-01", periods=35, freq="D")
        serie = pd.Series(range(1, 36), index=indice, dtype=float)

        baselines = criar_baselines(serie)

        self.assertEqual(baselines.loc["2026-01-31", "Naive"], 30.0)
        self.assertEqual(baselines.loc["2026-01-31", "Média móvel (7 dias)"], 27.0)
        self.assertEqual(baselines.loc["2026-01-31", "Média móvel (30 dias)"], 15.5)


if __name__ == "__main__":
    unittest.main()
