import unittest
from . import get_encoder

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = get_encoder('gpt3')
        self.codex_encoder = get_encoder('codex')

    def test_empty_string(self):
        text = ''
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [], 'empty string encode error')
        self.assertEqual(decoded, text, 'empty string decode error')

    def test_single_space(self):
        text = ' '
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [220], 'single space encode error')
        self.assertEqual(decoded, text, 'single space decode error')

    def test_single_tab(self):
        text = '\t'
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [197], 'single tab encode error')
        self.assertEqual(decoded, text, 'single tab decode error')

    def test_simple_text(self):
        text = 'This is some text'
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [1212, 318, 617, 2420], 'simple text encode error')
        self.assertEqual(decoded, text, 'simple text decode error')

    def test_multi_token_word(self):
        text = 'indivisible'
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [521, 452, 12843], 'multi-token word encode error')
        self.assertEqual(decoded, text, 'multi-token word decode error')

    def test_emojis(self):
        text = "hello 👋 world 🌍"
        encoded = self.encoder.encode(text)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(encoded, [31373, 50169, 233, 995, 12520, 234, 235], 'emojis encode error')
        self.assertEqual(decoded, text, 'emojis decode error')

    def test_codex(self):
        text = "def main():\n    print('hello world')"
        encoded = self.codex_encoder.encode(text)
        decoded = self.codex_encoder.decode(encoded)
        self.assertEqual(encoded, [4299, 1388, 33529, 198, 50258, 3601, 10786, 31373, 995, 11537], 'codex encode error')
        self.assertEqual(decoded, text, 'codex decode error')
