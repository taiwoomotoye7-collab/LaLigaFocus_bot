from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("finances"))
async def finances_command(message: types.Message):
    finances_content = (
        "💰 <b>La Liga Club Finances</b>\n\n"
        "Financial insights from Spanish football:\n\n"
        "📌 <b>What we analyze:</b>\n"
        "• Transfer budgets & spending patterns\n"
        "• Wage structures & contract insights\n"
        "• Revenue streams & sponsorship deals\n"
        "• Debt analysis & financial regulations\n\n"
        "📊 <i>Coming soon: Detailed club financial breakdowns!</i>"
    )
    await message.answer(finances_content)
