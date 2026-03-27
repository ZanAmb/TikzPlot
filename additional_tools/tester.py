import subprocess
import sys
from pathlib import Path


def run_python_files(directory: str, stop_on_error: bool = False):
    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise ValueError(f"Invalid directory: {directory}")

    py_files = sorted(dir_path.glob("*.py"))

    if not py_files:
        print("No .py files found.")
        return

    results = []

    for file in py_files:
        print(f"\n=== Running: {file.name} ===")

        try:
            result = subprocess.run(
                [sys.executable, str(file)],
                capture_output=True,
                text=True
            )

            print(result.stdout)
            if result.stderr:
                print("ERROR OUTPUT:")
                print(result.stderr)

            success = result.returncode == 0
            results.append((file.name, success))

            if not success and stop_on_error:
                print("Stopping due to error.")
                break

        except Exception as e:
            print(f"Failed to run {file.name}: {e}")
            results.append((file.name, False))

            if stop_on_error:
                break

    print("\n=== Summary ===")
    for name, success in results:
        status = "OK" if success else "FAIL"
        print(f"{name}: {status}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run all Python files in a directory.")
    parser.add_argument("directory", help="Directory containing .py files")
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop execution on first failure"
    )

    args = parser.parse_args()
    run_python_files(args.directory, args.stop_on_error)