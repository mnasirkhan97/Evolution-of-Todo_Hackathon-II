import { createAuthClient } from "better-auth/react" // Make sure to import from react adapter if using hooks
// or just standard client if manual.
// "better-auth/react" is typical for Next.js

export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
})

export const { signIn, signUp, useSession } = authClient;
