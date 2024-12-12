import hashlib
import json
import re
import uuid
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Set(BaseModel):
    type: str
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[int] = None


class Exercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[str] = None
    rest_seconds: Optional[int] = None
    notes: str
    sets: List[Set]


class Routine(BaseModel):
    title: str
    folder_id: Optional[str] = None
    notes: str
    exercises: List[Exercise]


class RoutineContainer(BaseModel):
    routine: Routine


class SampleExercise(BaseModel):
    exercise: str = Field(..., alias="Exercise")
    warmup_sets: int = Field(..., alias="WarmupSets")
    working_sets: int = Field(..., alias="WorkingSets")
    reps_duration: str = Field(..., alias="RepsDuration")
    rpe_percentage: str = Field(..., alias="RPE")
    rest: str = Field(..., alias="Rest")
    notes: str = Field(..., alias="Notes")


class Workout(BaseModel):
    workout: str = Field(..., alias="Workout")
    exercises: List[SampleExercise] = Field(..., alias="Exercises")


class SampleData(BaseModel):
    name: str
    workouts: List[Workout]


# Load the sample data
sample_data = {
    "name": "Week 1",
    "workouts": [
        {
            "Workout": "Lower #1",
            "Exercises": [
                {
                    "Exercise": "Back Squat",
                    "Warmup Sets": 3,
                    "Working Sets": 4,
                    "Reps/Duration": "4",
                    "RPE/%": "75%",
                    "Rest": "3-4 min",
                    "Notes": "Sit back and down, 15° toe flare, drive your knees out laterally",
                },
                {
                    "Exercise": "Eccentric-Accentuated Stiff-Leg Deadlift",
                    "Warmup Sets": 2,
                    "Working Sets": 3,
                    "Reps/Duration": "10",
                    "RPE/%": "7",
                    "Rest": "2-3 min",
                    "Notes": "4-second lowering phase. Keep your hips high",
                },
                {
                    "Exercise": "Dumbbell Walking Lunge",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15",
                    "RPE/%": "8",
                    "Rest": "2-3 min",
                    "Notes": "15 steps per leg",
                },
                {
                    "Exercise": "A1: Seated Leg Curl",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15",
                    "RPE/%": "9",
                    "Rest": "0 min",
                    "Notes": "Focus on squeezing your hamstrings",
                },
                {
                    "Exercise": "A2: Cable Pull-Through",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "Focus on squeezing your glutes",
                },
                {
                    "Exercise": "Eccentric-Accentuated/Constant-Tension Standing Calf Raise",
                    "Warmup Sets": 0,
                    "Working Sets": 4,
                    "Reps/Duration": "6/6",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "First 6 reps 3-second lowering phase, last 6 reps don't stop between reps",
                },
                {
                    "Exercise": "Cable Crunch",
                    "Warmup Sets": 0,
                    "Working Sets": 4,
                    "Reps/Duration": "30",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "Round your back as you crunch",
                },
            ],
        },
        {
            "Workout": "Upper #1",
            "Exercises": [
                {
                    "Exercise": "Barbell Bench Press",
                    "Warmup Sets": 3,
                    "Working Sets": 4,
                    "Reps/Duration": "6",
                    "RPE/%": "70%",
                    "Rest": "2-3 min",
                    "Notes": "Elbows at a 45° angle. Squeeze your shoulder blades and stay firm on the bench",
                },
                {
                    "Exercise": "Lat Pulldown",
                    "Warmup Sets": 2,
                    "Working Sets": 3,
                    "Reps/Duration": "10",
                    "RPE/%": "8",
                    "Rest": "2-3 min",
                    "Notes": "Pull your elbows down and in",
                },
                {
                    "Exercise": "Barbell Overhead Press",
                    "Warmup Sets": 2,
                    "Working Sets": 3,
                    "Reps/Duration": "10",
                    "RPE/%": "7",
                    "Rest": "2-3 min",
                    "Notes": "Squeeze your glutes to keep your torso upright",
                },
                {
                    "Exercise": "Seated T-Bar Row",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "12",
                    "RPE/%": "8",
                    "Rest": "2-3 min",
                    "Notes": "Squeeze shoulder blades together at the top, control the weight",
                },
                {
                    "Exercise": "Pause Dumbbell Incline Press",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "8",
                    "RPE/%": "7",
                    "Rest": "2-3 min",
                    "Notes": "3-second pause",
                },
                {
                    "Exercise": "Myo Reps Floor Skull Crusher",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "12",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "8 reps, rest 5 seconds, 2 reps, rest 5 seconds, 2 reps",
                },
                {
                    "Exercise": "Upper Body Weak Point 1",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15-20",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "Focus on mind-muscle connection",
                },
            ],
        },
        {
            "Workout": "Lower #2",
            "Exercises": [
                {
                    "Exercise": "Deadlift",
                    "Warmup Sets": 3,
                    "Working Sets": 2,
                    "Reps/Duration": "5",
                    "RPE/%": "80%",
                    "Rest": "3-5 min",
                    "Notes": "Brace your lats, chest tall, hips high, pull the slack out of the bar prior to moving it off the ground",
                },
                {
                    "Exercise": "Back Squat",
                    "Warmup Sets": 3,
                    "Working Sets": 3,
                    "Reps/Duration": "8",
                    "RPE/%": "70%",
                    "Rest": "3-4 min",
                    "Notes": "Sit back and down, 15° toe flare, drive your knees out laterally",
                },
                {
                    "Exercise": "Barbell Hip Thrust",
                    "Warmup Sets": 2,
                    "Working Sets": 4,
                    "Reps/Duration": "12",
                    "RPE/%": "8",
                    "Rest": "2-3 min",
                    "Notes": "Squeeze your glutes at the top",
                },
                {
                    "Exercise": "Unilateral Eccentric-Overloaded Leg Extension",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "12",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "12 reps each leg, bilateral concentric, unilateral eccentric",
                },
                {
                    "Exercise": "Constant-Tension Lying Leg Curl",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "20",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "Flex your hamstrings",
                },
                {
                    "Exercise": "Lower Body Weak Point 1",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15-20",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "Focus on mind-muscle connection",
                },
            ],
        },
        {
            "Workout": "Upper #2",
            "Exercises": [
                {
                    "Exercise": "Wide-Grip Pull-Up",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "6",
                    "RPE/%": "7",
                    "Rest": "2-3 min",
                    "Notes": "Pull your chest to the bar",
                },
                {
                    "Exercise": "Barbell Incline Press",
                    "Warmup Sets": 2,
                    "Working Sets": 4,
                    "Reps/Duration": "8",
                    "RPE/%": "7-8",
                    "Rest": "2-3 min",
                    "Notes": "Keep your elbows out",
                },
                {
                    "Exercise": "Pendlay Row/Barbell Bent Over Row",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "10/10",
                    "RPE/%": "8",
                    "Rest": "2-3 min",
                    "Notes": "10 reps pendlay row, 10 reps bent over row",
                },
                {
                    "Exercise": "A1: Cable Flye 21s",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "7/7/7",
                    "RPE/%": "8",
                    "Rest": "0 min",
                    "Notes": "7 reps top half of ROM, 7 reps bottom half ROM, 7 reps full ROM",
                },
                {
                    "Exercise": "A2: Face Pull",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "Focus on squeezing your shoulder blades together",
                },
                {
                    "Exercise": "Machine Lateral Raise",
                    "Warmup Sets": 1,
                    "Working Sets": 3,
                    "Reps/Duration": "12/12",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "Dropset",
                },
                {
                    "Exercise": "Supinated Dumbbell Curl",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15",
                    "RPE/%": "8",
                    "Rest": "1-2 min",
                    "Notes": "Supinate against the dumbbell",
                },
                {
                    "Exercise": "Upper Body Weak Point 1",
                    "Warmup Sets": 0,
                    "Working Sets": 3,
                    "Reps/Duration": "15-20",
                    "RPE/%": "9",
                    "Rest": "1-2 min",
                    "Notes": "Focus on mind-muscle connection",
                },
            ],
        },
    ],
}


