# Frontend Guidelines

## Stack
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS

## Patterns
- Use server components by default.
- Client components only when needed (interactivity).
- API calls go through `/lib/api.ts`.
- Use "better-auth" for authentication.

## Component Structure
- `/components` - Reusable UI components.
- `/app` - Pages and layouts.
