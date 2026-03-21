import jwt from "jsonwebtoken";
import { Pool } from "pg";

const JWT_SECRET = process.env.JWT_SECRET || "zentra-dev-secret";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

export function getTokenFromRequest(req) {
  const auth = req.headers.authorization || "";
  return auth.startsWith("Bearer ") ? auth.slice(7) : null;
}

export async function verifyToken(req) {
  const token = getTokenFromRequest(req);

  if (!token) {
    return {
      ok: false,
      status: 401,
      body: {
        status: "NO_TOKEN",
        message: "Authorization token required"
      }
    };
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);

    const sessionResult = await pool.query(
      `
      SELECT id, status, expires_at
      FROM sessions
      WHERE token = $1
      LIMIT 1
      `,
      [token]
    );

    if (sessionResult.rows.length === 0) {
      return {
        ok: false,
        status: 401,
        body: {
          status: "SESSION_NOT_FOUND",
          message: "Session not found"
        }
      };
    }

    const session = sessionResult.rows[0];

    if (session.status !== "active") {
      return {
        ok: false,
        status: 401,
        body: {
          status: "SESSION_INACTIVE",
          message: "Session is not active"
        }
      };
    }

    if (session.expires_at && new Date(session.expires_at) < new Date()) {
      return {
        ok: false,
        status: 401,
        body: {
          status: "SESSION_EXPIRED",
          message: "Session expired"
        }
      };
    }

    return {
      ok: true,
      user: decoded,
      token
    };
  } catch (error) {
    return {
      ok: false,
      status: 401,
      body: {
        status: "INVALID_TOKEN",
        message: error.message
      }
    };
  }
}

export function requireRole(authResult, allowedRoles = []) {
  if (!authResult.ok) return authResult;

  if (!allowedRoles.length) {
    return {
      ok: true,
      user: authResult.user,
      token: authResult.token
    };
  }

  if (!allowedRoles.includes(authResult.user.role)) {
    return {
      ok: false,
      status: 403,
      body: {
        status: "FORBIDDEN",
        message: "Insufficient role"
      }
    };
  }

  return {
    ok: true,
    user: authResult.user,
    token: authResult.token
  };
}

export function setCors(res, methods = "GET, POST, OPTIONS") {
  res.setHeader("Access-Control-Allow-Origin", "https://zentrarisk.com");
  res.setHeader("Access-Control-Allow-Methods", methods);
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
        }
