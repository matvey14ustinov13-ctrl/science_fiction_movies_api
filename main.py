"""API каталога фантастических фильмов."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="Science Fiction Movies API",
    description="API для просмотра и добавления фантастических фильмов.",
    version="1.0.0",
)


class MovieCreate(BaseModel):
    """Данные для добавления нового фильма."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        min_length=2,
        description="Название фильма (минимум 2 символа)",
        examples=["Интерстеллар"],
    )
    director: str = Field(
        min_length=2,
        description="Режиссёр фильма (минимум 2 символа)",
        examples=["Кристофер Нолан"],
    )
    year: int = Field(
        ge=1900,
        le=2030,
        description="Год выпуска фильма (от 1900 до 2030)",
        examples=[2014],
    )


class Movie(MovieCreate):
    """Фильм, хранящийся в каталоге."""

    id: int = Field(ge=1, description="Уникальный идентификатор фильма", examples=[1])


# Временное хранилище в памяти. При перезапуске сервера данные сбрасываются.
movies: list[Movie] = [
    Movie(id=1, title="Интерстеллар", director="Кристофер Нолан", year=2014),
    Movie(id=2, title="Матрица", director="Лана и Лилли Вачовски", year=1999),
    Movie(id=3, title="Дюна", director="Дени Вильнёв", year=2021),
]


@app.get("/movies", response_model=list[Movie], summary="Получить список фильмов")
def get_movies() -> list[Movie]:
    """Вернуть все фильмы каталога."""
    return movies


@app.get(
    "/movies/{movie_id}",
    response_model=Movie,
    summary="Получить фильм по id",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Фильм не найден"}},
)
def get_movie(movie_id: int) -> Movie:
    """Найти фильм по идентификатору или вернуть ошибку 404."""
    for movie in movies:
        if movie.id == movie_id:
            return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Фильм с id={movie_id} не найден",
    )


@app.post(
    "/movies",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить новый фильм",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Фильм с таким названием уже существует"
        }
    },
)
def create_movie(movie_data: MovieCreate) -> Movie:
    """Добавить фильм, если фильма с таким названием ещё нет."""
    normalized_title = movie_data.title.casefold()

    if any(movie.title.casefold() == normalized_title for movie in movies):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Фильм с названием «{movie_data.title}» уже существует",
        )

    new_movie = Movie(
        id=max((movie.id for movie in movies), default=0) + 1,
        **movie_data.model_dump(),
    )
    movies.append(new_movie)
    return new_movie
