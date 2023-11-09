import json
from math import sqrt

file = "journal.json"

def load_journal(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data


def compute_phi(file, event):
    journal_data = load_journal(file)

    n_11, n_00, n_10, n_01, n_plus_1, n_plus_0, n_plus, n_0_plus = (0, 0, 0, 0, 0, 0, 0, 0 )

    for item in journal_data:
        events = event in item["events"]
        squirrel_present = item["squirrel"]

        n_00 += not squirrel_present and not events
        n_01 += not squirrel_present and events
        n_10 += squirrel_present and not events
        n_11 += squirrel_present and events
        n_plus_1 += squirrel_present
        n_plus_0 += not squirrel_present
        n_plus += events
        n_0_plus += not events

    phi = (n_11 * n_00 - n_10 * n_01) / sqrt(n_plus_1 * n_plus_0 * n_0_plus * n_plus)
    return phi


def compute_correlations(file):
    journal_data = load_journal(file)
    correlations = {}

    for item in journal_data:
        events = item["events"]

        for event in events:
            if event not in correlations:
                correlations[event] = compute_phi(file, event)

    return correlations


def diagnose(file):
    correlations = compute_correlations(file)

    positive = negative = max_value = min_value = 0

    if correlations:
        first_event, first_correlation = list(correlations.items())[0]

        positive = negative = first_event
        max_value = min_value = first_correlation

        for event, correlation in correlations.items():
            if correlation > max_value:
                positive = event
                max_value = correlation

            if correlation < min_value:
                negative = event
                min_value = correlation

    return positive, negative

positive_correlation, negative_correlation = diagnose(file)

print("Hey Scott, avoid", positive_correlation)
print("To move against squirrel transformations keep up", negative_correlation)
