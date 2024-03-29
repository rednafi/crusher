#!/bin/python3
from __future__ import annotations

import subprocess
import sys

import toml


class UpdateDeps:
    """Automatically updating the dependencies, and revert if the tests fail."""

    def __init__(
        self, dep_file: str = "pyproject.toml", lock_file: str = "poetry.lock"
    ) -> None:
        self.dep_file = dep_file
        self.lock_file = lock_file

    @staticmethod
    def is_env_active() -> None:
        """Check if the virtual environment is active or not."""

        if sys.prefix == sys.base_prefix:
            print("Virtual environment is not active, exiting...\n")
            sys.exit(1)

        print("Virtual environment is active, proceeding...\n")

    @staticmethod
    def revert_changes(filename: str) -> None:
        print(f"Reverting file {filename} to HEAD...\n")
        subprocess.run(["git", "checkout", "HEAD", "--", filename])

    def update_deps(self) -> None:
        with open(self.dep_file, "r") as f:
            toml_dct = toml.loads(f.read())

            app_deps = toml_dct["tool"]["poetry"]["dependencies"]
            dev_deps = toml_dct["tool"]["poetry"]["dev-dependencies"]

            for k in app_deps:
                if k.lower() == "python":
                    continue
                subprocess.run(["poetry", "add", f"{k}@latest"])

            for k in dev_deps:
                if k.lower() == "python":
                    continue
                subprocess.run(["poetry", "add", f"{k}@latest", "--dev"])

    def run_tests(self) -> None:
        print("Running the tests...\n")

        result = subprocess.run(["pytest", "-v"], capture_output=True)

        if "FAILED" in str(result.stdout):
            print(
                f"Tests failed. Reverting {self.dep_file} and {self.lock_file} file..."
            )
            self.revert_changes(self.dep_file)
            self.revert_changes(self.lock_file)

        print("Tests ran successfully. Your dependencies are now up to date.")

    def execute(self) -> None:
        self.is_env_active()
        self.update_deps()
        self.run_tests()


if __name__ == "__main__":
    update = UpdateDeps()
    update.execute()
