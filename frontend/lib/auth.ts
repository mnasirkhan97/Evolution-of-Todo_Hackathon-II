import { betterAuth } from "better-auth";
import { pg } from "better-auth/adapters/pg";
import { Pool } from "pg";

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.DATABASE_URL?.includes("aws.neon.tech") ? { rejectUnauthorized: false } : false,
});

export const auth = betterAuth({
    database: pg(pool),
    emailAndPassword: {
        enabled: true,
    },
    secret: process.env.BETTER_AUTH_SECRET,
    // Add trusted origins to prevent CORS issues with auth
    trustedOrigins: ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
    session: {
        strategy: "jwt",
    }
});
