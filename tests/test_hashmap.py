import pytest

from task1.hashmap import HashMap


@pytest.fixture
def hashmap():
    obj = HashMap()

    obj.put("1", "Ukraine")
    obj.put("2", "Britain")
    obj.put("3", "America")
    obj.put("4", "Italy")
    obj.put("5", "German")

    return obj


class TestHashmap:
    def test_get_retuns_value_for_passed_key(self, hashmap):
        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") == "Britain"
        assert hashmap.get("3") == "America"
        assert hashmap.get("4") == "Italy"
        assert hashmap.get("5") == "German"

    def test_get_returns_none_if_key_does_not_exist(self, hashmap):
        assert hashmap.get("non_existing_key") is None

    @pytest.mark.parametrize("key", [[], {}, set()])
    def test_get_returns_exception_if_key_is_not_hashable(self, key, hashmap):
        try:
            hashmap.get(key)
        except TypeError as e:
            assert str(e) == f"unhashable type: '{key.__class__.__name__}'"

    def test_put_creates_a_new_node_with_passed_value(self):
        hashmap = HashMap()

        assert hashmap.get("1") is None

        hashmap.put("1", "Ukraine")

        assert hashmap.get("1") == "Ukraine"

    def test_put_creates_a_new_node_with_passed_value_if_hashmap_size_equals_to_one(
        self,
    ):
        hashmap = HashMap(1)

        assert hashmap.get("1") is None
        assert hashmap.get("2") is None

        hashmap.put("1", "Ukraine")
        hashmap.put("2", "Britain")

        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") == "Britain"
        assert hashmap.table[0].value == "Ukraine"
        assert hashmap.table[0].next.value == "Britain"

    @pytest.mark.parametrize("key", [[], {}, set()])
    def test_put_returns_exception_if_key_is_not_hashable(self, key, hashmap):
        try:
            hashmap.put(key, "Ukraine")
        except TypeError as e:
            assert str(e) == f"unhashable type: '{key.__class__.__name__}'"

    def test_remove_removes_value_from_hashmap(self, hashmap):
        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") == "Britain"
        assert hashmap.get("3") == "America"
        assert hashmap.get("4") == "Italy"
        assert hashmap.get("5") == "German"

        hashmap.remove("2")
        hashmap.remove("4")

        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") is None
        assert hashmap.get("3") == "America"
        assert hashmap.get("4") is None
        assert hashmap.get("5") == "German"

    def test_remove_does_not_remove_anything_if_pass_key_does_not_exist(self, hashmap):
        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") == "Britain"
        assert hashmap.get("3") == "America"
        assert hashmap.get("4") == "Italy"
        assert hashmap.get("5") == "German"

        hashmap.remove("not_existing_key")

        assert hashmap.get("1") == "Ukraine"
        assert hashmap.get("2") == "Britain"
        assert hashmap.get("3") == "America"
        assert hashmap.get("4") == "Italy"
        assert hashmap.get("5") == "German"

    @pytest.mark.parametrize("key", [[], {}, set()])
    def test_remove_returns_exception_if_key_is_not_hashable(self, key, hashmap):
        try:
            hashmap.remove(key)
        except TypeError as e:
            assert str(e) == f"unhashable type: '{key.__class__.__name__}'"
