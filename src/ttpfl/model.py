import pulp

def run_model(expected_points, prices, tours, current_picks, already_picked):
    model = pulp.LpProblem("TTPFL", pulp.LpMaximize)

    num_players = len(expected_points)

    decisions = [
        pulp.LpVariable("x{}".format(i), cat=pulp.LpInteger, lowBound=0, upBound=1)
        for i in range(num_players)
    ]

    budget = 20000
    total_spend = 0
    for i in range(num_players):
        if i in current_picks:
            model += decisions[i] == 1, "Picked {}".format(i)
            total_spend += prices[i]

    model += sum(decisions[i] * expected_points[i] for i in range(num_players)), "Objective"

    model += sum(decisions[i] * prices[i] for i in range(num_players)) <= budget, "Budget"
    model += sum(decisions) == 10, "Team Size"

    for i in range(num_players):
        if i in already_picked:
            model += decisions[i] == 0, "Gone {}".format(i)

    model += sum(decisions[i] for i in range(num_players) if tours[i] == 'wta') == 5, "WTA"
    model += sum(decisions[i] for i in range(num_players) if tours[i] == 'atp') == 5, "ATP"

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    return budget - total_spend, decisions
