import random
import datetime

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
        # Shuffle teams for variety
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
        
        # Sort by points descending
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
    def get_daily_matches(date: str = None):
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
