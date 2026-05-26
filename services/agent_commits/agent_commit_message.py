import asyncio
import subprocess
from agents import Agent, Runner, function_tool


def run_git_command(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return result.stderr.strip()

    return result.stdout.strip()


@function_tool
def get_git_history() -> str:
    """Return recent git commit history."""
    return run_git_command(["log", "--oneline", "-10"])


@function_tool
def get_staged_diff() -> str:
    """Return currently staged git diff."""
    return run_git_command(["diff", "--cached"])


@function_tool
def get_git_status() -> str:
    """Return current git status."""
    return run_git_command(["status", "--short"])


agent = Agent(
    name="Commit Message Agent",
    instructions="""
You are a senior software engineer helping with Git commits.

Your task:
1. Inspect git status.
2. Inspect staged diff.
3. Inspect recent git history.
4. Generate exactly one commit message.

Rules:
- Use Conventional Commits format.
- Add one relevant emoji at the beginning.
- Keep the title under 72 characters.
- Use English.
- Do not invent changes that are not visible in the diff.
- If there are no staged changes, say: "No staged changes found."

Allowed types:
feat, fix, docs, style, refactor, test, chore, ci, perf, build.

Format:
<emoji> <type>(optional-scope): <short summary>

Optional body:
- one or two bullets explaining what changed
""",
    tools=[get_git_status, get_staged_diff, get_git_history],
)


async def main() -> None:
    result = await Runner.run(
        agent,
        "Generate a commit message for the currently staged changes.",
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
