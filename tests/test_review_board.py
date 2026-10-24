import unittest
from src.review_board import render_board

class ReviewBoardTests(unittest.TestCase):
    def test_empty_board(self):
        result = render_board({'publication_allowed':False,'pending_claims':[]})
        self.assertIn('PUBLICACION BLOQUEADA', result)

    def test_reject_unsafe_candidate(self):
        with self.assertRaises(ValueError):
            render_board({'publication_allowed':False,'pending_claims':[{'status':'unverified','publication_allowed':True}]})
