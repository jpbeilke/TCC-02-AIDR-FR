"""
Testes para o serviço de ranking
"""

import unittest
from app.services.ranking_service import RankingService

class TestRankingService(unittest.TestCase):
    
    def setUp(self):
        self.ranking_service = RankingService()
    
    def test_gerar_ranking(self):
        """Testa a geração de ranking"""
        pass
    
    def test_ordenar_por_horas(self):
        """Testa a ordenação por horas"""
        pass

if __name__ == '__main__':
    unittest.main()
