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
    with pytest.raises(ValueError):
        enigma = Enigma(key="")

def test_machine_repr(enigma):
    assert repr(enigma) == "Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II <-> Rotor  III <-> Reflector \nKey:  + AAA"

def test_encipher(enigma):
    assert enigma.encipher("TEST") == "OLPF"
    assert enigma.encipher("AAAA") == "OWCX"
    assert enigma.encipher("") == ""


def test_decipher(enigma):
    assert enigma.decipher("OLPF") == "TEST"
    assert enigma.encipher("AAAA") == "OWCX"
    assert enigma.encipher("") == ""

def test_encipher_decipher_equal(enigma):
    cipher = enigma.encipher("BBBBBB")
    print(cipher)
    enigma = Enigma()
    assert enigma.decipher(cipher) == "BBBBBB"
    enigma = Enigma()
    assert enigma.encipher(cipher) == "BBBBBB"

def test_encode_decode_letter(enigma):
    with pytest.raises(ValueError):
        enigma.encode_decode_letter("")
    with pytest.raises(ValueError):
        enigma.encode_decode_letter("LETTER")
    assert enigma.encode_decode_letter("A") == "B"

def test_encode_decode_plug_swaps():
    enigma = Enigma(swaps=['AC', 'BD'])
    assert enigma.encode_decode_letter("A") == "Q"
    enigma = Enigma(swaps=['AC', 'QD'])
    assert enigma.encode_decode_letter("A") == "D"

def test_set_rotor_positions(enigma):
    enigma.set_rotor_position("")
    assert enigma.l_rotor.window == "A" and enigma.m_rotor.window == "A" and enigma.r_rotor.window == "A"
    enigma.set_rotor_position("ZZZ", printIt=True)
    assert enigma.l_rotor.window == "Z" and enigma.m_rotor.window == "Z" and enigma.r_rotor.window == "Z"
    enigma.set_rotor_position("BBB")
    assert enigma.l_rotor.window == "B" and enigma.m_rotor.window == "B" and enigma.r_rotor.window == "B"

def test_set_plugs(enigma):
    enigma.set_plugs(['AB', 'CD'], printIt=True)
    assert enigma.plugboard.swaps == {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
    enigma.set_plugs(['EF', 'GH'])
    assert enigma.plugboard.swaps == {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C', 'E': 'F', 'F': 'E', 'G': 'H', 'H': 'G'}


# Rotor tests:
@pytest.fixture()
def rotor():
    return Rotor('I', 'A')

def test_rotor_no_input():
    with pytest.raises(ValueError):
        rotor = Rotor('', 'A')

def test_rotor_repr(rotor):
    assert repr(rotor) == "Wiring:\n{'forward': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'backward': 'UWYGADFPVZBECKMTHXSLRINQOJ'}\nWindow: A"

def test_rotor_step(rotor):
    rotor.step()
    assert rotor.window == "B"

def test_rotor_step_notch():
    second_rotor = Rotor("II", "A")
    rotor = Rotor("I", "Q", second_rotor)
    rotor.step()
    assert rotor.window == "R" and second_rotor.window == "B"

def test_rotor_doublestep():
    second_rotor = Rotor("II", "E")
    rotor = Rotor("I", "A", second_rotor, prev_rotor=None)
    rotor.step()
    assert rotor.window == "B" and second_rotor.window == "F"

def test_encode(rotor):
    rotor.encode_letter("A", return_letter=True, printit=True)

def test_encode_invalid_index(rotor):
    with pytest.raises(ValueError):
        rotor.encode_letter("1")

def test_change_setting(rotor):
    rotor.change_setting("B")
    assert rotor.window == "B"


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
    assert repr(plugboard) == "A <-> B\nC <-> D"

def test_plugboard_no_swaps():
    plugboard = Plugboard([])
    assert repr(plugboard) == ""

def test_update_swaps(plugboard):
    plugboard.update_swaps(['AB', 'XR'], replace=True)
    plugboard.update_swaps(['AB', 'XR'], replace=True)
    plugboard.update_swaps(['AB', 'XR', 'EF', 'GH', 'HI', 'JK', 'LM'], replace=False)
    plugboard.update_swaps(None)