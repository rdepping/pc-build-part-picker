#!/usr/bin/env python3
import argparse
import csv
import json
import pprint
import sys
import pandas


def get_args() -> argparse.Namespace:
    """Get command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--parts-file', type=str, help='json file containg parts to pick from')
    parser.add_argument('-b', '--budget', type=int, help='budget in euros')
    args = parser.parse_args()

    return args


def load_csv_from(parts_file: str):
    df = pandas.read_csv(parts_file)
    return df


def main():
    args = get_args()
    print(f'Budget €{args.budget:0,.2f}\n')
    try:
        original_parts = load_csv_from(args.parts_file)

        add_exp_score_by_cost(original_parts)

        selected_parts = select_parts(original_parts)

        print(f'Picked Parts\n {selected_parts}')
        print(f"Total Cost €{selected_parts['cost'].sum():0,.2f}")
        print(f"Total Experience Score {selected_parts['experience_score'].sum()}\n")
    except Exception as e:
        print(f'exception: {e}')
        sys.exit(1)


def select_parts(original_parts):
    picked_part_category_tracker = []
    for index, row in original_parts.iterrows():
        if row['category'] not in picked_part_category_tracker:
            picked_part_category_tracker.append(row['category'])
            original_parts.at[index, 'selected'] = True
    original_parts.sort_values(by=['selected'], inplace=True, ascending=False)
    selected_parts = original_parts.loc[original_parts['selected'] == True]
    return selected_parts


def add_exp_score_by_cost(original_parts):
    print(f'Parts to pick from\n {original_parts}')
    original_parts['selected'] = False
    original_parts['exp/cost'] = original_parts['experience_score'] / original_parts['cost']
    original_parts.sort_values(by=['exp/cost'], inplace=True, ascending=False)
    print(f'Parts sorted by exp/cost\n {original_parts}')


if __name__ == "__main__":
    main()
