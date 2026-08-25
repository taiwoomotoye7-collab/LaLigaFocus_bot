from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("players"))
async def players_command(message: types.Message):
    players_content = (
        "👤 <b>La Liga Player Profiles</b>\n\n"
        "In-depth analysis of La Liga stars:\n\n"
        "📌 <b>What we cover:</b>\n"
        "• Player biographies & career history\n"
        "• Performance statistics & metrics\n"
        "• Playing style & role analysis\n"
        "• Transfer history & market value\n\n"
        "⭐ <i>Coming soon: Detailed player profiles!</i>"
    )
    await message.answer(players_content)
