import { FastifyInstance } from "fastify";
import supabase from "../config/db";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

// User Signup
// export async function signup(request: any, reply: any) {
//   const { email, password } = request.body;

//   if (!email || !password) {
//     return reply.status(400).send({ error: "Email and password are required!" });
//   }

//   // Hash the password
//   const hashedPassword = await bcrypt.hash(password, 10);

//   // Create user in Supabase Auth
//   const { data, error } = await supabase.auth.signUp({
//     email,
//     password: hashedPassword, // Supabase automatically hashes, but keeping for safety
//   });

//   if (error) {
//     return reply.status(400).send({ error: error.message });
//   }

//   return reply.send({ message: "User registered successfully!", data });
// }
// User Signup
export async function signup(request: any, reply: any) {
  const { email, password } = request.body;

  if (!email || !password) {
    return reply.status(400).send({ error: "Email and password are required!" });
  }

  // ❌ Remove manual password hashing (Supabase handles it internally)
  const { data, error } = await supabase.auth.signUp({
    email,
    password, // Send raw password (Supabase hashes it internally)
  });

  if (error) {
    return reply.status(400).send({ error: error.message });
  }

  return reply.send({ message: "User registered successfully!", data });
}


// User Login
export async function login(request: any, reply: any) {
  const { email, password } = request.body;

  if (!email || !password) {
    return reply.status(400).send({ error: "Email and password are required!" });
  }

  // Login with Supabase Auth
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return reply.status(400).send({ error: error.message });
  }

  // Generate JWT Token
  const token = jwt.sign({ userId: data.user?.id }, process.env.JWT_SECRET!, {
    expiresIn: "7d",
  });

  return reply.send({ message: "Login successful!", token, user: data.user });
}
