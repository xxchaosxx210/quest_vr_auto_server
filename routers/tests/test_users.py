import unittest
import pytest

import routers.users as users


class TestUsers(unittest.TestCase):
    def test_authenticate_user_invalid(self):
        with pytest.raises(LookupError):
            users.authenticate_user("invalid", "invalid")

    def test_get_user_fail(self):
        with pytest.raises(LookupError):
            users.get_user("invalid")

    def test_get_password_hash(self):
        password = "password"
        hash = users.get_password_hash(password)
        assert users.verify_password(password, hash) == True

    def test_get_password_hash_fail(self):
        password = "password"
        hash = users.get_password_hash(password)
        assert users.verify_password("invalid", hash) == False
