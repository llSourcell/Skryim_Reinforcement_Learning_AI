# Contributing

Thanks for your interest in contributing! Please follow these guidelines to help us keep things smooth and reproducible.

## Getting Started
- Use Python 3.10+ on macOS (tested).
- Install dependencies:
  - `pip install -r requirements.txt`
- Ensure you own Skyrim and can run it windowed at 1280x720 (top-left).

## Development
- Keep code clear and modular. Prefer descriptive names and early returns.
- Type-hint all functions where practical.
- Avoid adding large binaries or game assets to the repository.
- Put models, checkpoints, and TensorBoard logs under `skyrim_checkpoints*/` and `skyrim_ppo_tensorboard/` (already in `.gitignore`).

## Pull Requests
1. Create a feature branch.
2. Add/update tests or simple smoke checks when feasible.
3. Update documentation (README) if behavior or usage changes.
4. Open a PR with a clear description of the change and rationale.

## Reporting Issues
- Include OS, Python version, and steps to reproduce.
- Share logs and minimal scripts where possible.

## Code of Conduct
Be respectful and constructive. Disagreements are fine—disrespect is not.


