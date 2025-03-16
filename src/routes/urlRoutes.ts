import { FastifyInstance } from "fastify";
import { verifyToken } from "../middlewares/verifyToken";
import { resolveShortUrl, shortenUrl } from "../controllers/urlController";

export async function urlRoutes(app: FastifyInstance) {
  app.post("/shorten", { preHandler: verifyToken }, shortenUrl);
  app.get("/:shortUrl", resolveShortUrl); // ✅ Handle redirection
}
