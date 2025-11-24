import sys
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, EVENT_TYPE_CREATED

class NewFileHandler(FileSystemEventHandler):
        """Handle only file-creation events."""
        def __init__(self,root_dir: Path, script_path: Path):
            self.root_dir = root_dir.resolve()
            self.script_path = script_path.resolve()
            super().__init__()

        def on_any_event(self, event):
            if event.event_type != EVENT_TYPE_CREATED:
                return 
            if event.is_directory:
                return

            file_path = Path(str(event.src_path)).resolve()

            try:
                relative = file_path.relative_to(self.root_dir)
            except ValueError:
                return

            parts = relative.parts
            if len(parts) < 2:
                return

            sub_folder = self.root_dir.joinpath(*parts[:-1])

            cmd = [
                sys.executable,
                str(self.script_path),
                str(sub_folder)
            ]
            print(f"[+] New file detected: {file_path}")
            print(f"    Triggering: {''.join(cmd)}")

            try:
                subprocess.Popen(cmd)
            except Exception as exc:
                print(f"[!] Failed to launch script: {exc}", file=sys.stderr)

def main(root_dir: str, script_path: str):
    root = Path(root_dir).resolve()
    script = Path(script_path).resolve()

    if not root.is_dir():
        sys.exit(f"Root directory does not exist: {root}")
    if not script.is_file():
        sys.exit(f"Script to execute not found: {script}")

    observer = Observer()
    handler = NewFileHandler(root, script)

    observer.schedule(handler, str(root), recursive=True)

    print(f"Watching '{root}' for new files...")
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n Stopping watcher...")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write( f"Usage: {sys.argv[0]} /data/downloads/sports /data/match-rename.py\n")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
