from sports_skills_football_data import (
    get_current_season,
    get_season_standings,
    get_season_schedule,
    get_daily_schedule,
    get_event_summary
)

class LaLigaService:
    COMPETITION_ID = "la-liga"
    
    @staticmethod
    def _safe_call(func, *args, **kwargs):
        """Safely call sports-skills functions with error handling"""
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return None
    
    @staticmethod
    def get_current_season_id():
        """Get the current La Liga season ID"""
        result = LaLigaService._safe_call(
            get_current_season, 
            competition_id=LaLigaService.COMPETITION_ID
        )
        if result and isinstance(result, dict):
            return result.get("id")
        return None
    
    @staticmethod
    def get_standings():
        """Get current La Liga standings"""
        season_id = LaLigaService.get_current_season_id()
        if not season_id:
            return None
        result = LaLigaService._safe_call(
            get_season_standings, 
            season_id=season_id
        )
        return result
    
    @staticmethod
    def get_fixtures(limit=10):
        """Get upcoming La Liga fixtures"""
        season_id = LaLigaService.get_current_season_id()
        if not season_id:
            return None
        result = LaLigaService._safe_call(
            get_season_schedule, 
            season_id=season_id
        )
        if result and isinstance(result, list):
            return result[:limit]
        return None
    
    @staticmethod
    def get_daily_matches(date: str = None):
        """Get matches for a specific date"""
        import datetime
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        result = LaLigaService._safe_call(
            get_daily_schedule, 
            date=date
        )
        return result
    
    @staticmethod
    def format_standings(standings_data):
        """Format standings for Telegram message"""
        if not standings_data:
            return "⚠️ No standings data available."
        
        response = "🏆 <b>La Liga Standings</b>\n\n"
        
        # Handle different possible response formats
        if isinstance(standings_data, list):
            for i, team in enumerate(standings_data[:10], 1):
                name = team.get('name', 'Unknown')
                points = team.get('points', 0)
                response += f"{i}. {name} — {points} pts\n"
        elif isinstance(standings_data, dict):
            # Some APIs return dict with 'standings' key
            standings_list = standings_data.get('standings', [])
            if standings_list:
                for i, team in enumerate(standings_list[:10], 1):
                    name = team.get('name', 'Unknown')
                    points = team.get('points', 0)
                    response += f"{i}. {name} — {points} pts\n"
            else:
                response = "📊 Standings data unavailable at this time."
        else:
            response = "📊 Standings data unavailable at this time."
        
        return response
    
    @staticmethod
    def format_fixtures(fixtures_data):
        """Format fixtures for Telegram message"""
        if not fixtures_data:
            return "⚠️ No fixtures available."
        
        response = "📅 <b>Upcoming La Liga Fixtures</b>\n\n"
        
        if isinstance(fixtures_data, list):
            for match in fixtures_data:
                home = match.get('home_team', {}).get('name', 'Unknown')
                away = match.get('away_team', {}).get('name', 'Unknown')
                date = match.get('date', 'TBD')
                response += f"• {home} vs {away}\n  📅 {date}\n\n"
        else:
            response = "📅 Fixtures data unavailable at this time."
        
        return response
