# Repository instructions for Codex

Follow these instructions for every new commit in this repository.

- Put each new proof of concept in its own top-level directory named `descriptive-project-name-YYYY-MM-DD`. Use lowercase words separated by hyphens and an ISO date, following the predominant convention in [vishal-vazkar-poc-collection](https://github.com/vazkarvishal/vishal-vazkar-poc-collection). Keep related source, examples, tests, and documentation inside that directory.
- Use Conventional Commits for every commit message, including commits pushed to a branch: `<type>(<optional scope>): <imperative summary>`. Examples: `feat(property-watch): add listing evaluator` and `docs: describe repository conventions`. Use a standard type such as `feat`, `fix`, `docs`, `test`, `refactor`, or `chore`.
- Before committing, run the relevant checks for changed projects and review the staged files for generated output, credentials, and personal data.
