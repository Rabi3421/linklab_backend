import { FastifyInstance } from "fastify";
import { healthRoutes } from "./routes/health";
import { authRoutes } from "./routes/authRoutes"; // ✅ Import auth routes
import { userRoutes } from "./routes/userRoutes";
import { urlRoutes } from "./routes/urlRoutes";

export function registerRoutes(app: FastifyInstance) {
  app.register(healthRoutes);
  app.register(authRoutes); // ✅ Register auth routes
  app.register(userRoutes); // ✅ Protected user routes
  app.register(urlRoutes); // ✅ Register URL shortener API
}
