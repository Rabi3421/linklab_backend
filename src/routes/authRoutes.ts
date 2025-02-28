import { FastifyInstance } from "fastify";
import { signup, login } from "../controllers/authController";

export async function authRoutes(app: FastifyInstance) {
  app.post("/auth/signup", signup);
  app.post("/auth/login", login);
}
