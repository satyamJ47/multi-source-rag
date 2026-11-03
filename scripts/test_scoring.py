from scripts.run_eval_vector import score

names = {"Alex", "Ian", "Brian", "Julia"}

cases = [
    (["Ian"], "The lowest is Ian with 70.", (True, True)),
    (["Ian"], "Brian has 78 and Ian has 70.", (True, False)),   # Brian is an extra wrong name
    (["Alex", "Ian"], "Alex scored 70.", (False, False)),       # Ian is missing
    (["Ian"], "Brian scored 78.", (False, False)),              # "Ian" must not match inside "Brian"
    ([83.8], "The average is 83.8.", (True, True)),
    ([83.8], "The average is about 84.", (False, False)),
    (["CANNOT_ANSWER"], "I don't have enough information.", (True, True)),
]

for expected, answer, want in cases:
    got = score(expected, answer, names)
    print("OK " if got == want else "BAD", expected, "|", answer, "|", got)