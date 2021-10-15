from unittest.mock import patch

from django.core.management import call_command
# simulate the db being available or not when run the command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # try and retrieve db connection from django
        # check if it retrieves Operationalerror or not
        # Overwrite the behavior of ConnectionHandler
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # Mock the behavior of time.sleep, replaces it with a
    # mock function that returns true.
    # same thing as above, it will pass in as an argument ts what is
    # equivalent of 'gi'
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # Usuallay we do while loop to check if Operational error is
        #  raised or not. If raised, wait for one second and try again
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # First 5 times you call the getitem will raise Operationalerror
            # On the sixth time it will return
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
