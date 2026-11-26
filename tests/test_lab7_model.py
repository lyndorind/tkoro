"""Small DB-independent unit tests, run in parallel with Postman integration tests."""

import unittest

from pydantic import ValidationError

from db_api import NoteIn


class NoteInputTests(unittest.TestCase):
    def test_valid_text(self):
        self.assertEqual(NoteIn(text="A note").text, "A note")

    def test_empty_note_is_rejected(self):
        with self.assertRaises(ValidationError):
            NoteIn(text="")

    def test_over_500_characters_is_rejected(self):
        with self.assertRaises(ValidationError):
            NoteIn(text="x" * 501)

    def test_exactly_500_characters_is_accepted(self):
        self.assertEqual(len(NoteIn(text="x" * 500).text), 500)


if __name__ == "__main__":
    unittest.main()
