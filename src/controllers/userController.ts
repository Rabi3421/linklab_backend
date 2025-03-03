import { FastifyRequest, FastifyReply } from "fastify";
import supabase from "../config/db"; // ✅ Ensure correct Supabase import

export async function getUserProfile(request: FastifyRequest, reply: FastifyReply) {
  try {
    const userId = (request as any).user?.userId;

    if (!userId) {
      return reply.status(401).send({ error: "Unauthorized" });
    }
    const { data, error } = await supabase.auth.admin.getUserById(userId);;

    if (error || !data?.user) {
      return reply.status(500).send({ error: "Failed to fetch user profile" });
    }

    return reply.send({
      message: "User profile fetched successfully",
      user: data.user,
    });
  } catch (error) {
    return reply.status(500).send({ error: "Internal server error" });
  }
}
