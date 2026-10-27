def generate_plan(subjects, difficulties, hours, days):
    weights = {"Easy": 1, "Medium": 2, "Hard": 3}
    total_minutes = int(hours * 60)
    result = []

    for day in range(1, days + 1):
        ordered = subjects[(day - 1) % len(subjects):] + \
                  subjects[:(day - 1) % len(subjects)]

        active = ordered[:min(len(ordered), total_minutes)]
        subject_weights = [
            weights[difficulties[s]] for s in active
        ]
        total_weight = sum(subject_weights)

        allocations = [
            total_minutes * w // total_weight
            for w in subject_weights
        ]

        remaining = total_minutes - sum(allocations)
        for i in range(remaining):
            allocations[i % len(allocations)] += 1

        for subject, minutes in zip(active, allocations):
            result.append({
                "Day": day,
                "Subject": subject,
                "Difficulty": difficulties[subject],
                "Minutes": minutes,
                "Completed": False
            })

    return result