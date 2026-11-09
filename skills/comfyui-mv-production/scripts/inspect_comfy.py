"""Read ComfyUI node contracts and check a prepared API graph without queuing it."""
import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request


def inspect_graph(graph, definitions):
    graph = graph.get('prompt', graph)
    missing = sorted({v['class_type'] for v in graph.values()} - set(definitions))
    errors = []
    for node_id, node in graph.items():
        if node['class_type'] not in definitions:
            continue
        required = definitions[node['class_type']].get('input', {}).get('required', {})
        for name, contract in required.items():
            if name not in node.get('inputs', {}):
                errors.append(f'{node_id}.{name}: required input missing')
                continue
            value = node['inputs'][name]
            if isinstance(value, str) and '{{' in value:
                errors.append(f'{node_id}.{name}: unresolved parameter')
            choices = contract[0] if contract and isinstance(contract[0], list) else None
            if choices is None and len(contract) > 1 and isinstance(contract[1], dict):
                choices = contract[1].get('options')
            if not isinstance(choices, list) or any(isinstance(c, (dict, list)) for c in choices):
                choices = None
            if choices and not isinstance(value, list) and value not in choices:
                errors.append(f'{node_id}.{name}: unavailable choice {value!r}')
    return dict(ready=not missing and not errors, missing_nodes=missing, input_errors=errors,
                runtime_validation_still_required=True, submitted=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', type=Path)
    parser.add_argument('--server', default='http://127.0.0.1:8188')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if urllib.parse.urlsplit(args.server).username:
        parser.error('Do not embed credentials in the server URL')
    with urllib.request.urlopen(args.server.rstrip('/') + '/object_info', timeout=30) as response:
        definitions = json.load(response)
    result = inspect_graph(json.loads(args.workflow.read_text(encoding='utf-8')), definitions)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text)
    return 0 if result['ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
