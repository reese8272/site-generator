import unittest
from main import extract_title

class TestMarkdownTitle(unittest.TestCase):
    def test_h1_title(self):
        md = '''# header

        with some text'''
        title = extract_title(md)
        self.assertEqual("header",title)

    def test_no_h1_raises_exception(self):
        md_no_h1 = '''## this is not an h1

        some content.'''
        with self.assertRaises(Exception):
            extract_title(md_no_h1)