"""
Testes para o serviço de métricas
"""

import unittest
from app.services.metrics_service import MetricsService

class TestMetricsService(unittest.TestCase):
    
    def setUp(self):
        self.metrics_service = MetricsService()
    
    def test_calcular_horas_total(self):
        """Testa o cálculo de horas totais"""
        pass
    
    def test_calcular_media_horas(self):
        """Testa o cálculo de média de horas"""
        pass

if __name__ == '__main__':
    unittest.main()
