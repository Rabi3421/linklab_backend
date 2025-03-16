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
  // console.log("req:",req)
  const { shortUrl } = req.params as { shortUrl: string };
  console.log("shortUrl:",shortUrl)
  
  try {
    const link = await getUrl(shortUrl);
    console.log("link:",link)
    
    if (!link) {
      return reply.status(404).send({ error: "Short URL not found" });
    }

    // ✅ Redirect user to the original URL
    reply.redirect(301, link.original_url);
    // reply.send({ originalUrl: link.original_url });
  } catch (error) {
    reply.status(500).send({ error: "Internal Server Error" });
  }
}
