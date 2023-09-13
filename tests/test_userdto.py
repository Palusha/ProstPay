from datetime import datetime

import pytest
from freezegun import freeze_time
from unittest.mock import AsyncMock, MagicMock

from task2.userdto import User, UserDTO, UserManager


@pytest.fixture
def user_manager():
    return UserManager()


@pytest.fixture
@freeze_time("2000-01-01")
def user():
    return User(
        id=1,
        firstname="John",
        lastname="Ash",
        username="johna",
        create_date=datetime.now(),
    )


@pytest.fixture
def async_session_mock(mocker):
    session_mock = MagicMock()
    mocker.patch(
        "task2.userdto.get_async_session",
        return_value=session_mock,
        create=True,
    )
    return session_mock


@pytest.fixture
def scalar_one_or_none_mock(async_session_mock):
    aenter_mock = async_session_mock.__aenter__.return_value = AsyncMock()
    execute_mock = aenter_mock.execute.return_value = MagicMock()
    return execute_mock.scalar_one_or_none


class TestUserManager:
    @pytest.mark.asyncio
    @freeze_time("2000-01-01")
    async def test_get_returns_a_user(
        self, scalar_one_or_none_mock, user, user_manager
    ):
        scalar_one_or_none_mock.return_value = user

        user = await user_manager.get(1)

        scalar_one_or_none_mock.assert_called_once()
        assert user.id == 1
        assert user.firstname == "John"
        assert user.lastname == "Ash"
        assert user.username == "johna"
        assert user.create_date == datetime.now()

    @pytest.mark.asyncio
    async def test_get_raises_an_validation_error_if_user_is_none(
        self, scalar_one_or_none_mock, user_manager
    ):
        scalar_one_or_none_mock.return_value = None
        try:
            user = await user_manager.get(1)
        except ValueError as e:
            assert "input_type=NoneType" in str(e)

        scalar_one_or_none_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_calls_session_add_function_with_passed_user(
        self, async_session_mock, user_manager
    ):
        aenter_mock = async_session_mock.__aenter__.return_value = AsyncMock()
        add_mock = aenter_mock.add

        user = UserDTO(
            id=1, firstname="Pavlo", lastname="Andrushkiv", username="palushka"
        )
        await user_manager.add(user)

        add_mock.assert_called_once()
        assert len(add_mock.call_args) == 2
        assert isinstance(add_mock.call_args.args[0], User)
