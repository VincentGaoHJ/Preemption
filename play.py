def play(prov, your_castle, computer_castle, rules):
    candidates = {}
    for i in prov:
        if i not in your_castle:
            if i not in computer_castle:
                candidates[i] = 0
    for rule in rules:
        if rule[0] in candidates:
            candidates[rule[0]] += 1

    return sorted(candidates, key=lambda x: candidates[x])[-1]
