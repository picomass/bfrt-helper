from bfrt_helper.fields import IPv4Address
from bfrt_helper.match import LPM
from bfrt_helper.match import Field
from bfrt_helper.util import InvalidValue

import pytest


class EightBit(Field):
    bitwidth = 8


def test_lpm_ipaddress_to_string():
    lpm = LPM(IPv4Address("192.168.0.0"), prefix=24)
    assert str(lpm) == "192.168.0.0/24"


def test_lpm_ipaddress_creates_correct_mask():
    lpm = LPM(IPv4Address("192.168.0.0"), prefix=24)
    expected_mask = IPv4Address("255.255.255.0")
    assert lpm.mask == expected_mask


def test_lpm_ipaddress_masks_value():
    lpm = LPM(IPv4Address("192.168.42.42"), prefix=16)
    expected_value = IPv4Address("192.168.0.0")
    assert lpm.value == expected_value


def test_lpm_is_subset_1():
    lpm_a = LPM(IPv4Address("192.168.42.0"), prefix=24)
    lpm_b = LPM(IPv4Address("192.168.0.0"), prefix=16)
    assert lpm_a < lpm_b
    assert lpm_b > lpm_a
    assert not lpm_a > lpm_b
    assert not lpm_b < lpm_a


def test_lpm_is_subset_2():
    lpm_a = LPM(IPv4Address("192.168.0.0"), prefix=24)
    lpm_b = LPM(IPv4Address("192.168.0.0"), prefix=16)
    assert lpm_a < lpm_b
    assert lpm_b > lpm_a
    assert not lpm_a > lpm_b
    assert not lpm_b < lpm_a


def test_lpm_equal_are_subset():
    lpm = LPM(IPv4Address("192.168.0.0"), prefix=24)
    assert lpm <= lpm
    assert lpm >= lpm


def test_lpm_equal_are_not_proper_subset():
    lpm = LPM(IPv4Address("192.168.0.0"), prefix=24)
    assert not lpm > lpm
    assert not lpm < lpm


def test_lpm_equal():
    lpm = LPM(IPv4Address("192.168.0.0"), prefix=24)
    assert lpm == lpm


def test_lpm_does_not_raise_with_maximum_prefix():
    try:
        LPM(EightBit(42), prefix=EightBit.bitwidth)
    except Exception:
        pytest.fail("Initialising PortId with prefix==bitwidth failed")


def test_lpm_raises_when_prefix_exceeds_maximum():
    with pytest.raises(InvalidValue):
        LPM(EightBit(42), prefix=EightBit.bitwidth + 1)
