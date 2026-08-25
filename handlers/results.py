from aiogram import Router, types
from aiogram.filters import Command
from services.la_liga_service import LaLigaService

router = Router()

@router.message(Command("results"))
async def results_command(message: types.Message):
    await message.answer("⚽ Fetching recent results...")
    
    # Try to get daily matches
    matches = LaLigaService.get_daily_matches()
    
    if matches:
        response = "📊 <b>Recent La Liga Results</b>\n\n"
        if isinstance(matches, list):
            for match in matches:
                home = match.get('home_team', {}).get('name', 'Unknown')
                away = match.get('away_team', {}).get('name', 'Unknown')
                score = match.get('score', 'TBD')
                response += f"• {home} {score} {away}\n"
        else:
            response = "⚽ No recent results available."
    else:
        response = "⚽ No recent results available."
    
    await message.answer(response)
