import unittest
from src.queue import normalize

class QueueInputValidationTests(unittest.TestCase):
    def test_nontext_title(self):
        self.assertIsNone(normalize({"title":42,"url":"https://example.org/a"}))

    def test_nontext_url(self):
        self.assertIsNone(normalize({"title":"Noticia","url":None}))

    def test_long_url(self):
        self.assertIsNone(normalize({"title":"Noticia","url":"https://example.org/"+"a"*2100}))

    def test_newline_in_url(self):
        self.assertIsNone(normalize({"title":"Noticia","url":"https://example.org/a\nb"}))
