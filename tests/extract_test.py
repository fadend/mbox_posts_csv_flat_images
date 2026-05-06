from mbox_posts_csv_flat_images import extract
import unittest


class ExtractTestCase(unittest.TestCase):
    def testExtractBodyContent(self):
        self.assertEqual(
            "<b>bold!</b>",
            extract.extract_body_content(
                "<html><head><title>Y?!</title></head><body> <b>bold!</b>\t\n</body></html>"
            ),
        )
        self.assertEqual(
            "<em>Mm</em>",
            extract.extract_body_content(
                '<html><head><title>Y?!</title></head><body style="color: red"><em>Mm</em></body></html>'
            ),
        )
