#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "sqlmodel",
# ]
# ///

from __future__ import annotations

import argparse
import importlib
import logging
import os

from sqlmodel import SQLModel, create_engine

LOGGER = logging.getLogger(__name__)


def init_database(database_url: str | None = None, module: str = 'app.models') -> None:
    if database_url is None:
        database_url = os.getenv('DATABASE_URL')

    if not database_url:
        raise SystemExit('DATABASE_URL not provided')

    safe_target = database_url.split('@', 1)[1] if '@' in database_url else database_url
    LOGGER.info('connecting to %s', safe_target)

    engine = create_engine(database_url, echo=True)

    try:
        importlib.import_module(module)
    except ImportError:
        LOGGER.warning('could not import models from %s; adjust before using this helper', module)

    LOGGER.info('creating tables')
    SQLModel.metadata.create_all(engine)
    LOGGER.info('database initialized')


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description='Initialize a database from imported SQLModel metadata',
    )
    parser.add_argument('--url', help='database URL (default: DATABASE_URL)')
    parser.add_argument(
        '--module',
        default='app.models',
        help='module to import before create_all()',
    )
    args = parser.parse_args()
    init_database(args.url, args.module)


if __name__ == '__main__':
    main()
