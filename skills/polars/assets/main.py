#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "polars",
# ]
# ///

from __future__ import annotations

from pathlib import Path

import polars as pl

BASE_DIR = Path(__file__).parent


def main() -> None:
    sales_path = BASE_DIR / 'sales.csv'
    regions_path = BASE_DIR / 'regions.csv'
    output_path = BASE_DIR / 'report.parquet'

    sales = pl.scan_csv(
        sales_path,
        schema_overrides={
            'order_id': pl.UInt32,
            'region_id': pl.UInt8,
            'amount': pl.Float64,
        },
    )
    regions = pl.scan_csv(
        regions_path,
        schema_overrides={
            'region_id': pl.UInt8,
            'region_name': pl.String,
        },
    )

    report = (
        sales
        .filter(pl.col('amount') > 0)
        .join(regions, on='region_id', how='left')
        .group_by('region_name')
        .agg(
            pl.len().alias('orders'),
            pl.col('amount').sum().alias('revenue'),
            pl.col('amount').mean().round(2).alias('avg_order'),
        )
        .sort('region_name')
        .collect()
    )

    report.write_parquet(output_path)
    print(report)
    print(f'wrote {output_path.name}')


if __name__ == '__main__':
    main()
