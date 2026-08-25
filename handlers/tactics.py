from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("tactics"))
async def tactics_command(message: types.Message):
    tactics_content = (
        "⚽ <b>La Liga Tactical Focus</b>\n\n"
        "Deep dive into Spanish football tactics:\n\n"
        "📌 <b>Key Topics:</b>\n"
        "• Pressing patterns & high defensive lines\n"
        "• Positional play & attacking structures\n"
        "• Set-piece routines & defensive organization\n"
        "• Managerial strategies & in-game adjustments\n\n"
        "🔍 <i>Coming soon: Detailed match-by-match tactical breakdowns!</i>"
    )
    await message.answer(tactics_content)
