import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 30, "junior", False)


def test_extra_time_charge_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_haircut_within_included_time():
    assert extra_time_charge("haircut", 30, "junior", False) == 0


def test_member_gets_extra_included_time():
    assert extra_time_charge("haircut", 40, "junior", True) == 0


def test_colour_nonmember_extra_time_junior_rate():
    assert extra_time_charge("colour", 70, "junior", False) == 100


def test_spa_member_does_not_get_extra_included_time():
    assert extra_time_charge("spa", 100, "junior", True) == 100


def test_non_junior_uses_standard_nonjunior_rate():
    assert extra_time_charge("haircut", 40, "senior", False) == 180


def test_long_extra_time_surcharge_for_senior():
    assert extra_time_charge("haircut", 100, "senior", False) == 2100


def test_walkin_booking_for_two_people():
    assert can_book(2, 5, True) is True


def test_walkin_booking_for_more_than_two_people_rejected():
    assert can_book(3, 1, True) is False


def test_non_walkin_booking_party_over_four_rejected():
    assert can_book(5, 1, False) is False


def test_non_walkin_booking_two_services_allowed():
    assert can_book(4, 2, False) is True


def test_non_walkin_booking_over_two_services_rejected():
    assert can_book(4, 3, False) is False


def test_arrival_open_for_colour_on_weekend_at_cutoff():
    assert arrival_status(20, True, True) == "open"


def test_arrival_late_on_weekend_for_colour():
    assert arrival_status(6, True, True) == "late"


def test_arrival_closed_for_weekend_colour_early_arrival():
    assert arrival_status(4, True, True) == "closed"