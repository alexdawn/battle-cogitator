from deployment import make_unit_from_bs, resolve_links, remove_empty_links
from stratgey import Strategy

example_json = {
    "c353-858f-36ed-23d4": {
            "primary_category": "",
            "id": "c353-858f-36ed-23d4",
            "name": "Guardian Defenders",
            "target_type": "selectionEntry",
            "link_target": {
                "type": "unit",
                "primary_category": "Troops",
                "id": "0341-e29a-e0ec-acd4",
                "name": "Guardian Defenders",
                "info_links": {},
                "selection_entries": {
                    "8cb4-c382-d67e-3d08": {
                        "type": "upgrade",
                        "primary_category": "",
                        "id": "8cb4-c382-d67e-3d08",
                        "name": "Guardian Heavy Weapons Platform",
                        "comment": "",
                        "modifiers": [],
                        "modifier_groups": [],
                        "constraints": [],
                        "profiles": [
                            {
                                "profile_type": "Unit",
                                "name": "Guardian Heavy Weapons Platform",
                                "M": "7\"",
                                "WS": "6+",
                                "BS": "3+",
                                "S": "3",
                                "T": "3",
                                "W": "2",
                                "A": "1",
                                "Ld": "7",
                                "Save": "3+"
                            },
                            {
                                "profile_type": "Abilities",
                                "name": "Crewed Weapon",
                                "Description": "A Heavy Weapon Platform can only fire its ranged weapon if a Guardian from this unit is within 3\" and 'fires' it instead of shooting any of their own weapons. A single Guardian cannot operate multiple Heavy Weapon Platforms in this way in a single turn."
                            },
                            {
                                "profile_type": "Keywords",
                                "name": "Heavy Weapon Platform - Keywords",
                                "Keywords (Faction)": "Aeldari, Asuryani, Warhost, <CRAFTWORLD>",
                                "Keywords (Basic)": "Infantry, Artillery, Guardian, Heavy Weapons Platform"
                            }
                        ],
                        "rules": [],
                        "info_groups": [],
                        "info_links": {},
                        "selection_entries": {},
                        "selection_entry_groups": {},
                        "entry_links": {
                            "994d-77a0-41df-a797": {
                                "primary_category": "",
                                "id": "994d-77a0-41df-a797",
                                "name": "Heavy Weapons",
                                "comment": "",
                                "modifiers": [],
                                "modifier_groups": [],
                                "constraints": [],
                                "profiles": [],
                                "rules": [],
                                "info_groups": [],
                                "info_links": {},
                                "selection_entries": {},
                                "selection_entry_groups": {},
                                "entry_links": {},
                                "category_links": [],
                                "costs": {},
                                "target_type": "selectionEntryGroup",
                                "link_target": {
                                    "primary_category": "",
                                    "id": "7d84-2892-c4e1-b2a1",
                                    "name": "Heavy Weapons",
                                    "comment": "",
                                    "modifiers": [],
                                    "modifier_groups": [],
                                    "constraints": [],
                                    "profiles": [],
                                    "rules": [],
                                    "info_groups": [],
                                    "info_links": {},
                                    "selection_entries": {},
                                    "selection_entry_groups": {},
                                    "entry_links": {
                                        "1bbf-a8ef-2873-cad2": {
                                            "primary_category": "",
                                            "id": "1bbf-a8ef-2873-cad2",
                                            "name": "Aeldari Missile Launcher",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "constraints": [],
                                            "profiles": [],
                                            "rules": [],
                                            "info_groups": [],
                                            "info_links": {},
                                            "selection_entries": {},
                                            "selection_entry_groups": {},
                                            "entry_links": {},
                                            "category_links": [],
                                            "costs": {},
                                            "target_type": "selectionEntry",
                                            "link_target": {
                                                "type": "upgrade",
                                                "primary_category": "",
                                                "id": "5f31-e870-f91d-1162",
                                                "name": "Aeldari Missile Launcher",
                                                "comment": "",
                                                "modifiers": [],
                                                "modifier_groups": [],
                                                "constraints": [],
                                                "profiles": [],
                                                "rules": [],
                                                "info_groups": [],
                                                "info_links": {
                                                    "71b6-5768-5adc-bdcd": {
                                                        "target_type": "profile",
                                                        "id": "71b6-5768-5adc-bdcd",
                                                        "name": "",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "(AML) Starshot Missile",
                                                            "Range": "48\"",
                                                            "Type": "Heavy 1",
                                                            "S": "8",
                                                            "AP": "-2",
                                                            "D": "D6",
                                                            "Abilities": "-"
                                                        }
                                                    },
                                                    "0745-a663-5889-8775": {
                                                        "target_type": "profile",
                                                        "id": "0745-a663-5889-8775",
                                                        "name": "(AML) Sunburst Missile",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "(AML) Sunburst Missile",
                                                            "Range": "48\"",
                                                            "Type": "Heavy D6",
                                                            "S": "4",
                                                            "AP": "-1",
                                                            "D": "1",
                                                            "Abilities": "Blast"
                                                        }
                                                    }
                                                },
                                                "selection_entries": {},
                                                "selection_entry_groups": {},
                                                "entry_links": {},
                                                "category_links": [],
                                                "costs": {
                                                    "pts": "20.0"
                                                }
                                            }
                                        },
                                        "e3d1-2cae-8e85-49d3": {
                                            "primary_category": "",
                                            "id": "e3d1-2cae-8e85-49d3",
                                            "name": "Bright Lance",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "constraints": [],
                                            "profiles": [],
                                            "rules": [],
                                            "info_groups": [],
                                            "info_links": {},
                                            "selection_entries": {},
                                            "selection_entry_groups": {},
                                            "entry_links": {},
                                            "category_links": [],
                                            "costs": {},
                                            "target_type": "selectionEntry",
                                            "link_target": {
                                                "type": "upgrade",
                                                "primary_category": "",
                                                "id": "57df-80ae-e780-591e",
                                                "name": "Bright Lance",
                                                "comment": "",
                                                "modifiers": [],
                                                "modifier_groups": [],
                                                "constraints": [],
                                                "profiles": [],
                                                "rules": [],
                                                "info_groups": [],
                                                "info_links": {
                                                    "6058-dc2c-a284-968d": {
                                                        "target_type": "profile",
                                                        "id": "6058-dc2c-a284-968d",
                                                        "name": "Bright Lance",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "Bright Lance",
                                                            "Range": "36\"",
                                                            "Type": "Heavy 1",
                                                            "S": "8",
                                                            "AP": "-4",
                                                            "D": "D6",
                                                            "Abilities": "-"
                                                        }
                                                    }
                                                },
                                                "selection_entries": {},
                                                "selection_entry_groups": {},
                                                "entry_links": {},
                                                "category_links": [],
                                                "costs": {
                                                    "pts": "20.0"
                                                }
                                            }
                                        },
                                        "dac7-8c51-973d-348a": {
                                            "primary_category": "",
                                            "id": "dac7-8c51-973d-348a",
                                            "name": "Scatter Laser",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "constraints": [],
                                            "profiles": [],
                                            "rules": [],
                                            "info_groups": [],
                                            "info_links": {},
                                            "selection_entries": {},
                                            "selection_entry_groups": {},
                                            "entry_links": {},
                                            "category_links": [],
                                            "costs": {},
                                            "target_type": "selectionEntry",
                                            "link_target": {
                                                "type": "upgrade",
                                                "primary_category": "",
                                                "id": "3725-493d-89a4-75b1",
                                                "name": "Scatter Laser",
                                                "comment": "",
                                                "modifiers": [],
                                                "modifier_groups": [],
                                                "constraints": [],
                                                "profiles": [],
                                                "rules": [],
                                                "info_groups": [],
                                                "info_links": {
                                                    "8cd6-d8e1-ae8a-6806": {
                                                        "target_type": "profile",
                                                        "id": "8cd6-d8e1-ae8a-6806",
                                                        "name": "",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "Scatter Laser",
                                                            "Range": "36\"",
                                                            "Type": "Heavy 4",
                                                            "S": "6",
                                                            "AP": "0",
                                                            "D": "1",
                                                            "Abilities": "-"
                                                        }
                                                    }
                                                },
                                                "selection_entries": {},
                                                "selection_entry_groups": {},
                                                "entry_links": {},
                                                "category_links": [],
                                                "costs": {
                                                    "pts": "10.0"
                                                }
                                            }
                                        },
                                        "1876-f0a7-9823-173e": {
                                            "primary_category": "",
                                            "id": "1876-f0a7-9823-173e",
                                            "name": "Shuriken Cannon",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "constraints": [],
                                            "profiles": [],
                                            "rules": [],
                                            "info_groups": [],
                                            "info_links": {},
                                            "selection_entries": {},
                                            "selection_entry_groups": {},
                                            "entry_links": {},
                                            "category_links": [],
                                            "costs": {},
                                            "target_type": "selectionEntry",
                                            "link_target": {
                                                "type": "upgrade",
                                                "primary_category": "",
                                                "id": "64d6-6994-d3e8-6e09",
                                                "name": "Shuriken Cannon",
                                                "comment": "",
                                                "modifiers": [],
                                                "modifier_groups": [],
                                                "constraints": [],
                                                "profiles": [],
                                                "rules": [],
                                                "info_groups": [],
                                                "info_links": {
                                                    "8dc0-d0b2-c152-cd0d": {
                                                        "target_type": "profile",
                                                        "id": "8dc0-d0b2-c152-cd0d",
                                                        "name": "",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "Shuriken Cannon",
                                                            "Range": "24\"",
                                                            "Type": "Assault 3",
                                                            "S": "6",
                                                            "AP": "0",
                                                            "D": "1",
                                                            "Abilities": "Each time you make a wound roll of 6+ for this weapon, that hit is resolved with an AP of -3 instead of 0."
                                                        }
                                                    }
                                                },
                                                "selection_entries": {},
                                                "selection_entry_groups": {},
                                                "entry_links": {},
                                                "category_links": [],
                                                "costs": {
                                                    "pts": "10.0"
                                                }
                                            }
                                        },
                                        "9d6e-c587-51bc-ec7e": {
                                            "primary_category": "",
                                            "id": "9d6e-c587-51bc-ec7e",
                                            "name": "Starcannon",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "constraints": [],
                                            "profiles": [],
                                            "rules": [],
                                            "info_groups": [],
                                            "info_links": {},
                                            "selection_entries": {},
                                            "selection_entry_groups": {},
                                            "entry_links": {},
                                            "category_links": [],
                                            "costs": {},
                                            "target_type": "selectionEntry",
                                            "link_target": {
                                                "type": "upgrade",
                                                "primary_category": "",
                                                "id": "c628-671e-285b-b6bf",
                                                "name": "Starcannon",
                                                "comment": "",
                                                "modifiers": [],
                                                "modifier_groups": [],
                                                "constraints": [],
                                                "profiles": [],
                                                "rules": [],
                                                "info_groups": [],
                                                "info_links": {
                                                    "8f17-5eac-b719-7788": {
                                                        "target_type": "profile",
                                                        "id": "8f17-5eac-b719-7788",
                                                        "name": "Starcannon",
                                                        "comment": "",
                                                        "modifiers": [],
                                                        "modifier_groups": [],
                                                        "link_target": {
                                                            "profile_type": "Weapon",
                                                            "name": "Starcannon",
                                                            "Range": "36\"",
                                                            "Type": "Heavy 2",
                                                            "S": "6",
                                                            "AP": "-3",
                                                            "D": "D3",
                                                            "Abilities": "-"
                                                        }
                                                    }
                                                },
                                                "selection_entries": {},
                                                "selection_entry_groups": {},
                                                "entry_links": {},
                                                "category_links": [],
                                                "costs": {
                                                    "pts": "15.0"
                                                }
                                            }
                                        }
                                    },
                                    "category_links": [],
                                    "default_selection": "1876-f0a7-9823-173e"
                                }
                            }
                        },
                        "category_links": [
                            "Heavy Weapons Platform",
                            "Artillery"
                        ],
                        "costs": {
                            "pts": "12.0",
                            "PL": "1.0"
                        }
                    },
                    "c758-aaf5-4754-8653": {
                        "type": "model",
                        "primary_category": "",
                        "id": "c758-aaf5-4754-8653",
                        "name": "Guardian Defender",
                        "comment": "",
                        "modifiers": [],
                        "modifier_groups": [],
                        "constraints": [],
                        "profiles": [
                            {
                                "profile_type": "Unit",
                                "name": "Guardian Defender",
                                "M": "7\"",
                                "WS": "3+",
                                "BS": "3+",
                                "S": "3",
                                "T": "3",
                                "W": "1",
                                "A": "1",
                                "Ld": "7",
                                "Save": "5+"
                            }
                        ],
                        "rules": [],
                        "info_groups": [],
                        "info_links": {},
                        "selection_entries": {},
                        "selection_entry_groups": {},
                        "entry_links": {
                            "52e5-2c4d-f31d-2306": {
                                "primary_category": "",
                                "id": "52e5-2c4d-f31d-2306",
                                "name": "",
                                "comment": "",
                                "modifiers": [],
                                "modifier_groups": [],
                                "constraints": [],
                                "profiles": [],
                                "rules": [],
                                "info_groups": [],
                                "info_links": {},
                                "selection_entries": {},
                                "selection_entry_groups": {},
                                "entry_links": {},
                                "category_links": [],
                                "costs": {},
                                "target_type": "selectionEntry",
                                "link_target": {
                                    "type": "upgrade",
                                    "primary_category": "",
                                    "id": "1d13-3a9a-37d6-1735",
                                    "name": "Shuriken Catapult",
                                    "comment": "",
                                    "modifiers": [],
                                    "modifier_groups": [],
                                    "constraints": [],
                                    "profiles": [],
                                    "rules": [],
                                    "info_groups": [],
                                    "info_links": {
                                        "dc2f-3dd4-422f-6ed4": {
                                            "target_type": "profile",
                                            "id": "dc2f-3dd4-422f-6ed4",
                                            "name": "",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "link_target": {
                                                "profile_type": "Weapon",
                                                "name": "Shuriken Catapult",
                                                "Range": "12\"",
                                                "Type": "Assault 2",
                                                "S": "4",
                                                "AP": "0",
                                                "D": "1",
                                                "Abilities": "Each time you make a wound roll of 6+ for this weapon, that hit is resolved with an AP of -3 instead of 0."
                                            }
                                        }
                                    },
                                    "selection_entries": {},
                                    "selection_entry_groups": {},
                                    "entry_links": {},
                                    "category_links": [],
                                    "costs": {}
                                }
                            },
                            "94d6-a95f-c32a-3524": {
                                "primary_category": "",
                                "id": "94d6-a95f-c32a-3524",
                                "name": "Plasma Grenades",
                                "comment": "",
                                "modifiers": [],
                                "modifier_groups": [],
                                "constraints": [],
                                "profiles": [],
                                "rules": [],
                                "info_groups": [],
                                "info_links": {},
                                "selection_entries": {},
                                "selection_entry_groups": {},
                                "entry_links": {},
                                "category_links": [],
                                "costs": {},
                                "target_type": "selectionEntry",
                                "link_target": {
                                    "type": "upgrade",
                                    "primary_category": "",
                                    "id": "b7fa-f88c-305c-534f",
                                    "name": "Plasma Grenades",
                                    "comment": "",
                                    "modifiers": [],
                                    "modifier_groups": [],
                                    "constraints": [],
                                    "profiles": [],
                                    "rules": [],
                                    "info_groups": [],
                                    "info_links": {
                                        "9681-d218-8c01-af9a": {
                                            "target_type": "profile",
                                            "id": "9681-d218-8c01-af9a",
                                            "name": "Plasma Grenade",
                                            "comment": "",
                                            "modifiers": [],
                                            "modifier_groups": [],
                                            "link_target": {
                                                "profile_type": "Weapon",
                                                "name": "Plasma Grenade",
                                                "Range": "6\"",
                                                "Type": "Grenade D6",
                                                "S": "4",
                                                "AP": "-1",
                                                "D": "1",
                                                "Abilities": "Blast"
                                            }
                                        }
                                    },
                                    "selection_entries": {},
                                    "selection_entry_groups": {},
                                    "entry_links": {},
                                    "category_links": [],
                                    "costs": {}
                                }
                            }
                        },
                        "category_links": [
                            "Guardian Defenders"
                        ],
                        "costs": {
                            "pts": "10.0"
                        }
                    }
                },
                "selection_entry_groups": {},
                "entry_links": {
                    "dummy": {
                        "target_type": "selectionEntry",
                        "link_target": {
                            "selection_entries": {},
                            "entry_links": {}
                        },
                    }
                },
                "category_links": [
                    "Faction: <Craftworld>",
                    "Faction: Aeldari",
                    "Faction: Asuryani",
                    "Infantry",
                    "Troops",
                    "Faction: Warhost",
                    "Guardian"
                ],
                "costs": {
                    "PL": "5.0"
                }
            }
        }
}


