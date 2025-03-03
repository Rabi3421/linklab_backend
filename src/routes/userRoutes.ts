import { FastifyInstance } from "fastify";
import { verifyToken } from "../middlewares/verifyToken";
import { getUserProfile } from "../controllers/userController";

export async function userRoutes(app: FastifyInstance) {
  app.get("/user/profile", { preHandler: verifyToken }, getUserProfile);
}
