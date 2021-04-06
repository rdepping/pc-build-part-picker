#!/usr/bin/env python3
import argparse
import sys

import pandas


def get_args() -> argparse.Namespace:
    """Get command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--parts-file', type=str, help='json file containg parts to pick from')
    parser.add_argument('-b', '--budget', type=int, help='budget in euros')
    parser.add_argument('-s', '--sort', type=str, help='sort by', default='exp/cost')
    args = parser.parse_args()

    return args


def load_data_from_csv(parts_file: str):
    df = pandas.read_csv(parts_file)
    return df


def main():
    args = get_args()
    print(f'Budget €{args.budget:0,.2f}\n')
    summary_printer = part_picker_summary_print(args.budget)
    try:
        original_parts = load_data_from_csv(args.parts_file)
        print(f'Parts to pick from \n{original_parts}')

        add_exp_score_by_cost_to(original_parts)
        print(f'Parts with experience score by cost \n{original_parts}')

        selected_parts = select_parts_based_on(original_parts, 'exp/cost')
        summary_printer('Best Value', selected_parts)

        reset_selected_parts(original_parts)
        selected_parts = select_parts_based_on(original_parts, 'experience_score')
        summary_printer('Maximum Experience Score Pick', selected_parts)

        selected_parts = select_for_budget(original_parts, args.budget, args.sort)

        if selected_parts is None:
            print(f'Failed to find parts in budget {args.budget}')
        else:
            summary_printer('Selected Parts', selected_parts)

        sys.exit(0)
    except Exception as e:
        print(f'exception: {e}')
        sys.exit(1)


def reset_selected_parts(parts):
    parts.loc[:, 'selected'] = False


def part_picker_summary_print(budget):
    def print_part_picker_summary(use_case, selected_parts):
        print('\n\n')
        print('#' * 10 + f' {use_case} ' + '#' * 10)
        print(f'{selected_parts}')
        print('#' * 40)
        print(f"Total Budget: €{budget:0,.2f}")
        costs = selected_parts['cost'].sum()
        print(f"Total Cost: €{costs :0,.2f}")
        print(f"Remaining Budget: €{budget-costs:0,.2f}")
        print(f"Total Experience Score: {selected_parts['experience_score'].sum()}")
        print('#' * 40)
        print('\n\n')
    return print_part_picker_summary


def select_for_budget(original_parts, budget, sort):
    original_parts.sort_values(by=['selected', sort], ascending=[False, True], inplace=True,
                               ignore_index=True)
    if in_budget(original_parts, budget):
        return original_parts.loc[original_parts['selected'] == True]
    category_idx = 0
    in_budget_flag = False
    selected_parts = original_parts.loc[original_parts['selected'] == True]
    while not in_budget_flag and category_idx < 6:  # 6 categories
        category = selected_parts.at[category_idx, 'category']
        not_selected_parts = get_alternative_parts(category, original_parts)
        deselected_part = selected_parts.at[category_idx, 'name']
        selected_parts = selected_parts.drop(category_idx)
        prev_not_selected_idx = None
        for not_selected_parts_idx, row in not_selected_parts.iterrows():
            if prev_not_selected_idx:
                selected_parts = selected_parts.drop(prev_not_selected_idx) # We are trying again, so drop the last selected
            prev_not_selected_idx = not_selected_parts_idx
            print('#' * 40)
            print(f"Category Part Swap: {category}")
            print(f"\t- Removing: {deselected_part}")
            print(f"\t- Adding: {not_selected_parts.loc[not_selected_parts_idx]['name']}")
            selected_parts = selected_parts.append(row)
            selected_parts.at[not_selected_parts_idx, 'selected'] = True
            if in_budget(selected_parts, budget):
                return selected_parts.loc[selected_parts['selected'] == True]
            # print('#' * 40)
        category_idx += 1
    return None


def get_alternative_parts(category, original_parts):
    return original_parts[
        (original_parts['selected'] == False) & (original_parts['category'] == category)].sort_values(
        by=['experience_score'], ascending=False)


def in_budget(parts, budget):
    selected_parts = parts.loc[parts['selected'] == True]
    # print_results("Budget Match Attempt", selected_parts)
    cost = selected_parts['cost'].sum()
    if cost > budget:
        print(f'Cost: €{cost} > Budget: €{budget}')
        return False
    else:
        print(f'Cost: €{cost} within budget: €{budget}')
        # print_results("Within Budget Pick", selected_parts)
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


if __name__ == "__main__":
    main()
