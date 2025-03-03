import supabase from "../config/db";
import { Url } from "../models/url.model";
import { nanoid } from "nanoid";

// ✅ Function to create a shortened URL
export async function createShortUrl(originalUrl: string, title?: string, userId?: string) {
  const shortUrl = nanoid(8); // Generate a short URL (8-character)

  const { data, error } = await supabase
    .from("urls")
    .insert([{ 
      original_url: originalUrl, 
      short_url: shortUrl, 
      title, 
      user_id: userId 
    }])
    .select()
    .single();

  if (error) throw new Error(error.message);
  return data as Url;
}

// ✅ Function to get a URL by short code
export async function getUrl(shortUrl: string) {
  const { data, error } = await supabase
    .from("urls")
    .select("*")
    .eq("short_url", shortUrl)
    .single();

  if (error) return null;
  return data as Url;
}
