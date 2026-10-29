
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


@pytest.mark.parametrize("service,duration,level,member,expected", [
    ("unknown", 10, "junior", False, "unknown service"),
    ("haircut", -1, "junior", False, "invalid duration"),
])
def test_invalid_inputs(service, duration, level, member, expected):
    with pytest.raises(ValueError, match=expected):
        extra_time_charge(service, duration, level, member)


@pytest.mark.parametrize("service,duration,level,member,expected", [
    ("haircut", 30, "junior", False, 0),
    ("haircut", 45, "junior", True, 0),
    ("spa", 100, "junior", True, 100),
    ("colour", 70, "junior", False, 100),
    ("haircut", 40, "senior", False, 180),
    ("haircut", 100, "junior", False, 1260),
    ("haircut", 100, "senior", False, 2100),
])
def test_extra_time_branches(service, duration, level, member, expected):
    assert extra_time_charge(service, duration, level, member) == expected


@pytest.mark.parametrize("party,services,walkin,expected", [
    (2, 5, True, True),
    (3, 1, True, False),
    (5, 1, False, False),
    (4, 2, False, True),
    (4, 3, False, False),
])
def test_booking_branches(party, services, walkin, expected):
    assert can_book(party, services, walkin) is expected


@pytest.mark.parametrize("minutes,colour,weekend,expected", [
    (10, True, False, "open"),
    (9, True, False, "late"),
    (-6, True, False, "closed"),
    (5, False, False, "open"),
    (4, False, False, "late"),
    (-11, False, False, "closed"),
    (20, True, True, "open"),
    (6, True, True, "late"),
    (4, True, True, "closed"),
])
def test_arrival_branches(minutes, colour, weekend, expected):
    assert arrival_status(minutes, colour, weekend) == expected
