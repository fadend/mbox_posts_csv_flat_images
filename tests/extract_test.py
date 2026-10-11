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
    def testExtractITags(self):
        self.assertEqual(
            ["Phacelia californica", "Madia elegans", "Megachile sp."],
            extract.extract_i_tags('<div class="">Our <i class="">\tPh|acelia californ|ica    </i> is still going strong.'
                                   '<div class="">The <i class="plant">M|adia    eleg|ans </i>in our garden</div></div>'
                                   '...<i class=""><b>Phacelia</b>\tcaliforn|ica</i>...'
                                   '<i class="">Megach|ile\nsp.</i>')
        )
    def testExtractITagsNoEmpty(self):
        self.assertEqual(
            [],
            extract.extract_i_tags('<i></i>')
        )
