import Fastify from "fastify";
import dotenv from "dotenv";
import { registerRoutes } from "./routes";

dotenv.config();
const app = Fastify({ logger: true });

// ✅ Register all routes
registerRoutes(app);

const PORT = process.env.PORT || 5000;
app.listen({ port: Number(PORT), host: "0.0.0.0" }, (err, address) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`🚀 Server running at ${address}`);
});