def test_remove_empty_links():
    test = {
        'foo': [],
        'bar': {},
        'selection_entries': {
            'id1': {
                'foo': [],
                'bar': {},
                'selection_entries': {
                    'id2': {
                        'foo': [],
                        'bar': {}
                    },
                    'something': 'to stop this entry getting deleted'
                },
                'selection_entry_groups': {}
            }
        },
        'selection_entry_groups': {
            'id1': {
                'foo': [],
                'bar': {},
                'something': 'to stop this entry getting deleted'
            }
        }
    }
    result = remove_empty_links(test)
    assert 'foo' not in result.keys()
    assert 'bar' not in result.keys()
    assert 'foo' not in result['selection_entries'].keys()
    assert 'bar' not in result['selection_entries'].keys()
    assert 'foo' not in result['selection_entry_groups'].keys()
    assert 'bar' not in result['selection_entry_groups'].keys()
    assert 'foo' not in result['selection_entries']['id1']['selection_entries'].keys()
    assert 'bar' not in result['selection_entries']['id1']['selection_entries'].keys()


def test_remove_empty_links_real_case():
    result = remove_empty_links(resolve_links(example_json['c353-858f-36ed-23d4']['link_target']))
    assert 'info_links' not in result.keys()


def test_resolve_links():
    len(example_json['c353-858f-36ed-23d4']['link_target']['selection_entries'].keys()) == 2
    result = resolve_links(example_json['c353-858f-36ed-23d4']['link_target'])
    assert result
    assert result['entry_links'] == {}
    assert result['info_links'] == {}
    assert len(result['selection_entries'].keys()) == 3
    assert '52e5-2c4d-f31d-2306' in result['selection_entries']['c758-aaf5-4754-8653']['selection_entries']
    assert result['selection_entries']['c758-aaf5-4754-8653']['selection_entries']['52e5-2c4d-f31d-2306']['name'] == 'Shuriken Catapult'


