export interface Url {
    id: string; // Unique identifier (UUID)
    created_at: Date; // Timestamp of creation
    original_url: string; // Long URL
    short_url: string; // Auto-generated short URL
    custom_url?: string; // User-defined short URL (optional)
    user_id?: string; // ID of the user who created the URL (optional)
    title?: string; // Title of the URL (optional)
    qr?: string; // QR code data (optional)
  }
  