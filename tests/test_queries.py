"""
Testes para as queries do banco de dados
"""

import unittest
from app.db.queries import Queries

class TestQueries(unittest.TestCase):
    
    def setUp(self):
        self.queries = Queries()
    
    def test_get_turnos(self):
        """Testa a obtenção de turnos"""
        pass
    
    def test_get_relatorio(self):
        """Testa a obtenção de relatório"""
        pass

if __name__ == '__main__':
    unittest.main()
