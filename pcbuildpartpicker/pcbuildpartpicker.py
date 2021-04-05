#!/usr/bin/env python3
import argparse
import sys

import pandas


def get_args() -> argparse.Namespace:
    """Get command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--parts-file', type=str, help='json file containg parts to pick from')
    parser.add_argument('-b', '--budget', type=int, help='budget in euros')
    args = parser.parse_args()

    return args


def load_data_from_csv(parts_file: str):
    df = pandas.read_csv(parts_file)
    return df


def main():
    args = get_args()
    print(f'Budget €{args.budget:0,.2f}\n')
    try:
        original_parts = load_data_from_csv(args.parts_file)
        print(f'Parts to pick from \n{original_parts}')

        add_exp_score_by_cost_to(original_parts)
        print(f'Parts with experience score by cost \n{original_parts}')

        selected_parts = select_parts_based_on(original_parts, 'exp/cost')
        print_results('Best Value', selected_parts)

        reset_selected_parts(original_parts)
        selected_parts = select_parts_based_on(original_parts, 'experience_score')
        print_results('Maximum Experience Score', selected_parts)

        get_in_budget(original_parts, args.budget)

        # print_results('All Parts', original_parts)

        sys.exit(0)
    except Exception as e:
        print(f'exception: {e}')
        sys.exit(1)


def reset_selected_parts(original_parts):
    original_parts.loc[:, 'selected'] = False


def print_results(use_case, selected_parts):
    print('#' * 10 + f' {use_case} ' + '#' * 10)
    print(f'Picked Parts \n{selected_parts}')
    print('#' * 30)
    print(f"Total Cost: €{selected_parts['cost'].sum():0,.2f}")
    print(f"Total Experience Score: {selected_parts['experience_score'].sum()}\n")


def get_in_budget(parts, budget):
    if in_budget(parts, budget):
        return
    parts.sort_values(['selected', 'experience_score'], ascending=[False, False], inplace=True)
    parts.reset_index(drop=True, inplace=True)
    # print_results("SORTED by selected and experience_score", parts)
    attempts = 0
    while not in_budget(parts, budget) and attempts < 6:
        parts.at[attempts, 'selected'] = False
        category = parts.at[attempts, 'category']
        deselected_part = parts.at[attempts, 'name']
        print('#' * 30)
        print(f"Attempt: {attempts}, Category: {category}")
        print('#' * 30)
        for index, row in parts.iterrows():
            if row['category'] == category and row['name'] != deselected_part:
                parts.at[index, 'selected'] = True
                new_part = row
                break
        print(f"Check if {new_part['name']} costing {new_part['cost']} instead of {deselected_part} works")
        attempts += 1


def in_budget(parts, budget):
    selected_parts = parts.loc[parts['selected'] == True]
    # print_results("Budget attempt", selected_parts)
    cost = selected_parts['cost'].sum()
    if cost > budget:
        print(f'Cost: €{cost} > Budget: €{budget}')
        return False
    else:
        print(f'Cost: €{cost} within budget: €{budget}')
        print_results("", selected_parts)
        return True


def select_parts_based_on(parts, sort_by):
    parts.sort_values(by=[sort_by], inplace=True, ascending=False)
    picked_part_category_tracker = []
    for index, row in parts.iterrows():
        if row['category'] not in picked_part_category_tracker:
            picked_part_category_tracker.append(row['category'])
            parts.at[index, 'selected'] = True
    return parts.loc[parts['selected'] == True]


def add_exp_score_by_cost_to(parts):
    parts['selected'] = False
    parts['exp/cost'] = parts['experience_score'] / parts['cost']
    print(f'Parts sorted by exp/cost\n {parts}')


if __name__ == "__main__":
    main()
