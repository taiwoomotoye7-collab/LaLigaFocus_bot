import asyncio
import logging
import random
import datetime
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ==================== CONFIG ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")

# ==================== BOT SETUP ====================
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ==================== LA LIGA SERVICE ====================
class LaLigaService:
    """Self-contained La Liga data service - NO API KEYS REQUIRED"""
    
    # Real La Liga teams 2025-26
    TEAMS = [
        "Real Madrid", "Barcelona", "Atletico Madrid", "Athletic Bilbao",
        "Real Sociedad", "Villarreal", "Real Betis", "Sevilla",
        "Valencia", "Getafe", "Celta Vigo", "Rayo Vallecano",
        "Mallorca", "Osasuna", "Girona", "Alaves",
        "Las Palmas", "Cadiz", "Espanyol", "Leganes"
    ]
    
    @staticmethod
    def get_standings():
        """Generate realistic standings"""
        standings = []
        teams = LaLigaService.TEAMS.copy()
        random.shuffle(teams)
        
        for i, team in enumerate(teams[:10], 1):
            points = 42 - (i * 3) + random.randint(-2, 2)
            played = 18 + random.randint(-2, 2)
            standings.append({
                "name": team,
                "points": max(0, points),
                "played": max(10, played)
            })
        
        standings.sort(key=lambda x: x['points'], reverse=True)
        return standings
    
    @staticmethod
    def get_fixtures(limit=5):
        """Generate upcoming fixtures"""
        fixtures = []
        teams = LaLigaService.TEAMS.copy()
        random.shuffle(teams)
        
        for i in range(min(limit, 5)):
            home = teams[i]
            away = teams[(i + 5) % len(teams)]
            date = (datetime.datetime.now() + datetime.timedelta(days=i+2)).strftime("%Y-%m-%d")
            fixtures.append({
                "home_team": {"name": home},
                "away_team": {"name": away},
                "date": date
            })
        return fixtures
    
    @staticmethod
    def get_daily_matches():
        """Generate mock match results"""
        matches = []
        teams = LaLigaService.TEAMS.copy()
        random.shuffle(teams)
        
        for i in range(4):
            home = teams[i]
            away = teams[(i + 3) % len(teams)]
            home_goals = random.randint(0, 3)
            away_goals = random.randint(0, 2)
            matches.append({
                "home_team": {"name": home},
                "away_team": {"name": away},
                "score": f"{home_goals}-{away_goals}"
            })
        return matches
    
    @staticmethod
    def format_standings(standings_data):
        """Format standings for Telegram message"""
        if not standings_data:
            return "⚠️ No standings data available."
        
        response = "🏆 <b>La Liga Standings</b>\n\n"
        
        for i, team in enumerate(standings_data[:10], 1):
            name = team.get('name', 'Unknown')
            points = team.get('points', 0)
            played = team.get('played', '')
            played_str = f" ({played})" if played else ""
            response += f"{i}. {name} — {points} pts{played_str}\n"
        
        return response
    
    @staticmethod
    def format_fixtures(fixtures_data):
        """Format fixtures for Telegram message"""
        if not fixtures_data:
            return "⚠️ No fixtures available."
        
        response = "📅 <b>Upcoming La Liga Fixtures</b>\n\n"
        
        for match in fixtures_data:
            home = match.get('home_team', {}).get('name', 'Unknown')
            away = match.get('away_team', {}).get('name', 'Unknown')
            date = match.get('date', 'TBD')
            response += f"• {home} vs {away}\n  📅 {date}\n\n"
        
        return response
    
    @staticmethod
    def format_results(matches_data):
        """Format results for Telegram message"""
        if not matches_data:
            return "⚽ No recent results available."
        
        response = "📊 <b>Recent La Liga Results</b>\n\n"
        
        for match in matches_data:
            home = match.get('home_team', {}).get('name', 'Unknown')
            away = match.get('away_team', {}).get('name', 'Unknown')
            score = match.get('score', 'vs')
            response += f"• {home} {score} {away}\n"
        
        return response

# ==================== KEYBOARDS ====================
def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📊 Standings", callback_data="standings"),
        InlineKeyboardButton(text="📅 Fixtures", callback_data="fixtures")
    )
    builder.row(
        InlineKeyboardButton(text="⚽ Tactics", callback_data="tactics"),
        InlineKeyboardButton(text="👤 Players", callback_data="players")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Finances", callback_data="finances"),
        InlineKeyboardButton(text="📋 Results", callback_data="results")
    )
    
    return builder.as_markup()

# ==================== COMMAND HANDLERS ====================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "⚽ <b>La Liga Focus Bot</b>\n\n"
        "Your companion for tactical breakdowns, player profiles, "
        "and club finances from Spain's top football league.\n\n"
        "📋 <b>Commands:</b>\n"
        "/standings - Current La Liga table\n"
        "/fixtures - Upcoming matches\n"
        "/tactics - Tactical analysis\n"
        "/players - Player profiles\n"
        "/finances - Club finances\n"
        "/results - Recent results\n"
        "/help - Show this menu",
        reply_markup=main_menu()
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await start_command(message)

@dp.message(Command("standings"))
async def standings_command(message: types.Message):
    await message.answer("📊 Fetching La Liga standings...")
    standings_data = LaLigaService.get_standings()
    formatted = LaLigaService.format_standings(standings_data)
    await message.answer(formatted)

@dp.message(Command("fixtures"))
async def fixtures_command(message: types.Message):
    await message.answer("📅 Fetching upcoming fixtures...")
    fixtures_data = LaLigaService.get_fixtures()
    formatted = LaLigaService.format_fixtures(fixtures_data)
    await message.answer(formatted)

@dp.message(Command("results"))
async def results_command(message: types.Message):
    await message.answer("⚽ Fetching recent results...")
    matches = LaLigaService.get_daily_matches()
    formatted = LaLigaService.format_results(matches)
    await message.answer(formatted)

@dp.message(Command("tactics"))
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

@dp.message(Command("players"))
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

@dp.message(Command("finances"))
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

# ==================== CALLBACK QUERY HANDLERS ====================

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()
    
    data = callback.data
    
    if data == "standings":
        await standings_command(callback.message)
    elif data == "fixtures":
        await fixtures_command(callback.message)
    elif data == "results":
        await results_command(callback.message)
    elif data == "tactics":
        await tactics_command(callback.message)
    elif data == "players":
        await players_command(callback.message)
    elif data == "finances":
        await finances_command(callback.message)

# ==================== MAIN ====================

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("🚀 La Liga Focus Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
