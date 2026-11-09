"""Check encoded picture AND audio duration; decode is explicit and never visual acceptance."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import subprocess


def verify(path, width, height, fps, frames, decode=False, silent=False):
    metadata = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))
    video = next((s for s in metadata['streams'] if s['codec_type'] == 'video'), None)
    audios = [s for s in metadata['streams'] if s['codec_type'] == 'audio']
    errors = []
    expected_seconds = frames / float(Fraction(fps))
    tolerance = max(1 / float(Fraction(fps)), .02)
    if video is None:
        errors.append('Video stream missing')
    else:
        if (video['width'], video['height']) != (width, height):
            errors.append('Video dimensions differ from delivery specification')
        if Fraction(video['avg_frame_rate']) != Fraction(fps):
            errors.append('Video frame rate differs from specification')
        if video.get('nb_frames', 'N/A') != 'N/A' and int(video['nb_frames']) != frames:
            errors.append('Video frame count differs from specification')
        if abs(float(video.get('duration', -1)) - expected_seconds) > tolerance:
            errors.append('Video duration differs from expected complete film')
        if video.get('sample_aspect_ratio', '1:1') != '1:1':
            errors.append('Non-square pixels; verify intended display aspect')
    if not silent and not audios:
        errors.append('Audio stream missing')
    for audio in audios:
        if abs(float(audio.get('duration', -1)) - expected_seconds) > tolerance:
            errors.append('Audio duration differs from expected complete soundtrack')
    decode_code, decoded_frames = None, None
    if decode:
        result = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-nostats', '-threads', '4',
            '-i', str(path), '-map', '0:v:0', '-map', '0:a?', '-progress', 'pipe:1',
            '-f', 'null', '-'], capture_output=True, text=True)
        decode_code = result.returncode
        counts = [int(line.split('=', 1)[1]) for line in result.stdout.splitlines() if line.startswith('frame=')]
        decoded_frames = max(counts, default=0)
        if decode_code != 0 or 'progress=end' not in result.stdout:
            errors.append('Full decode failed: ' + result.stderr[-1000:])
        if decoded_frames != frames:
            errors.append('Decoded video frame count differs from expected film')
    elif video and video.get('nb_frames', 'N/A') == 'N/A':
        errors.append('Unknown frame count; use --decode to establish it')
    return dict(file=str(path), expected_seconds=expected_seconds, expected_frames=frames,
        passed=not errors, errors=errors, decode_requested=decode, decode_exit_code=decode_code,
        decoded_video_frames=decoded_frames, visual_acceptance=False,
        music_content_not_compared=True, streams=metadata['streams'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--height', type=int, required=True)
    parser.add_argument('--fps', default='24')
    parser.add_argument('--frames', type=int, required=True)
    parser.add_argument('--decode', action='store_true')
    parser.add_argument('--silent', action='store_true', help='Explicitly allow a silent visual-only export')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.frames <= 0 or Fraction(args.fps) <= 0:
        parser.error('Positive frame count and frame rate required')
    result = verify(args.video, args.width, args.height, args.fps, args.frames, args.decode, args.silent)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
