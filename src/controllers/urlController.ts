import { FastifyReply, FastifyRequest } from "fastify";
import { createShortUrl, getUrl, storeClick } from "../services/url.service";

export async function shortenUrl(req: FastifyRequest, reply: FastifyReply) {
  const { originalUrl, title, userId } = req.body as { originalUrl: string; title?: string; userId?: string };

  try {
    const newLink = await createShortUrl(originalUrl, title, userId);
    reply.send(newLink);
  } catch (error: any) {
    reply.status(500).send({ error: error.message });
  }
}


export async function resolveShortUrl(req: FastifyRequest, reply: FastifyReply) {
  const { shortUrl } = req.params as { shortUrl: string };

  try {
    const link = await getUrl(shortUrl);

    if (!link) {
      return reply.status(404).send({ error: "Short URL not found" });
    }

    // Get IP, User-Agent for tracking
    const ip = req.ip || req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    const userAgent = req.headers['user-agent'] || 'unknown';

    // Call the function to store click data
    await storeClick({
      urlId: link.id,
      ip: ip as string,
      userAgent
    });

    // ✅ Redirect user to the original URL
    reply.redirect(301, link.original_url);
    // reply.send({ originalUrl: link.original_url });
  } catch (error) {
    reply.status(500).send({ error: "Internal Server Error" });
  }
}
