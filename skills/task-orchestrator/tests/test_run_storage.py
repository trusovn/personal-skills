"""Filesystem faults at publication boundaries; application tests own transactions."""
import hashlib
import importlib.util
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    'task_orchestrator_run_storage', Path(__file__).parents[1] / 'scripts/run_storage.py')
storage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(storage)


class RunStorageTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_replacement_failure_preserves_previous_ledger_then_retry_replaces(self):
        path = self.root / 'ledger.json'
        path.write_bytes(b'{"revision":1}\n')
        with mock.patch.object(Path, 'replace', side_effect=OSError('interrupted replace')):
            with self.assertRaisesRegex(OSError, 'interrupted replace'):
                storage.atomic_write_json(path, {'revision': 2})
        self.assertEqual(b'{"revision":1}\n', path.read_bytes())
        # Replacement intentionally retains its historical unsynced temp protocol.
        self.assertEqual(1, len(list(self.root.glob('.*.tmp'))))
        storage.atomic_write_json(path, {'revision': 2})
        self.assertEqual(b'{\n  "revision": 2\n}\n', path.read_bytes())
        self.assertEqual({'revision': 2}, storage.read_json(path))
        self.assertEqual([], list(self.root.glob('.*.tmp')))

    def test_durable_publication_syncs_complete_file_before_link_and_directory_after(self):
        path = self.root / 'actor.json'
        content = b'{"operation":"actor-01"}'
        sync = os.fsync
        observed = []

        def observe_sync(descriptor):
            directory = stat.S_ISDIR(os.fstat(descriptor).st_mode)
            observed.append('directory' if directory else 'file')
            if directory:
                self.assertEqual(content, path.read_bytes())
            else:
                self.assertFalse(path.exists())
                self.assertEqual(content, next(self.root.glob('.*.tmp')).read_bytes())
            sync(descriptor)

        with mock.patch.object(storage.os, 'fsync', side_effect=observe_sync):
            storage.write_durable_exclusive(path, content)
        self.assertEqual(['file', 'directory'], observed)
        with self.assertRaises(FileExistsError):
            storage.write_durable_exclusive(path, b'conflicting bytes')
        self.assertEqual(content, path.read_bytes())
        self.assertEqual([], list(self.root.glob('.*.tmp')))

    def test_sync_failure_retains_only_published_bytes_and_exact_replay_rejects_conflict(self):
        for boundary in ('file', 'directory'):
            with self.subTest(boundary=boundary):
                path = self.root / f'{boundary}.json'
                sync = os.fsync

                def fail_sync(descriptor):
                    directory = stat.S_ISDIR(os.fstat(descriptor).st_mode)
                    if directory == (boundary == 'directory'):
                        raise OSError('interrupted sync')
                    sync(descriptor)

                with mock.patch.object(storage.os, 'fsync', side_effect=fail_sync):
                    with self.assertRaisesRegex(OSError, 'interrupted sync'):
                        storage.publish_or_reuse_bytes(path, b'complete bytes')
                self.assertEqual(boundary == 'directory', path.exists())
                self.assertEqual([], list(self.root.glob('.*.tmp')))
                storage.publish_or_reuse_bytes(path, b'complete bytes')
                before = path.stat().st_mtime_ns
                storage.publish_or_reuse_bytes(path, b'complete bytes')
                self.assertEqual(before, path.stat().st_mtime_ns)
                with self.assertRaisesRegex(ValueError, 'Conflicting prepared actor record'):
                    storage.publish_or_reuse_bytes(path, b'conflict')
                self.assertEqual(b'complete bytes', path.read_bytes())

    def test_record_replay_requires_valid_exact_bytes_without_repair(self):
        path = self.root / 'inspection.json'
        record = {'revision': 1}

        def validate(value):
            if value != record:
                raise ValueError('invalid inspection revision')

        synced = []
        sync = os.fsync

        def observe_sync(descriptor):
            synced.append(stat.S_ISDIR(os.fstat(descriptor).st_mode))
            sync(descriptor)

        with mock.patch.object(storage.os, 'fsync', side_effect=observe_sync):
            actual, digest = storage.publish_or_reuse_record(path, record, validate)
        self.assertEqual(record, actual)
        self.assertEqual(b'{"revision":1}', path.read_bytes())
        self.assertEqual(hashlib.sha256(b'{"revision":1}').hexdigest(), digest)
        self.assertEqual([False], synced)  # File sync only for legacy records.
        before = path.stat().st_mtime_ns
        self.assertEqual((actual, digest), storage.publish_or_reuse_record(path, record, validate))
        self.assertEqual(before, path.stat().st_mtime_ns)
        for raw, reason in ((b'{"revision": 1}\n', 'bytes contradict'),
                            (b'{"revision":2}', 'invalid inspection revision'),
                            (b'{', 'record is invalid')):
            with self.subTest(raw=raw):
                path.write_bytes(raw)
                with self.assertRaisesRegex(ValueError, reason):
                    storage.publish_or_reuse_record(path, record, validate)
                self.assertEqual(raw, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
