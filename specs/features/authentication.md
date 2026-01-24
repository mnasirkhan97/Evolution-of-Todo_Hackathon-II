# Feature: Authentication

## Overview
We use **Better Auth** for secure, drop-in authentication for Next.js, with **JWT** strategy for FastAPI backend verification.

## Architecture
- **Frontend**: Better Auth runs in Next.js. Handles Login, Signup, Session management.
- **Backend**: Accepts JWT tokens in `Authorization: Bearer <token>` header.

## User Stories
- As a user, I can **sign up** with email/password.
- As a user, I can **log in** to access my tasks.
- As a user, I can **log out**.

## Technical Details
- **Shared Secret**: `BETTER_AUTH_SECRET` env var must match in Frontend and Backend.
- **Token**: Better Auth issues a JWT.
- **Middleware**: FastAPI middleware decodes JWT and injects `user` into request context.