def get_superset_id(label, superset_dict):
    if label in superset_dict:
        return superset_dict[label]
    else:
        # Generate a new superset ID
        superset_id = str(uuid.uuid4())
        superset_dict[label] = superset_id
        return superset_id


def generate_exercise_template_id(exercise_name):
    # Generate a unique ID based on the exercise name
    return hashlib.md5(exercise_name.encode("utf-8")).hexdigest().upper()[:8]


def parse_rest_seconds(rest_str):
    # rest_str example: "3-4 min", "1-2 min", "0 min", etc.
    if not rest_str:
        return None
    rest_str = rest_str.strip()
    if "min" in rest_str:
        rest_str = rest_str.replace("min", "").strip()
        if "-" in rest_str:
            parts = rest_str.split("-")
            min_rest = float(parts[0])
            max_rest = float(parts[1])
            avg_rest = (min_rest + max_rest) / 2
        else:
            avg_rest = float(rest_str)
        rest_seconds = int(avg_rest * 60)
        return rest_seconds
    elif "sec" in rest_str or "seconds" in rest_str:
        # Similar parsing for seconds
        rest_str = rest_str.replace("sec", "").replace("seconds", "").strip()
        if "-" in rest_str:
            parts = rest_str.split("-")
            min_rest = float(parts[0])
            max_rest = float(parts[1])
            avg_rest = (min_rest + max_rest) / 2
        else:
            avg_rest = float(rest_str)
        rest_seconds = int(avg_rest)
        return rest_seconds
    else:
        # Can't parse rest time
        return None


