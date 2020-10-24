from rules import apply_modifier, apply_modifiers


def test_apply_modifier():
    # check each operator works
    assert apply_modifier(1, ('+', 1)) == 2
    assert apply_modifier(1, ('-', 1)) == 0
    assert apply_modifier(1, ('*', 2)) == 2
    assert apply_modifier(1, ('/', 2)) == 0.5


def test_apply_modifiers():
    # check they are sorted by operator
    assert apply_modifiers(1, [('/', 2), ('*', 3)]) == apply_modifiers(1, [('*', 3), ('/', 2)])
    # check it rounds up result
    assert apply_modifiers(1, [('/', 2), ('*', 3)]) == '2'
    # check min works
    assert apply_modifiers(1, [('/', 2)]) == '1'
    # check multiple of the same operation works
    assert apply_modifiers(1, [('+', 1), ('+', 1), ('+', 1)]) == '4'
