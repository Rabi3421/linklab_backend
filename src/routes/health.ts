import { FastifyInstance } from 'fastify';

export async function healthRoutes(app: FastifyInstance) {
  app.get('/', async (_, reply) => {
    return reply.redirect(302, 'https://linklab.in/');
  });
}
