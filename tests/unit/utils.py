from app.db.constants import ID
import unittest
from app.db.utils import is_valid_email
import re

def exclude_keys(item: dict, keys_to_exclude: set):
    """
    Remove specified keys from an item.
    """
    return {k: v for k, v in item.items() if k not in keys_to_exclude}

def assert_items_equal(actual, expected, extra_exclude=None):
    """
    Assert two items are equal, ignoring '_id' by default
    and ignoring any additional fields if provided.
    """
    if extra_exclude is None:
        extra_exclude = set()
    combined_exclude = {"_id"} | extra_exclude

    actual_minus_excluded = exclude_keys(actual, combined_exclude)
    expected_minus_excluded = exclude_keys(expected, combined_exclude)

    print("DEBUG actual =>", actual_minus_excluded)
    print("DEBUG expected =>", expected_minus_excluded)

    if ("name" in actual_minus_excluded):
        actual_minus_excluded["name"] = actual_minus_excluded["name"].lower()

    if ("name" in expected_minus_excluded):
        expected_minus_excluded["name"] = expected_minus_excluded["name"].lower()

    assert actual_minus_excluded == expected_minus_excluded # nosec B101


class TestEmailValidation(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(is_valid_email("test@gmail.com"))
        self.assertTrue(is_valid_email("user@company.com"))
        self.assertTrue(is_valid_email("name@co.uk"))
        self.assertTrue(is_valid_email("user123@example.org"))

    def test_invalid_emails(self):
        self.assertFalse(is_valid_email("invalidemail.com"))
        self.assertFalse(is_valid_email("user@domain"))
        self.assertFalse(is_valid_email("user@@domain.com"))
        self.assertFalse(is_valid_email("user@.com"))
        self.assertFalse(is_valid_email("user@domain..com"))

def normalize_text(text):
    slug = re.sub(r'\W+', '-', text.lower()).strip('-')  # Normalize the text --> standardizing for testing
    return slug

if __name__ == "__main__":
    unittest.main()
