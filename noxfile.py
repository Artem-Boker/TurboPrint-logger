from pathlib import Path
from shutil import rmtree

from nox import Session, options
from nox_uv import session

options.default_venv_backend = "uv"
options.reuse_existing_virtualenvs = True
options.sessions = ["clean", "security", "lints", "formats", "tests", "builds", "docs"]
PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]
REPORT_FILES = [
    "pip-audit-report.json",
    "bandit-report.json",
    "coverage.xml",
    ".coverage",
]
CACHE_DIRS = [
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".benchmarks",
]
BUILD_DIRS = ["build", "dist", "docs/_build"]


@session(python=PYTHON_VERSIONS, uv_groups=["tests"])
def tests(s: Session) -> None:
    """Запуск тестов (coverage)."""
    s.run("pytest")


@session(uv_groups=["lints"])
def lints(s: Session) -> None:
    """Запуск статических анализаторов."""
    s.run("ruff", "check")
    s.run("ty", "check")


@session(uv_groups=["formats"])
def formats(s: Session) -> None:
    """Запуск форматеров кода (fix)."""
    s.run("ruff", "check", "--fix")
    s.run("ruff", "format")


@session(uv_groups=["formats"])
def check_format(s: Session) -> None:
    """Проверка форматирования без исправления."""
    s.run("ruff", "check")
    s.run("ruff", "format", "--check")


@session(uv_groups=["docs"])
def docs(s: Session) -> None:
    """Запуск генерации документации"""
    docs_source = Path("docs")
    if not docs_source.exists():
        s.error("docs source directory does not exist")
    docs_build = docs_source / "_build"
    if docs_build.exists():
        rmtree(docs_build)
    s.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@session(uv_groups=["security"])
def security(s: Session) -> None:
    """Комплексная проверка безопасности"""
    baseline = Path(".secrets.baseline")
    if baseline.exists():
        s.run("detect-secrets", "scan", "--baseline", str(baseline), "src")
    else:
        s.run("detect-secrets", "scan", "src")

    s.run("bandit", "-r", "src")
    s.run("pip-audit")


@session(uv_groups=["builds"])
def builds(s: Session) -> None:
    """Запуск сборки проекта"""
    for folder in ("build", "dist"):
        if Path(folder).exists():
            rmtree(folder)
    s.run("build", "--outdir", "dist")


def _get_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    if path.is_dir():
        size = 0
        for file in path.rglob("*"):
            if file.is_file():
                size += file.stat().st_size
        return size
    return 0


@session()
def clean(s: Session) -> None:
    """Очистка временных и служебных файлов."""
    total_size = 0

    for folder in [*BUILD_DIRS, *CACHE_DIRS]:
        path = Path(folder)
        if path.exists():
            total_size += _get_size(path)
            rmtree(path)

    for file in REPORT_FILES:
        file_path = Path(file)
        if file_path.exists():
            total_size += _get_size(file_path)
            file_path.unlink(missing_ok=True)

    for pycache in Path().rglob("__pycache__"):
        if pycache.exists():
            total_size += _get_size(pycache)
            rmtree(pycache)

    for pyc in Path().rglob("*.pyc"):
        if pyc.exists():
            total_size += _get_size(pyc)
            pyc.unlink(missing_ok=True)

    kb_size = total_size / 1024
    mb_size = total_size / 1024 / 1024

    s.log(f"Total size: {total_size} bytes // {kb_size:.2f} KB // {mb_size:.2f} MB")
