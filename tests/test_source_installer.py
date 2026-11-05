"""Exercise source staging against real local Git, including failure cleanup."""
import json, pathlib, shutil, subprocess, sys, tempfile, unittest

class SourceInstallerTests(unittest.TestCase):
    def test_pinned_fetch_idempotence_dirty_refusal_and_failure_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root=pathlib.Path(directory); source=root/'origin';source.mkdir()
            def git(*args):
                return subprocess.check_output(['git','-C',str(source),*args],stderr=subprocess.DEVNULL,text=True).strip()
            git('init','-q');(source/'data').write_text('canonical source\n')
            git('add','.');git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture')
            commit=git('rev-parse','HEAD')
            (root/'scripts').mkdir();(root/'catalog').mkdir()
            shutil.copyfile(pathlib.Path(__file__).resolve().parents[1]/'scripts/install-sources.py',root/'scripts/install-sources.py')
            lock=root/'catalog/sources.lock.json';destination=root/'installed'
            def run(repository=str(source)):
                lock.write_text(json.dumps({'sources':[{'name':'fixture','repository':repository,'commit':commit}]}))
                return subprocess.run([sys.executable,str(root/'scripts/install-sources.py'),'--destination',str(destination)],capture_output=True,text=True)
            self.assertEqual(run().returncode,0)
            self.assertEqual((destination/'fixture/data').read_text(),'canonical source\n')
            self.assertEqual(run().returncode,0)
            (destination/'fixture/data').write_text('operator change')
            failed=run();self.assertNotEqual(failed.returncode,0);self.assertIn('Refusing to overwrite',failed.stderr)
            self.assertEqual((destination/'fixture/data').read_text(),'operator change')
            shutil.rmtree(destination/'fixture')
            failed=run(str(root/'missing-origin'));self.assertNotEqual(failed.returncode,0)
            self.assertEqual(list(destination.iterdir()),[])
            (destination/'fixture').symlink_to(source,target_is_directory=True)
            failed=run();self.assertNotEqual(failed.returncode,0);self.assertIn('Refusing symlink',failed.stderr)

if __name__=='__main__':unittest.main()
