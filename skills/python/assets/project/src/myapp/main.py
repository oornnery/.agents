from __future__ import annotations

from myapp.settings import Settings


def build_message(settings: Settings) -> str:
    return f'{settings.app_name}: {settings.environment}'


def main() -> None:
    settings = Settings()
    print(build_message(settings))


if __name__ == '__main__':
    main()
