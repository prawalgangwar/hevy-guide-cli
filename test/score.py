import json
from collections import defaultdict

primary_scores = {
    "other": 16,
    "cardio": 14,
    "full_body": 12,
    "abdominals": 11,
    "hamstrings": 9,
    "shoulders": 8,
    "quadriceps": 8,
    "chest": 5,
    "glutes": 5,
    "biceps": 4,
    "neck": 4,
    "upper_back": 4,
    "calves": 4,
    "lats": 3,
    "forearms": 2,
    "traps": 2,
    "triceps": 2,
}
secondary_scores = {
    "triceps": 7,
    "shoulders": 7,
    "hamstrings": 6,
    "glutes": 13,
    "calves": 2,
    "quadriceps": 2,
    "lower_back": 2,
    "upper_back": 3,
    "forearms": 2,
    "neck": 2,
}

primary = [
    "lats",
    "forearms",
    "neck",
    "traps",
    "upper_back",
    "chest",
    "other",
    "abdominals",
    "full_body",
    "lower_back",
    "triceps",
    "shoulders",
    "calves",
    "quadriceps",
    "cardio",
    "biceps",
    "glutes",
    "hamstrings",
    "adductors",
    "abductors",
]
secondary = [
    "quadriceps",
    "lower_back",
    "chest",
    "lats",
    "biceps",
    "forearms",
    "neck",
    "triceps",
    "abdominals",
    "traps",
    "shoulders",
    "calves",
    "glutes",
    "hamstrings",
    "upper_back",
]

# merge primary and secondary scores but secondary scores are half as important if a muscle is not present in either score it zero

final_score = defaultdict(float)
for muscle in primary:
    final_score[muscle] = primary_scores.get(muscle, 0) + secondary_scores.get(muscle, 0) / 2

# sort the final score
sorted_final_score = dict(sorted(final_score.items(), key=lambda x: x[1], reverse=True))

print(json.dumps(sorted_final_score, indent=4))
