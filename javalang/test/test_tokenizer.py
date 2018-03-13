import unittest
from .. import tokenizer


class TestTokenizer(unittest.TestCase):

    def test_tokenizer_annotation(self):
        # Given
        code = "    @Override"

        # When
        tokens = list(tokenizer.tokenize(code))

        # Then
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].value, "@")
        self.assertEqual(tokens[1].value, "Override")
        self.assertEqual(type(tokens[0]), tokenizer.Annotation)
        self.assertEqual(type(tokens[1]), tokenizer.Identifier)

    def test_tokenizer_javadoc(self):
        # Given
        code = "/**\n" \
               " * See {@link BlockTokenSecretManager#setKeys(ExportedBlockKeys)}\n" \
               " */"

        # When
        tokens = list(tokenizer.tokenize(code))

        # Then
        self.assertEqual(len(tokens), 0)

    def test_tokenize_ignore_errors(self):
        # Given
        # character '#' was supposed to trigger an error of unknown token with a single line of javadoc
        code = " * See {@link BlockTokenSecretManager#setKeys(ExportedBlockKeys)}"

        # When
        tokens = list(tokenizer.tokenize(code, ignore_errors=True))

        # Then
        self.assertEqual(len(tokens), 11)

    def test_tokenize_comment_line_with_period(self):
        # Given
        code = "   * all of the servlets resistant to cross-site scripting attacks."

        # When
        tokens = list(tokenizer.tokenize(code))

        # Then
        self.assertEqual(len(tokens), 13)

    def test_tokenize_number_at_end(self):
        # Given
        code = "nextKey = new BlockKey(serialNo, System.currentTimeMillis() + 3"

        # When
        tokens = list(tokenizer.tokenize(code, ignore_errors=True))

        # Then
        self.assertEqual(len(tokens), 14)
