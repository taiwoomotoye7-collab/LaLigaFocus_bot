from aiogram import Router, types
from aiogram.filters import Command
from services.la_liga_service import LaLigaService

router = Router()

@router.message(Command("fixtures"))
async def fixtures_command(message: types.Message):
    await message.answer("📅 Fetching upcoming fixtures...")
    
    fixtures_data = LaLigaService.get_fixtures()
    formatted = LaLigaService.format_fixtures(fixtures_data)
    
    await message.answer(formatted, parse_mode="HTML")
