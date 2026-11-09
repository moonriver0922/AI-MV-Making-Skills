"""Audit declared shot lineage; metadata-only mode never certifies real files."""
import argparse
import copy
import json
from pathlib import Path
import subprocess

STAGES = {'native', 'second_pass', 'super_resolution'}


def audit_shot(shot, probe=False):
    candidates = copy.deepcopy(shot['candidates'])
    ids = [c['id'] for c in candidates]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate candidate IDs in ' + shot['shot_id'])
    by_id = {c['id']: c for c in candidates}
    rejected, eligible = {}, []
    start, count = int(shot['source_in']), int(shot['frames'])
    if start < 0 or count <= 0:
        raise ValueError('Invalid source interval')
    for candidate in candidates:
        reason, seen, current = None, set(), candidate
        while current is not None:
            if current['id'] in seen:
                reason = 'Lineage cycle'; break
            seen.add(current['id'])
            if current.get('take_id') != shot['approved_take']:
                reason = 'Different take'; break
            if current.get('stage') not in STAGES:
                reason = 'Preview/editorial/unknown stage in lineage'; break
            if not current.get('full_frame') or current.get('crop') or current.get('post_geometry'):
                reason = 'Cropped or geometrically altered ancestor'; break
            parent = current.get('parent_id')
            if parent is None:
                if current['stage'] != 'native':
                    reason = 'Non-native stage has no parent'
                break
            if parent not in by_id:
                reason = 'Missing parent'; break
            current = by_id[parent]
        if not reason and not candidate.get('approved'):
            reason = 'Candidate not approved'
        if not reason and probe:
            try:
                data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
                    '-select_streams', 'v:0', '-show_entries', 'stream=width,height,nb_frames',
                    '-of', 'json', candidate['path']], text=True))['streams'][0]
                candidate.update(width=data['width'], height=data['height'])
                if data.get('nb_frames', 'N/A') != 'N/A':
                    candidate['frames'] = int(data['nb_frames'])
            except (OSError, subprocess.CalledProcessError, KeyError, ValueError) as error:
                reason = 'File probe failed: ' + str(error)
        native_start = int(candidate.get('native_start', 0))
        if not reason and not (native_start <= start and
                start + count <= native_start + int(candidate.get('frames', 0))):
            reason = 'Candidate does not cover requested native interval'
        if not reason and (int(candidate.get('width', 0)) <= 0 or int(candidate.get('height', 0)) <= 0):
            reason = 'Unknown dimensions'
        if reason:
            rejected[candidate['id']] = reason
        else:
            eligible.append(candidate)
    selected = max(eligible, key=lambda c: (int(c['width']) * int(c['height']),
                    {'native': 0, 'super_resolution': 1, 'second_pass': 2}[c['stage']]), default=None)
    return dict(shot_id=shot['shot_id'], selected_id=selected['id'] if selected else None,
        selected=selected, candidate_source_in=start-int(selected.get('native_start', 0)) if selected else None,
        rejected=rejected, files_probed=probe, lineage_is_declared_not_forensically_proven=True,
        visual_acceptance=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--probe', action='store_true', help='Read actual dimensions with ffprobe')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    if not isinstance(manifest.get('shots'), list) or not manifest['shots']:
        parser.error('Manifest must contain at least one shot')
    rows = [audit_shot(s, args.probe) for s in manifest['shots']]
    result = dict(shots=rows, all_have_eligible_source=all(r['selected_id'] for r in rows),
                  mode='file-probed' if args.probe else 'metadata-only', visual_acceptance=False)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text)
    return 0 if result['all_have_eligible_source'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
