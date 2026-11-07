# module02_shell_navigation/tests/test_week4.py


def test_always_passes():
    assert 2 + 2 == 4


def test_string_is_lowercase():
    name = "ism3232"
    assert name == name.lower()


def test_path_segments():
    path = "/Users/yourname/ism3232/module02_shell_navigation"
    parts = path.split("/")
    assert "ism3232" in parts
