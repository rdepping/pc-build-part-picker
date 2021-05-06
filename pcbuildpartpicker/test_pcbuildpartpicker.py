from pandas import DataFrame

import pcbuildpartpicker

selected_parts_test_data = {
    "category": {
        0: "case",
        1: "storage",
        2: "motherboard",
        3: "memory",
        4: "graphics",
        5: "cpu",
    },
    "name": {
        0: "very-base case",
        1: "base storage 1",
        2: "mid mb 2",
        3: "base memory 1",
        4: "mid graphics 2",
        5: "high-end cpu 3",
    },
    "cost": {0: 5, 1: 40, 2: 75, 3: 100, 4: 120, 5: 300},
    "experience_score": {0: 2, 1: 5, 2: 8, 3: 8, 4: 12, 5: 30},
    "selected": {0: True, 1: True, 2: True, 3: True, 4: True, 5: True},
    "exp/cost": {0: 0.4, 1: 0.125, 2: 0.10666666666666667, 3: 0.08, 4: 0.1, 5: 0.1},
}

original_parts_test_data = {
    "category": {
        0: "case",
        1: "case",
        2: "case",
        3: "case",
        4: "motherboard",
        5: "motherboard",
        6: "motherboard",
        7: "cpu",
        8: "cpu",
        9: "cpu",
        10: "graphics",
        11: "graphics",
        12: "graphics",
        13: "storage",
        14: "storage",
        15: "storage",
        16: "memory",
        17: "memory",
        18: "memory",
    },
    "name": {
        0: "base case 1",
        1: "mid case 2",
        2: "high-end case 3",
        3: "very-base case",
        4: "base mb 1",
        5: "mid mb 2",
        6: "high-end mb 3",
        7: "base cpu 1",
        8: "mid cpu 2",
        9: "high-end cpu 3",
        10: "base graphics 1",
        11: "mid graphics 2",
        12: "high-end graphics 3",
        13: "base storage 1",
        14: "mid storage 2",
        15: "high-end storage 3",
        16: "base memory 1",
        17: "mid memory 2",
        18: "high-end memory 3",
    },
    "cost": {
        0: 30,
        1: 50,
        2: 75,
        3: 5,
        4: 50,
        5: 75,
        6: 120,
        7: 150,
        8: 200,
        9: 300,
        10: 80,
        11: 120,
        12: 200,
        13: 40,
        14: 80,
        15: 120,
        16: 100,
        17: 150,
        18: 200,
    },
    "experience_score": {
        0: 3,
        1: 6,
        2: 8,
        3: 2,
        4: 5,
        5: 8,
        6: 12,
        7: 12,
        8: 20,
        9: 30,
        10: 8,
        11: 12,
        12: 16,
        13: 5,
        14: 7,
        15: 9,
        16: 8,
        17: 12,
        18: 14,
    },
}

original_parts_selected_by_experience_score = {
    "category": {
        9: "cpu",
        8: "cpu",
        12: "graphics",
        18: "memory",
        6: "motherboard",
        7: "cpu",
        11: "graphics",
        17: "memory",
        15: "storage",
        5: "motherboard",
        10: "graphics",
        2: "case",
        16: "memory",
        14: "storage",
        1: "case",
        4: "motherboard",
        13: "storage",
        0: "case",
        3: "case",
    },
    "name": {
        9: "high-end cpu 3",
        8: "mid cpu 2",
        12: "high-end graphics 3",
        18: "high-end memory 3",
        6: "high-end mb 3",
        7: "base cpu 1",
        11: "mid graphics 2",
        17: "mid memory 2",
        15: "high-end storage 3",
        5: "mid mb 2",
        10: "base graphics 1",
        2: "high-end case 3",
        16: "base memory 1",
        14: "mid storage 2",
        1: "mid case 2",
        4: "base mb 1",
        13: "base storage 1",
        0: "base case 1",
        3: "very-base case",
    },
    "cost": {
        9: 300,
        8: 200,
        12: 200,
        18: 200,
        6: 120,
        7: 150,
        11: 120,
        17: 150,
        15: 120,
        5: 75,
        10: 80,
        2: 75,
        16: 100,
        14: 80,
        1: 50,
        4: 50,
        13: 40,
        0: 30,
        3: 5,
    },
    "experience_score": {
        9: 30,
        8: 20,
        12: 16,
        18: 14,
        6: 12,
        7: 12,
        11: 12,
        17: 12,
        15: 9,
        5: 8,
        10: 8,
        2: 8,
        16: 8,
        14: 7,
        1: 6,
        4: 5,
        13: 5,
        0: 3,
        3: 2,
    },
    "selected": {
        9: True,
        8: False,
        12: True,
        18: True,
        6: True,
        7: False,
        11: False,
        17: False,
        15: True,
        5: False,
        10: False,
        2: True,
        16: False,
        14: False,
        1: False,
        4: False,
        13: False,
        0: False,
        3: False,
    },
    "exp/cost": {
        9: 0.1,
        8: 0.1,
        12: 0.08,
        18: 0.07,
        6: 0.1,
        7: 0.08,
        11: 0.1,
        17: 0.08,
        15: 0.075,
        5: 0.10666666666666667,
        10: 0.1,
        2: 0.10666666666666667,
        16: 0.08,
        14: 0.0875,
        1: 0.12,
        4: 0.1,
        13: 0.125,
        0: 0.1,
        3: 0.4,
    },
}


def test_print_summary():
    budget = 1000
    summary_print = pcbuildpartpicker.part_picker_summary_print(budget)
    summary_print("test use case", DataFrame.from_dict(selected_parts_test_data))


def test_add_columns():
    test_parts_df = DataFrame.from_dict(
        {"experience_score": [10, 20, 30], "cost": [2, 4, 8]}
    )
    assert "selected" not in test_parts_df.columns
    assert "exp/cost" not in test_parts_df.columns

    pcbuildpartpicker.add_additional_columns(test_parts_df)

    assert "selected" in test_parts_df.columns
    assert "exp/cost" in test_parts_df.columns


def test_unique_categories_selected_for_given_budget():
    budget = 1000
    selected_parts = pcbuildpartpicker.select_for_budget(
        DataFrame.from_dict(original_parts_selected_by_experience_score),
        budget=budget,
        sort="exp/cost",
    )
    assert len(selected_parts["selected"]) == 6
    assert selected_parts["cost"].sum() <= budget
    assert selected_parts["category"].is_unique
