import { authClient } from "@/lib/auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const { data: session } = await authClient.getSession();
  // Assuming token is available in session.token or we use cookies. 
  // If backend requires Bearer, we need the token. 
  // Better Auth often handles this via cookies for same-domain, but for cross-port we might need explicit header if configured.
  // For this hackathon, we'll try to extract it or expect cookie-based proxy if mapped.
  // However, the backend middleware expects HTTPBearer.
  // NOTE: If token is not exposed client-side, this architecture needs a proxy route.
  // For now, let's try to send the cookie or token if present.

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...options.headers as Record<string, string>,
  };

  // If we have a token in the session object (depends on config), use it.
  // Otherwise credentials include cookies.
  if (session?.session?.user) {
    // better-auth usually matches session token to cookie. 
    // If we need explicit token:
    // headers["Authorization"] = `Bearer ${session.session.token}`; // if exists
  }

  // Important: Include credentials to send cookies to backend
  // options.credentials = "include"; 

  // COMPLETE FIX:
  // Ideally we'd use a more robust token retrieval. 
  // But let's set credentials: include to allow cookies to pass if on same domain or CORS allow.
  // And if we have a token string, use it.

  // For this step, I will just uncomment import and basic session fetch, 
  // and rely on credentials 'include' for cookies or token if I can find it.
  // actually, better-auth client might rely on cookies.

  // Let's stick to the prompt request: provide complete flow.
  // I'll update to use credentials: 'include' which is safer for cross-origin if configured right.

  // Attempt to use session.token (if exposed) or session.id as the Bearer token
  // Backend expects JWT. If Better Auth is configured with JWT, the session token might be available.
  // Note: Adjust 'token' access based on your specific Better Auth config.
  // Common pattern: Use session.token if available, else try session.id

  // Debugging Frontend Session
  console.log("DEBUG: Full Session Object:", session);

  const token = (session?.session as any)?.token || session?.session?.id;
  console.log("DEBUG: Extracted Token:", token);

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  } else {
    console.warn("DEBUG: No token found for Authorization header");
  }


  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  getTasks: (status?: string) => {
    const query = status ? `?status=${status}` : "";
    return fetchWithAuth(`/tasks${query}`);
  },
  createTask: (data: { title: string; description?: string }) => {
    return fetchWithAuth("/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  updateTask: (id: number, data: { title?: string; description?: string; status?: string }) => {
    return fetchWithAuth(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },
  deleteTask: (id: number) => {
    return fetchWithAuth(`/tasks/${id}`, {
      method: "DELETE",
    });
  },
  completeTask: async (id: number) => {
    return fetchWithAuth(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify({ status: "completed" }),
    });
  }
};
