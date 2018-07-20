import unittest
import os

from modules import api
import namestat


class TestUM(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUM, self).__init__(*args, **kwargs)

        test_path = "example_file"
        self.path = os.path.join('.', test_path)

    def test_top_functions_names_path(self):
        functions_names = api.get_top_functions_names_in_path(self.path, 10, 'python')
        self.assertEqual(8, len(functions_names))
        self.assertEqual(8, len(set(functions_names)))

    def test_top_functions_verbs_in_path(self):
        verbs = namestat.get_top_part_speech(self.path, 10, 'verb', 'global', 'python')
        total_verbs = [vb[1] for vb in verbs]
        self.assertEqual(8, sum(total_verbs))
        self.assertEqual(7, len(set(verbs)))

    def test_top_functions_noun_in_path(self):
        nouns = namestat.get_top_part_speech(self.path, 10, 'noun', 'global', 'python')
        total_nouns = [noun[1] for noun in nouns]
        self.assertEqual(1, sum(total_nouns))
        self.assertEqual(1, len(set(nouns)))

    def test_all_names_in_path(self):
        names = api.get_all_names_in_path(self.path, 'python')
        self.assertEqual(4, len(names))
        self.assertEqual(3, len(set(names)))


if __name__ == '__main__':
    unittest.main()
