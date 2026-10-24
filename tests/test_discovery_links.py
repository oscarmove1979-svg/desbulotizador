import unittest
from unittest.mock import patch
from src.discovery import fetch_feed

class FeedResponse:
    def __init__(self, payload):
        self.payload=payload
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, limit):
        return self.payload

class DiscoveryLinkTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_rss_embedded_credentials_rejected(self, mocked):
        mocked.return_value=FeedResponse(b"<rss><channel><item><title>Data 2025</title><link>https://user:secret@example.org/x</link></item></channel></rss>")
        self.assertEqual(fetch_feed("https://example.org/feed"),[])

    @patch("urllib.request.urlopen")
    def test_atom_embedded_credentials_rejected(self, mocked):
        mocked.return_value=FeedResponse(b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Data 2025</title><link href="https://user:secret@example.org/x"/></entry></feed>')
        self.assertEqual(fetch_feed("https://example.org/feed"),[])
