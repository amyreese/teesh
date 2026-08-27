# Copyright Amethyst Reese
# Licensed under the MIT license


from unittest import TestCase

import teesh


class SmokeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        import tracemalloc

        tracemalloc.start()

    def test_echo(self):
        result = teesh.run(
            "uv", "run", "-m", "teesh.tests.echo", "hello world", "testing"
        )
        self.assertEqual(
            teesh.CompletedProcess(
                cmd=("uv", "run", "-m", "teesh.tests.echo", "hello world", "testing"),
                returncode=0,
                stdout="hello world\ntesting\n",
                stderr="",
            ),
            result,
        )

    def test_false(self):
        with self.assertRaisesRegex(
            teesh.CalledProcessError, "Command 'uv' returned non-zero exit status 1."
        ):
            teesh.run("uv", "run", "-m", "teesh.tests.false")

    def test_false_no_check(self):
        result = teesh.run("uv", "run", "-m", "teesh.tests.false", check=False)
        self.assertEqual(
            teesh.CompletedProcess(
                cmd=("uv", "run", "-m", "teesh.tests.false"),
                returncode=1,
                stdout="",
                stderr="",
            ),
            result,
        )

    def test_mixed(self):
        result = teesh.run("uv", "run", "-m", "teesh.tests.mixed", check=False)
        self.assertEqual(
            teesh.CompletedProcess(
                cmd=("uv", "run", "-m", "teesh.tests.mixed"),
                returncode=42,
                stdout="hello world\nhave a nice day\nsay hello to your librarian\n",
                stderr="support your friendly neighborhood anti-fascist\ntrans rights are human rights\n",
            ),
            result,
        )
