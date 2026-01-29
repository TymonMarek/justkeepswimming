import logging
import platform
import subprocess
from pathlib import Path

import rich.logging
from rich.progress import Progress

LOG_FILE_PATH: str = "dist/build.log"
VENV_PYTHON: str = (
    ".venv/bin/python"
    if platform.system() != "Windows"
    else ".venv\\Scripts\\python.exe"
)
COMPILER: str = "nuitka"
COMPILER_ARGUMENTS: list[str] = [
    "--standalone",  # Create a standalone executable
    "--output-dir=dist",  # Output directory
    f"--output-filename=justkeepswimming{
        '.exe' if platform.system() == 'Windows' else ''
    }",  # Output filename
    "--windows-icon-from-ico=assets/icon.png",  # Windows icon
    "--macos-app-icon=assets/icon.png",  # macOS icon
    "--linux-icon=assets/icon.png",  # Linux icon
    "--assume-yes-for-downloads",  # Automatically agree to downloads
    "--deployment",  # Optimize for deployment
    "--product-name=JustKeepSwimming",  # Product name
    "--product-version=1.0.0",  # Product version
    "--file-version=1",  # File version
    '--file-description="A game about a small fish in the deep sea."',
    '--copyright="(c) 2026 Tymon Marek"',  # Copyright
    "--include-data-dir=assets=assets",  # Include assets directory
]
ENTRY_POINT = "src/justkeepswimming"

logging.basicConfig(
    level=logging.DEBUG,
    format="[bold cyan]%(name)s[/] %(message)s",
    handlers=[
        rich.logging.RichHandler(
            rich_tracebacks=True,
            show_time=False,
            show_level=False,
            markup=True)],
)
logger = logging.getLogger(__package__)


def build() -> None:
    logger.info("Starting build process...")

    with Progress() as progress:
        preparing_task = progress.add_task("[cyan]Preparing...", total=1)
        process = subprocess.Popen(
            [VENV_PYTHON, "-m", COMPILER, *COMPILER_ARGUMENTS, ENTRY_POINT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        progress.update(preparing_task, advance=1)
        progress.remove_task(preparing_task)
        compiling_task = progress.add_task("[cyan]Compiling...", total=None)
        compiler_logger = logging.getLogger(COMPILER.capitalize())
        dist_path = Path("dist")
        dist_path.mkdir(exist_ok=True)
        log_file = open(LOG_FILE_PATH, "w")
        if process.stdout:
            for line in process.stdout:
                compiler_logger.debug(line.strip())
                log_file.write(line)
        log_file.close()
        returncode = process.wait()
        progress.update(compiling_task, total=1, completed=1)
        if returncode != 0:
            raise subprocess.CalledProcessError(
                returncode,
                [VENV_PYTHON, "-m", COMPILER, *COMPILER_ARGUMENTS, ENTRY_POINT],
            )
        progress.remove_task(compiling_task)
        cleaning_task = progress.add_task("[cyan]Finalizing...", total=1)
        process.wait()
        progress.update(cleaning_task, advance=1)
        progress.remove_task(cleaning_task)
    logger.info("Build process completed.")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
