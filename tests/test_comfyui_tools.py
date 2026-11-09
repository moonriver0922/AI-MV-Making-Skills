import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/comfyui-mv-production/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceTests(unittest.TestCase):
    def test_highest_approved_same_take_with_uncropped_ancestry(self):
        audit = load('audit_sources')
        shot = dict(shot_id='door', approved_take='T01', source_in=0, frames=24, candidates=[
            dict(id='native', take_id='T01', stage='native', approved=True, full_frame=True,
                 width=1152, height=480, frames=24, path='native.mp4'),
            dict(id='second', take_id='T01', stage='second_pass', parent_id='native',
                 approved=True, full_frame=True, width=2304, height=960, frames=24, path='second.mp4'),
            dict(id='crop', take_id='T01', stage='editorial', parent_id='native',
                 approved=True, full_frame=False, width=6192, height=2580, frames=24, path='crop.mp4'),
            dict(id='sr_crop', take_id='T01', stage='super_resolution', parent_id='crop',
                 approved=True, full_frame=True, width=8000, height=3334, frames=24, path='sr_crop.mp4'),
            dict(id='other', take_id='T02', stage='native', approved=True, full_frame=True,
                 width=8000, height=3334, frames=24, path='other.mp4')])
        report = audit.audit_shot(shot)
        self.assertEqual(report['selected_id'], 'second')
        self.assertIn('sr_crop', report['rejected'])
        self.assertIn('other', report['rejected'])
        self.assertFalse(report['files_probed'])

    def test_missing_parent_and_cycle_are_rejected(self):
        audit = load('audit_sources')
        base = dict(approved=True, full_frame=True, take_id='T01', width=100, height=100,
                    frames=24, path='x.mp4', stage='second_pass')
        shot = dict(shot_id='bad', approved_take='T01', source_in=0, frames=24,
                    candidates=[dict(base, id='a', parent_id='b'), dict(base, id='b', parent_id='a'),
                                dict(base, id='c', parent_id='missing')])
        report = audit.audit_shot(shot)
        self.assertIsNone(report['selected_id'])
        self.assertEqual(len(report['rejected']), 3)

    def test_selected_interval_requires_real_coverage(self):
        audit = load('audit_sources')
        shot = dict(shot_id='range', approved_take='T01', source_in=100, frames=24,
                    candidates=[dict(id='short', take_id='T01', stage='native', approved=True,
                       full_frame=True, width=2304, height=960, frames=100, path='short.mp4')])
        self.assertIsNone(audit.audit_shot(shot)['selected_id'])


class WorkflowTests(unittest.TestCase):
    def test_binding_preserves_numeric_types(self):
        module = load('bind_workflow')
        value = module.bind({'width': '{{render.width}}', 'prefix': 'mv/{{shot_id}}'},
                            {'render': {'width': 1536}, 'shot_id': 'A01'})
        self.assertEqual(value, {'width': 1536, 'prefix': 'mv/A01'})

    def test_missing_binding_fails_before_queue(self):
        module = load('bind_workflow')
        with self.assertRaises(KeyError):
            module.bind('{{missing.parameter}}', {})

    def test_missing_node_is_reported_before_queue(self):
        module = load('inspect_comfy')
        result = module.inspect_graph({'1': {'class_type': 'MissingNode', 'inputs': {}}}, {})
        self.assertEqual(result['missing_nodes'], ['MissingNode'])
        self.assertFalse(result['ready'])

    def test_modern_combo_options_reject_missing_video(self):
        module = load('inspect_comfy')
        definitions = {'LoadVideo': {'input': {'required': {
            'file': ['COMBO', {'options': ['real-source.mp4']}]}}}}
        graph = {'1': {'class_type': 'LoadVideo', 'inputs': {'file': 'missing-source.mp4'}}}
        result = module.inspect_graph(graph, definitions)
        self.assertFalse(result['ready'])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class DeliveryTests(unittest.TestCase):
    def make(self, directory, audio_duration):
        path = Path(directory) / 'film.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
            'color=c=black:s=128x64:r=24:d=0.5', '-f', 'lavfi', '-i',
            'sine=frequency=440:sample_rate=48000:duration=' + str(audio_duration),
            '-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '1', '-c:a', 'aac',
            '-pix_fmt', 'yuv420p', '-y', str(path)], check=True)
        return path

    def test_audio_tail_loss_fails_even_when_picture_dimensions_pass(self):
        module = load('verify_delivery')
        with tempfile.TemporaryDirectory() as directory:
            report = module.verify(self.make(directory, .25), 128, 64, '24', 12)
            self.assertFalse(report['passed'])
            self.assertTrue(any('audio' in x.lower() for x in report['errors']))

    def test_complete_export_full_decode(self):
        module = load('verify_delivery')
        with tempfile.TemporaryDirectory() as directory:
            report = module.verify(self.make(directory, .5), 128, 64, '24', 12, decode=True)
            self.assertTrue(report['passed'], report['errors'])
            self.assertEqual(report['decode_exit_code'], 0)
            self.assertFalse(report['visual_acceptance'])


if __name__ == '__main__':
    unittest.main()
