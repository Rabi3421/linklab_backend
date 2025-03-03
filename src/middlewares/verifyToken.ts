import { FastifyRequest, FastifyReply } from "fastify";
import jwt from "jsonwebtoken";

export async function verifyToken(request: FastifyRequest, reply: FastifyReply) {
  console.log("🟢 Headers received:", request.headers);

  const authHeader = request.headers.authorization;

  if (!authHeader) {
    console.log("❌ No Authorization header found");
    return reply.status(401).send({ error: "Unauthorized - Missing Authorization Header" });
  }

  if (!authHeader.startsWith("Bearer ")) {
    console.log("❌ Authorization header format is incorrect");
    return reply.status(401).send({ error: "Unauthorized - Invalid Token Format" });
  }

  const token = authHeader.split(" ")[1];
  console.log("🔵 Extracted Token:", token);

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    console.log("✅ Decoded Token:", decoded);

    // Attach user to request
    (request as any).user = decoded;
    console.log("✅ User attached to request:", (request as any).user);
  } catch (err) {
    console.error("❌ JWT Verification Failed:", err);
    return reply.status(401).send({ error: "Unauthorized - Invalid Token" });
  }
}
