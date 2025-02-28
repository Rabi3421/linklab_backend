import { FastifyInstance } from "fastify";
import { healthRoutes } from "./routes/health";
import { authRoutes } from "./routes/authRoutes"; // ✅ Import auth routes

export function registerRoutes(app: FastifyInstance) {
  app.register(healthRoutes);
  app.register(authRoutes); // ✅ Register auth routes
}