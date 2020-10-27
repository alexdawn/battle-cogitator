from unit import Model, ModelStats, DamageTable


def test_model():
    """Test the model's damage table is applied properly"""
    model = Model(
        ModelStats("foo", 6, 4, 4, 4, 4, 5, 1, 8, 4),
        [
            DamageTable(3, 5, {"movement": 6, "ballistic_skill": 4}),
            DamageTable(1, 2, {"movement": 4, "ballistic_skill": 3})
        ], [], [], []
    )
    assert model.model.movement == 6
    assert model.model.ballistic_skill == 4
    model.apply_damage(0)
    assert model.model.movement == 6
    assert model.model.ballistic_skill == 4
    model.apply_damage(1)
    assert model.model.movement == 6
    assert model.model.ballistic_skill == 4
    model.apply_damage(3)
    assert model.model.wounds == 1
    assert model.model.movement == 4
    assert model.model.ballistic_skill == 3
