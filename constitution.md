# Project Constitution: The Evolution of Todo

## Core Principle: Spec-Driven Development
This project strictly follows a Spec-Driven Development methodology. 

### Rule 1: The Spec is the Source of Truth
- No code shall be written without a corresponding specification.
- The Specification acts as the blueprint. The Code is merely the implementation of that blueprint.
- Validation is performed against the Spec, not just the Code.

### Rule 2: AI-Generated Implementation
- The goal is to act as a System Architect.
- Implementation details (syntax, boilerplate) are delegated to the AI.
- You must refine the prompt and the spec until the AI generates the correct code. Do not manually "fix" code if it deviates from the spec; fix the spec or the prompt.

### Rule 3: Iterative Evolution
- The project evolves in Phases (I to V).
- Each phase builds upon the previous one, introducing new complexity and technology.
- Archives of previous specs must be maintained.

## Workflow
1. **Draft Spec**: Define requirements, data models, and interface behavior in a markdown spec file.
2. **Review Plan**: Generate an implementation plan based on the spec.
3. **Generate Code**: Use the spec to generate the code.
4. **Verify**: Ensure the code meets the spec requirements.
