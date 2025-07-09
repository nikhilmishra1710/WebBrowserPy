import subprocess


def format_code() -> None:
    """Run Black formatter."""
    subprocess.run(["black", "src/"])


def lint(fix: bool = False) -> None:
    """
    Run isort (import sorting) and ruff (linting) with optional auto-fixing.

    Args:
        fix: If True, attempts to automatically fix fixable issues.
             If False, only checks for issues (suitable for CI).

    Return:
        None
    """
    success = True

    print("=" * 50)
    print(f"{'FIXING' if fix else 'CHECKING'} CODE IMPORT SORTING AND LINTING ISSUES")
    # Run isort
    isort_status = subprocess.run(
        ["isort", "src/", "--apply" if fix else "--check-only"],
        capture_output=True,
        text=True,
    )

    if isort_status.returncode != 0:
        print("X Import sorting issues found:\n" + isort_status.stdout)
        if not fix:
            print("! Run poetry run lint-fix")
        else:
            print("\n! Some problem occured")
        success = False
    else:
        print("✓ No isort issues found")

    # Run Ruff
    ruff_cmd = ["ruff", "check", "src/"]
    if fix:
        ruff_cmd.append("--fix")

    ruff_status = subprocess.run(ruff_cmd, capture_output=True, text=True)

    if ruff_status.returncode != 0:
        print("X Ruff found some issues:\n" + ruff_status.stdout)
        if fix and "fixed" not in ruff_status.stdout:
            print("! Some issues require manaual attention")
        else:
            print("! Run 'poetry run lint-fix'")
        success = False
    else:
        print("✓ No Ruff issues found")

    if success:
        print("✓ All checks passed!")
    else:
        print("X Checks failed!")
    print("=" * 50)


def lint_fix() -> None:
    """
    Auto-fix linting and import sorting issues.
    Args:
        None
    Return:
        None
    """

    lint(fix=True)


def type_check() -> None:
    """
    Run mypy type checker on src folder.
    Args:
        None
    Return:
        None
    """
    print("=" * 50)
    print("TYPE CHECKING")
    type_check_status = subprocess.run(["mypy", "src/"], capture_output=True, text=True)

    if type_check_status.returncode != 0:
        print("X Some issues found:\n" + type_check_status.stdout)
        print("! Fix the issues before moving forward")
    else:
        print("✓ No issues found")
    print("=" * 50)
