from machine import Enigma
from components import Rotor, Reflector, Plugboard
from unittest.mock import patch, Mock
import pytest

# Enigma tests
@pytest.fixture()
def enigma():
    return Enigma()

def test_init(enigma):
    assert hasattr(enigma, "key")
    assert enigma.key == "AAA"

def test_init_invalid_key():
    with pytest.raises(ValueError):
        enigma = Enigma(key="")

def test_machine_repr(enigma):
    assert repr(enigma) == "Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II <-> Rotor  III <-> Reflector \nKey:  + AAA"

def test_encipher(enigma):
    assert enigma.encipher("TEST") == "OLPF"

def test_decipher(enigma):
    assert enigma.decipher("OLPF") == "TEST"

# Enigma encode_decode_letter:
def test_encode_decode_letter_invalid(enigma):
    with pytest.raises(ValueError):
        enigma.encode_decode_letter("")



# Rotor tests:
@pytest.fixture()
def rotor():
    return Rotor('I', 'A')

def test_rotor_no_input():
    with pytest.raises(ValueError):
        rotor = Rotor('', 'A')

def test_rotor_repr(rotor):
    assert repr(rotor) == "Wiring:\n{'forward': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'backward': 'UWYGADFPVZBECKMTHXSLRINQOJ'}\nWindow: A"


# Reflector tests
@pytest.fixture()
def reflector():
    return Reflector()

def test_reflector_repr(reflector):
    assert repr(reflector) == "Reflector wiring: \n{'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J', 'Y': 'A', 'Z': 'T'}"


# Plugboard tests
@pytest.fixture()
def plugboard():
    return Plugboard(['AB', 'CD'])

def test_plugboard_repr(plugboard):
    print(repr(plugboard))
    assert repr(plugboard) == "A <-> B\nC <-> D"

def test_plugboard_no_swaps():
    plugboard = Plugboard([])
    assert repr(plugboard) == ""