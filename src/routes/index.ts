import { FastifyInstance } from "fastify";
import { authRoutes } from "./authRoutes";
import { userRoutes } from "./userRoutes";
import { healthRoutes } from "./health";

export function registerRoutes(app: FastifyInstance) {
  app.register(healthRoutes, { prefix: "/" }); // ✅ Health check route
  app.register(authRoutes, { prefix: "/auth" }); // ✅ Authentication routes
  app.register(userRoutes, { prefix: "/user" }); // ✅ Protected user routes
}
