from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
