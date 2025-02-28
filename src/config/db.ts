import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";

dotenv.config();

// Validate environment variables
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  throw new Error("❌ Missing Supabase environment variables. Check .env file.");
}

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Test the connection
async function testConnection() {
  // Query the correct table in the auth schema
  const { data, error } = await supabase.auth.admin.listUsers();
  if (error) {
    console.error("❌ Supabase Connection Failed:", error);
  } else {
    console.log("✅ Supabase Connection Successful. Users count:", data?.users?.length);
  }
}

// Run connection test
testConnection();

export default supabase;
