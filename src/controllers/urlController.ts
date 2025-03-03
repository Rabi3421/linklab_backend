import { FastifyReply, FastifyRequest } from "fastify";
import { createShortUrl, getUrl } from "../services/url.service";

export async function shortenUrl(req: FastifyRequest, reply: FastifyReply) {
  const { originalUrl, title, userId } = req.body as { originalUrl: string; title?: string; userId?: string };

  try {
    const newLink = await createShortUrl(originalUrl, title, userId);
    reply.send(newLink);
  } catch (error:any) {
    reply.status(500).send({ error: error.message });
  }
}

export async function resolveShortUrl(req: FastifyRequest, reply: FastifyReply) {
  const { shortUrl } = req.params as { shortUrl: string };

  const link = await getUrl(shortUrl);
  if (!link) return reply.status(404).send({ error: "Short URL not found" });

  reply.redirect(link.original_url);
}
