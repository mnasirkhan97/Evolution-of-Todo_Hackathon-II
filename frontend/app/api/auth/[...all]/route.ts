import { auth } from "@/lib/auth"; // We will create this
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
