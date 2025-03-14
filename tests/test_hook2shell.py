"""Unit tests for hook2shell"""

import datetime
import unittest
from hook2shell import hook2shell

class TestHook2shell(unittest.TestCase):
    """Class to hold hook2shell unit tests"""

    def test_is_future_date(self):
        """Test dates against today"""
        self.assertTrue(hook2shell.is_future_date("2067-01-01"))
        self.assertFalse(hook2shell.is_future_date(datetime.date.today()))
        self.assertFalse(hook2shell.is_future_date("2000-01-01"))

    def test_does_not_expire(self):
        """Test entries that do not have an expiration date"""
        self.assertTrue(hook2shell.does_not_expire("-"))
        self.assertTrue(hook2shell.does_not_expire("*"))
        self.assertFalse(hook2shell.does_not_expire(" "))
        self.assertFalse(hook2shell.does_not_expire("2038"))

    def test_is_valid_expiration(self):
        """Test dates and symbols as expiration identifiers"""
        self.assertTrue(hook2shell.is_valid_expiration("2067-01-01"))
        self.assertFalse(hook2shell.is_valid_expiration("2000-01-01"))
        self.assertTrue(hook2shell.is_valid_expiration("-"))
        self.assertTrue(hook2shell.is_valid_expiration("*"))
        self.assertFalse(hook2shell.is_valid_expiration(" "))