def test_make_unit_from_bs():
    # idea is a selector describes just enough for loading selections from a catalogue
    # for repeat selections maybe list [(count, id, [(child_count, child_id, [child_childs]), ...]), ...]
    selector = {
        'c758-aaf5-4754-8653': (4, ('1d13-3a9a-37d6-1735', 'b7fa-f88c-305c-534f')),
        # defenders with catapult and grenades
        '8cb4-c382-d67e-3d08': (1, ('57df-80ae-e780-591e'))
        # weapons platform with bright lance
    }
    unit = make_unit_from_bs('some clever name', 'c353-858f-36ed-23d4', selector, example_json, 5, Strategy.CHARGE, False)
    assert unit.unit_type == 'Guardian Defenders'
    assert "Infantry" in unit.tags
    assert unit.models[0].model.name == 'Guardian Defender 0'
    assert unit.models[3].model.name == 'Guardian Defender 3'
    assert len(unit.models[0].weapons) == 2
    assert unit.models[0].weapons[0].name == 'Shuriken Catapult'
    assert unit.models[0].weapons[0].strength == '4'
    assert unit.models[0].weapons[1].name == 'Plasma Grenades'
    assert unit.models[-1].model.name == 'Guardian Heavy Weapons Platform 0'
    assert unit.models[-1].weapons[0].name == 'Bright Lance'
    assert unit.models[-1].weapons[0].strength == '8'
