import unittest
from unittest.mock import patch
from io import BytesIO
from src.discovery import fetch_feed, discover

class FakeResponse:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def read(self, limit):
        return b'<rss><channel><item><title>Dato publico</title><link>https://example.org/a</link></item></channel></rss>'

class DiscoveryTests(unittest.TestCase):
    @patch("urllib.request.urlopen", return_value=FakeResponse())
    def test_rss(self, mock):
        self.assertEqual(fetch_feed("https://example.org/feed")[0]["title"], "Dato publico")
    @patch("urllib.request.urlopen")
    def test_atom(self, mocked):
        response = FakeResponse()
        response.read = lambda limit: (
            b'<feed xmlns="http://www.w3.org/2005/Atom">'
            b'<entry><title>Dato oficial</title>'
            b'<link rel="alternate" href="https://example.org/documento"/></entry></feed>')
        mocked.return_value = response
        result = fetch_feed("https://example.org/atom")
        self.assertEqual(result[0]["title"], "Dato oficial")

    @patch("urllib.request.urlopen")
    def test_rejects_xml_doctype(self, mocked):
        response = FakeResponse()
        response.read = lambda limit: b'<!DOCTYPE rss [<!ENTITY test "unsafe">]><rss/>'
        mocked.return_value = response
        with self.assertRaises(ValueError):
            fetch_feed("https://example.org/feed")

    def test_explicit_empty_feed_list(self):
        self.assertEqual(discover([])["candidates"], [])

    def test_no_http(self):
        with self.assertRaises(ValueError):
            fetch_feed("http://example.org/feed")
    @patch("src.discovery.fetch_feed", side_effect=RuntimeError("network"))
    def test_failure_is_not_verdict(self, mock):
        result = discover(["https://example.org/feed"])
        self.assertEqual(result["candidates"], [])
        self.assertEqual(result["errors"][0]["error"], "RuntimeError")

if __name__ == "__main__":
    unittest.main()
