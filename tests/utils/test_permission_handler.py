import pytest
from unittest.mock import AsyncMock, MagicMock
from utils.permission_handler import PermissionHandler

@pytest.fixture
def ctx():
    c = MagicMock()
    c.send = AsyncMock()
    c.author = MagicMock()
    c.voice_client = None
    return c

@pytest.mark.asyncio
async def test_user_not_in_voice(ctx):
    ctx.author.voice = None  # * none user in a voice channel

    result = await PermissionHandler.check_user_in_voice(ctx)

    assert result is False
    ctx.send.assert_awaited_once()
    args, kwargs = ctx.send.await_args
    embed = kwargs["embed"]
    assert "No estás en un canal de voz" in embed.title
    assert "Unete a un canal de voz pibe" in embed.description


@pytest.mark.asyncio
async def test_user_in_voice(ctx):
    channel = MagicMock()
    ctx.author.voice = MagicMock(channel=channel)  # usuario en canal

    result = await PermissionHandler.check_user_in_voice(ctx)

    assert result is True
    ctx.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_bot_not_in_voice(ctx):
    ctx.voice_client = None  # bot no está en canal

    result = await PermissionHandler.check_bot_in_voice(ctx)

    assert result is False
    ctx.send.assert_awaited_once()


@pytest.mark.asyncio
async def test_bot_in_voice(ctx):
    channel = MagicMock()
    ctx.voice_client = MagicMock(channel=channel)

    result = await PermissionHandler.check_bot_in_voice(ctx)

    assert result is True
    ctx.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_both_in_voice(ctx):
    channel = MagicMock()
    ctx.author.voice = MagicMock(channel=channel)
    ctx.voice_client = MagicMock(channel=channel)

    result = await PermissionHandler.check_both_in_voice(ctx)

    assert result is True


@pytest.mark.asyncio
async def test_not_in_same_channel(ctx):
    user_channel = MagicMock()
    bot_channel = MagicMock()
    ctx.author.voice = MagicMock(channel=user_channel)
    ctx.voice_client = MagicMock(channel=bot_channel)

    result = await PermissionHandler.check_same_in_voice(ctx)

    assert result is False
    ctx.send.assert_awaited_once()
    args, kwargs = ctx.send.await_args
    embed = kwargs["embed"]
    assert "no estamos en el mismo canal" in embed.title