def parse_reps(reps_str):
    # reps_str examples: "4", "6/6", "15-20", "7/7/7", etc.
    if not reps_str:
        return None
    reps_str = reps_str.strip()
    if "-" in reps_str:
        parts = reps_str.split("-")
        min_reps = int(parts[0])
        max_reps = int(parts[1])
        avg_reps = (min_reps + max_reps) / 2
        return int(avg_reps)
    elif "/" in reps_str:
        # Handle multiple numbers separated by '/'
        parts = reps_str.split("/")
        reps_list = [int(part) for part in parts if part.isdigit()]
        total_reps = sum(reps_list)
        return total_reps
    else:
        # Single number
        if reps_str.isdigit():
            return int(reps_str)
        else:
            # Can't parse
            return None


routines = []

for week_name, workouts in sample_data.items():
    for workout in workouts:
        routine = Routine(
            title=workout["Workout"],
            folder_id=None,
            notes="",
            exercises=[],
        )

        exercises = workout["Exercises"]
        # Reset superset dictionary for each workout
        superset_dict = {}

        for ex in exercises:
            # Process each exercise
            exercise = {}
            exercise_name_full = ex["Exercise"]
            # Check for superset
            superset_match = re.match(r"([A-Z]\d+):\s*(.+)", exercise_name_full)
            if superset_match:
                superset_label = superset_match.group(1)
                exercise_name = superset_match.group(2)
                superset_id = get_superset_id(superset_label, superset_dict)
                exercise["superset_id"] = superset_id
            else:
                exercise_name = exercise_name_full
                exercise["superset_id"] = None

            exercise_obj = Exercise(
                exercise_template_id=generate_exercise_template_id(exercise_name),
                superset_id=exercise.get("superset_id", None),
                rest_seconds=parse_rest_seconds(ex.get("Rest", "")),
                notes=ex.get("Notes", ""),
                sets=[],
            )

            # Create sets
            warmup_sets = ex.get("Warmup Sets", 0)
            working_sets = ex.get("Working Sets", 0)
            reps = ex.get("Reps/Duration", "")
            reps_value = parse_reps(reps)

            for i in range(warmup_sets):
                set = {}
                set["type"] = "warmup"
                set["weight_kg"] = None
                set["reps"] = reps_value
                set["distance_meters"] = None
                set["duration_seconds"] = None
                exercise["sets"].append(set)
            for i in range(working_sets):
                set = {}
                set["type"] = "normal"
                set["weight_kg"] = None
                set["reps"] = reps_value
                set["distance_meters"] = None
                set["duration_seconds"] = None
                exercise["sets"].append(set)

            # Add the exercise to the routine
            routine.exercises.append(exercise)

        # Add the routine to routines list
        routines.append({"routine": routine})

# Output the routines
print(json.dumps(routines, indent=2))
