# Coding Standards

## General Principles
- Write self-documenting code with clear variable names
- Maximum function length: 50 lines
- DRY (Don't Repeat Yourself) - extract common logic
- Single Responsibility Principle for all functions/classes

## Python
- Follow PEP 8 style guide
- Use type hints for all function signatures
- All public functions must have docstrings (Google style)
- Prefer f-strings over .format() or %

## TypeScript/JavaScript
- Use TypeScript strict mode
- Prefer const over let, never use var
- Use async/await over raw Promises
- All exports must have JSDoc comments
- Use destructuring where it improves readability

## Error Handling
- Never use bare except/catch clauses
- Log errors with context
- Return meaningful error messages to users

