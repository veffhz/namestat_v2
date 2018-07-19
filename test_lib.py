import unittest
import os

import namestat


class TestUM(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUM, self).__init__(*args, **kwargs)

        test_path = "example_file"
        self.path = os.path.join('.', test_path)

    def test_top_functions_names_path(self):
        functions_names = namestat.get_top_py_functions_names_in_path(self.path, 10)
        self.assertEqual(8, len(functions_names))
        self.assertEqual(8, len(set(functions_names)))

    def test_top_functions_verbs_in_path(self):
        verbs = namestat.get_top_py_functions_verbs_in_path(self.path, 10)
        total_verbs = [vb[1] for vb in verbs]
        self.assertEqual(8, sum(total_verbs))
        self.assertEqual(7, len(set(verbs)))

    def test_all_names_in_path(self):
        names = namestat.get_all_py_names_in_path(self.path)
        self.assertEqual(3, len(names))
        self.assertEqual(2, len(set(names)))


if __name__ == '__main__':
    unittest.main()
