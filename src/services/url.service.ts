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
      user_id: userId || null
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
    .or(`custom_url.eq.${shortUrl},short_url.eq.${shortUrl}`)
    .single();

  if (!data || error) throw new Error("Short URL not found");

  if (error) return null;
  return data as Url;
}

export async function storeClick({ urlId, ip, userAgent }: { urlId: string; ip: string; userAgent: string }) {
  try {
    // Fetch location details using an IP API
    const response = await fetch(`https://ipapi.co/json`);

    const { city, country_name: country } = await response.json();

    // Store the click data
    await supabase.from('clicks').insert({
      url_id: urlId,
      city:city,
      country: country,
      device: userAgent.includes('Mobile') ? 'mobile' : 'desktop',
    });

    console.log("Click recorded successfully!");
  } catch (error) {
    console.error("Error recording click:", error);
  }
}