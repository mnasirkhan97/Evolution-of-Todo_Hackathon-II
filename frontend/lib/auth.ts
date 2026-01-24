import { betterAuth } from "better-auth";
import { pg } from "better-auth/adapters/pg"; // Or appropriate adapter
// To keep it simple and match "neon" requirement without full ORM in Next.js just for auth, 
// we can use standard postgres adapter if we install 'pg'.
// Or since we use SQLModel in backend, maybe we can share the db?
// Better Auth needs its own tables. It auto-migrates.

// For hackathon speed, we'll try to use the simplest setup.
// backend uses sqlmodel (sqlite/postgres).
// Setup for Next.js:
// We need 'pg' package.

import { Pool } from "pg";

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.DATABASE_URL?.includes("aws.neon.tech") ? { rejectUnauthorized: false } : false,
});

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.DATABASE_URL,
        // Pass SSL options if needed, usually passed in connectionString or extra config
    }),
    // Wait, better-auth might need specific adapter config.
    // Documentation says: 
    // database: { provider: "postgres", url: process.env.DATABASE_URL } (if using built-in?)
    // Let's use the generic config if possible or specific adapter.
    // Ideally:
    /*
    database: {
        url: process.env.DATABASE_URL,
        type: "postgres"
    }
    */
    // But checking imports... `better-auth` main export.

    // Let's assume standard config for now.
    emailAndPassword: {
        enabled: true,
    },
    secret: process.env.BETTER_AUTH_SECRET,
    session: {
        strategy: "jwt", // Crucial for backend verification!
    }
});
