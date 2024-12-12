import json
from collections import defaultdict

import typer

from app.heavy_api import get_exercise_templates

app = typer.Typer()

api_key_options = typer.Option(
    help="API key for the hevy api service.",
    prompt=True,
    envvar="HEVY_API_KEY",  # export HEVY_API_KEY="abcd"
)


@app.command()
def routines(
    api_key: str = api_key_options,
):

    typer.echo(f"API key: {api_key}")


@app.command()
def workouts(
    api_key: str = api_key_options,
):
    typer.echo(f"API key: {api_key}")


@app.command()
def exercise_templates(
    api_key: str = api_key_options,
):
    typer.echo(f"Fetching exercise templates")

    exercise_map = {}

    primary = set()
    secondary = set()
    primary_score = defaultdict(int)
    secondary_score = defaultdict(int)
    response = get_exercise_templates(api_key, page=1, page_size=100)
    while response:
        for exercise in response.exercise_templates:
            exercise_map[exercise.id] = exercise.title

            for muscle in exercise.secondary_muscle_groups:
                secondary.add(muscle)

            primary.add(exercise.primary_muscle_group)

        if response.page == response.page_count:
            break

        response = get_exercise_templates(api_key, page=response.page + 1, page_size=100)

    typer.echo(f"Found {len(exercise_map)} exercise templates")
    typer.echo(json.dumps(exercise_map))
    typer.echo(f"Primary muscle groups: {json.dumps({"primary":list(primary)})}")
    typer.echo(f"Secondary muscle groups: {json.dumps({"secondary":list(secondary)})}")
    typer.echo(f"Primary muscle group scores: {json.dumps(dict(primary_score))}")
    typer.echo(f"Secondary muscle group scores: {json.dumps(dict(secondary_score))}")


if __name__ == "__main__":
    app()


# For tick-tick

# "Upper Body Strength + Core Stability",
# "Lower Body Strength + Mobility",
# "Plyometrics + Agility + Core",
# "Rest or Active Recovery",
# "Upper Body Hypertrophy + Rotator Cuff + Neck",
# "Lower Body Hypertrophy + Adductors/Abductors",
# "Functional Training + Cardiovascular Endurance",
# "Rest or Active Recovery",
