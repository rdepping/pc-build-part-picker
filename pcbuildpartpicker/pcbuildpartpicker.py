#!/usr/bin/env python3
import argparse
import sys

import pandas


def get_args() -> argparse.Namespace:
    """Get command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--parts-file', type=str, help='json file containg parts to pick from')
    parser.add_argument('-b', '--budget', type=int, help='budget in euros')
    parser.add_argument('-s', '--sort', type=str, help='sort by', default='cost')
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

        # add_exp_score_by_cost_to(original_parts)
        # print(f'Parts with experience score by cost \n{original_parts}')

        # selected_parts = select_parts_based_on(original_parts, 'exp/cost')
        # print_results('Best Value', selected_parts)

        reset_selected_parts(original_parts)
        selected_parts = select_parts_based_on(original_parts, 'experience_score')
        print_results('Maximum Experience Score', selected_parts)

        selected_parts = get_in_budget(original_parts, args.budget, args.sort)

        print_results('Selected Parts', selected_parts)

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


def get_in_budget(original_parts, budget, sort='experience_score'):
    original_parts.sort_values(by=['selected', 'experience_score'], ascending=[False, True], inplace=True, ignore_index=True)
    if in_budget(original_parts, budget):
        return original_parts.loc[original_parts['selected'] == True]
    attempts = 0
    in_budget_flag = False
    while not in_budget_flag and attempts < 6: # 6 categories
        selected_parts = original_parts.loc[original_parts['selected'] == True]
        category = selected_parts.at[attempts, 'category']
        not_selected_df = original_parts[(original_parts['selected'] == False) & (original_parts['category'] == category)].sort_values(by=['experience_score'], ascending=False)
        selected_parts.at[attempts, 'selected'] = False
        deselected_part = original_parts.at[attempts, 'name']
        print('#' * 30)
        print(f"Attempt: {attempts} for Category: {category}")
        for index, row in not_selected_df.iterrows():
            print(f"\t- Removing {deselected_part} adding {original_parts.loc[index]['name']}")
            selected_parts = selected_parts.append(row)
            selected_parts.at[index, 'selected'] = True
            if in_budget(selected_parts, budget):
                in_budget_flag = True
                break
            else:
                selected_parts = selected_parts.drop(index)
        print('#' * 30)
        attempts += 1
    return selected_parts.loc[selected_parts['selected'] == True]


def in_budget(parts, budget):
    selected_parts = parts.loc[parts['selected'] == True]
    print_results("Budget Match Attempt", selected_parts)
    cost = selected_parts['cost'].sum()
    if cost > budget:
        print(f'Cost: €{cost} > Budget: €{budget}')
        return False
    else:
        print(f'Cost: €{cost} within budget: €{budget}')
        print_results("Within Budget Pick", selected_parts)
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
