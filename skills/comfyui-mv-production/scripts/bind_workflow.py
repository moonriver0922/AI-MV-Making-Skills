"""Bind JSON workflow parameters locally. Never submits a GPU task."""
import argparse
import json
from pathlib import Path
import re

TOKEN = re.compile(r'\{\{([A-Za-z0-9_.-]+)\}\}')


def lookup(config, path):
    value = config
    for key in path.split('.'):
        value = value[key]
    return value


def bind(value, config):
    if isinstance(value, dict):
        return {key: bind(item, config) for key, item in value.items()}
    if isinstance(value, list):
        return [bind(item, config) for item in value]
    if not isinstance(value, str):
        return value
    match = TOKEN.fullmatch(value)
    if match:
        return lookup(config, match.group(1))
    return TOKEN.sub(lambda match: str(lookup(config, match.group(1))), value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('template', type=Path)
    parser.add_argument('project', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; use a new versioned filename')
    template = json.loads(args.template.read_text(encoding='utf-8'))
    config = json.loads(args.project.read_text(encoding='utf-8'))
    result = bind(template, config)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Prepared locally, not submitted:', args.output)


if __name__ == '__main__':
    main()
