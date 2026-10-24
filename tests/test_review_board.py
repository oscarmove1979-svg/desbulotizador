import unittest
from src.review_board import render_board

class ReviewBoardTests(unittest.TestCase):
    def test_empty_board(self):
        result = render_board({'publication_allowed':False,'pending_claims':[]})
        self.assertIn('PUBLICACION BLOQUEADA', result)

    def test_reject_unsafe_candidate(self):
        with self.assertRaises(ValueError):
            render_board({'publication_allowed':False,'pending_claims':[{'status':'unverified','publication_allowed':True}]})

    def test_embedded_linebreaks_are_removed(self):
        item = dict(status='unverified',publication_allowed=False,claim='Dato 2025\ntexto',source_url='https://example.org\n')
        board = render_board(dict(publication_allowed=False,pending_claims=[item]))
        self.assertIn('Dato 2025 texto', board)

    def test_missing_claim_rejected(self):
        record = dict(status='unverified',publication_allowed=False,claim='',source_url='https://example.org')
        with self.assertRaises(ValueError):
            render_board(dict(publication_allowed=False,pending_claims=[record]))

    def test_escapes_markup(self):
        item = dict(status='unverified',publication_allowed=False,claim='<script>2025</script>',source_url='https://example.org')
        board = render_board(dict(publication_allowed=False,pending_claims=[item]))
        self.assertNotIn('<script>', board)

    def test_oversized_claim_rejected(self):
        item = dict(status='unverified',publication_allowed=False,claim='A' * 2100,source_url='https://example.org')
        with self.assertRaises(ValueError):
            render_board(dict(publication_allowed=False,pending_claims=[item]))

    def test_non_https_source_rejected(self):
        item = dict(status='unverified',publication_allowed=False,claim='Dato 2025',source_url='http://example.org')
        with self.assertRaises(ValueError):
            render_board(dict(publication_allowed=False,pending_claims=[item]))
