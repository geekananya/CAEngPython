from unittest.mock import Mock
import pytest
from shopping_cart import ShoppingCart
from item_database import ItemDatabase

# fixtures initialize test functions to increase consistency and repeatability
@pytest.fixture
def cart():
    return ShoppingCart(5)


def test_add_to_cart(cart):
    cart.add("apple")
    assert cart.size() == 1


def test_contains_item(cart):
    cart.add("apple")
    assert "apple" in cart.get_items()

@pytest.mark.maxItemsTest
def test_max_items_exception(cart):
    for _ in range(5):
        cart.add("apple")

    with pytest.raises(OverflowError):
        cart.add("apple")


# give mock value to database dependency
def test_total_price_mock(cart):
    cart.add("apple")
    cart.add("orange")
    item_database = ItemDatabase()

    def mock_get_item(item: str):
        if item == "apple":
            return 1.0
        if item == "orange":
            return 2.0

    item_database.get = Mock(side_effect=mock_get_item)     # forces a behavior on outside dependencies that we cant control (to pass the test case)
    assert cart.get_total_price(item_database) == 3.0


# run tests for different values of price_map
@pytest.mark.parametrize("price_map,expected_total", [
    ({"apple": 1.0, "banana": 0.5, "orange": 0.75}, 2.25),
    ({"apple": 1.0, "banana": 1.0, "orange": 2.5}, 4.5),  # Total for one apple and one orange
    ({"apple": 1.5, "banana": 1.5, "orange": 0.5}, 3.5),  # Total for one banana and one orange
])
def test_get_total_price_parametrized(cart, price_map, expected_total):
    cart.add("apple")
    cart.add("banana")
    cart.add("orange")

    total_price = cart.get_total_price(price_map)
    assert total_price == expected_total