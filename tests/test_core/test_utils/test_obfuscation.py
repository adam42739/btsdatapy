from src.btsdatapy.core.utils.obfuscation import rot13


def test_rot13():
    assert rot13("Hello World!") == "Uryyb Jbeyq!"
