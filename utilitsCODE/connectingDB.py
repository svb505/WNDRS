from supabase import create_client, Client
from datetime import datetime

# === ⚙️ Настройки Supabase ===
url = "https://tfylhlgmpdaorbffspwv.supabase.co"      # ← вставь свой Project URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmeWxobGdtcGRhb3JiZmZzcHd2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2NzUwNDAsImV4cCI6MjA3NTI1MTA0MH0.2qbShwG1H1KV1WOKu_gVCNnDQltpqmazdgppT4pfXLw"                        # ← вставь свой anon key (НЕ service role!)
supabase: Client = create_client(url, key)

def save_score(player_name: str, score: int, game_name: str):
    timestamp = datetime.now().isoformat()

    data = {
        "name": player_name,
        "score": score,
        "game_name": game_name,
        "updated_at": timestamp
    }
    supabase.table("scores").insert(data).execute()
def get_top_scores(game_name: str, limit: int = 10):
    result = supabase.table("scores") \
        .select("name, score") \
        .eq("game_name", game_name) \
        .order("score", desc=True) \
        .limit(limit) \
        .execute()

    return result.data or []
def get_all_games():
    """
    Возвращает список всех игр, которые уже добавлены в таблицу.
    """
    result = supabase.table("scores") \
        .select("game_name") \
        .execute()

    games = sorted(list({row["game_name"] for row in result.data}))
    return games
def get_player_scores(player_name: str):
    """
    Возвращает результаты игрока по всем играм.
    """
    result = supabase.table("scores") \
        .select("game_name, score") \
        .eq("name", player_name) \
        .order("game_name", asc=True) \
        .execute()

    return result.data or []

"""# === 🧰 Пример использования ===
if __name__ == "__main__":
    # Примеры добавления результатов
    save_score("Alex", 120, "ball")
    save_score("Alex", 400, "snake")
    save_score("Nina", 800, "asteroids")

    print("🔥 Топ для 'ball':")
    print(get_top_scores("ball"))

    print("\n🎮 Все игры:")
    print(get_all_games())

    print("\n👤 Результаты Alex:")
    print(get_player_scores("Alex"))"""
