from io import StringIO
from datetime import date, timedelta
from unittest import TestCase
from unittest.mock import patch

from view import View
from model import PressureStatistics


class ViewTestCase(TestCase):
    def setUp(self):
        self.view = View()

    def test__init__(self):
        view = View()
        self.assertFalse(view.model)
        view = View(model="Test model")
        self.assertEqual(view.model, "Test model")

    def test_get_main_menu_choice_cli(self):
        with patch('sys.argv', ['main.py', '-a']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 1)

        with patch('sys.argv', ['main.py', '-u']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 2)

        with patch('sys.argv', ['main.py', '-d']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 3)

        with patch('sys.argv', ['main.py', '-pw']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 4)

        with patch('sys.argv', ['main.py', '-pm']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 5)

        with patch('sys.argv', ['main.py', '-p']):
            result = self.view.get_main_menu_choice_cli()
            self.assertEqual(result, 6)

    @patch('backends.get_pickle.PickleSerializer.read', return_value={})
    def test_print_for_time(self, *mocks):
        self.view.model = PressureStatistics()
        self.view.model.update(date(2016, 5, 11), ['120', '80'])
        self.view.model.update(date(2016, 5, 1), ['120', '80'])
        self.view.model.update(date(2016, 2, 1), ['120', '80'])
        out = StringIO()
        import sys
        sys.stdout = out
        self.view.print_for_time(timedelta(weeks=4))
        expected_result = "2016-05-01 - 120, 80\n2016-05-11 - 120, 80\n"
        self.assertEqual(out.getvalue(), expected_result)

