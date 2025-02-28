import { FastifyRequest, FastifyReply } from "fastify";
import jwt from "jsonwebtoken";

export async function verifyToken(request: FastifyRequest, reply: FastifyReply) {
  try {
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      return reply.status(401).send({ error: "Unauthorized! No token provided." });
    }

    const token = authHeader.split(" ")[1]; // Extract token after "Bearer "
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);

    // Attach user ID to request for further use
    (request as any).user = decoded;
  } catch (error) {
    return reply.status(401).send({ error: "Invalid or expired token." });
  }
}
