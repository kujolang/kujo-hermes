import unittest
import pyte
from terminal_text import replay_text
class ReplayTests(unittest.TestCase):
    def test_selector_does_not_hide_approval_words(self):
        screen=pyte.Screen(60,4)
        pyte.Stream(screen).feed(replay_text('⚠️ Dangerous Command\r\n1. Allow once'))
        self.assertIn('Dangerous Command',screen.display[0])
        self.assertIn('1. Allow once',screen.display[1])
    def test_text_and_control_sequences_are_preserved(self):
        value='\x1b[31m5099 != 4500\r\nкужо'
        self.assertEqual(replay_text(value),value)
if __name__=='__main__':unittest.main()
