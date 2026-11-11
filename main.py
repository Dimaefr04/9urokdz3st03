from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="API каталога настольных игр")

class GameCreate(BaseModel):
    title: str
    genre: str
    players: int

class Game(BaseModel):
    id: int
    title: str
    genre: str
    players: int

games: list[Game] = [
    Game(id=1, title="Каркассон", genre="Стратегия", players=4),
    Game(id=2, title="Диксит", genre="Ассоциативная", players=6),
]

next_id = max((g.id for g in games), default=0) + 1

def find_game(game_id: int) -> Game:
    for game in games:
        if game.id == game_id:
            return game
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Игра с id={game_id} не найдена",
    )

@app.get("/games", response_model=list[Game])
def get_games():
    return games

@app.post("/games", response_model=Game, status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate):
    global next_id
    new_game = Game(id=next_id, **game.model_dump())
    next_id += 1
    games.append(new_game)
    return new_game

@app.put("/games/{game_id}", response_model=Game)
def update_game(game_id: int, game: GameCreate):
    existing = find_game(game_id)
    existing.title = game.title
    existing.genre = game.genre
    existing.players = game.players
    return existing

@app.delete("/games/{game_id}", response_model=Game)
def delete_game(game_id: int):
    game = find_game(game_id)
    games.remove(game)
    return game