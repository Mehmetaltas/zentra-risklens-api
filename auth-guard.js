import jwt from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET || "zentra-dev-secret";

export function getTokenFromRequest(req) {
  const auth = req.headers.authorization || "";
  return auth.startsWith("Bearer ") ? auth.slice(7) : null;
}

export function verifyToken(req) {
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
    return {
      ok: true,
      user: decoded
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
    return { ok: true, user: authResult.user };
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
    user: authResult.user
  };
}

export function setCors(res, methods = "GET, POST, OPTIONS") {
  res.setHeader("Access-Control-Allow-Origin", "https://zentrarisk.com");
  res.setHeader("Access-Control-Allow-Methods", methods);
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
                }
