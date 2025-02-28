📦 linkmancer-backend
 ┣ 📂 src
 ┃ ┣ 📂 config
 ┃ ┃ ┣ 📜 database.ts         # PostgreSQL (Supabase) connection
 ┃ ┃ ┣ 📜 redis.ts            # Redis connection
 ┃ ┃ ┗ 📜 env.ts              # Load environment variables
 ┃ ┣ 📂 routes
 ┃ ┃ ┣ 📜 index.ts            # Main route loader
 ┃ ┃ ┣ 📜 health.ts           # Base API health check
 ┃ ┃ ┗ 📜 link.ts             # Link shortener APIs
 ┃ ┣ 📂 controllers
 ┃ ┃ ┣ 📜 link.controller.ts  # Link management logic
 ┃ ┃ ┗ 📜 user.controller.ts  # User authentication logic
 ┃ ┣ 📂 services
 ┃ ┃ ┣ 📜 link.service.ts     # Handles DB logic for links
 ┃ ┃ ┣ 📜 user.service.ts     # Handles DB logic for users
 ┃ ┃ ┗ 📜 cache.service.ts    # Caching logic using Redis
 ┃ ┣ 📂 models
 ┃ ┃ ┣ 📜 link.model.ts       # Link schema/model
 ┃ ┃ ┗ 📜 user.model.ts       # User schema/model
 ┃ ┣ 📜 index.ts              # Entry point (Fastify server)
 ┃ ┣ 📜 app.ts                # App setup with Fastify
 ┃ ┗ 📜 routes.ts             # Register routes globally
 ┣ 📂 tests
 ┃ ┣ 📜 link.test.ts          # API tests for link shortener
 ┃ ┗ 📜 user.test.ts          # API tests for authentication
 ┣ 📂 scripts
 ┃ ┗ 📜 seed.ts               # Script to seed database
 ┣ 📂 docs
 ┃ ┗ 📜 api-docs.md           # API documentation (Swagger/Postman)
 ┣ 📜 .env                    # Environment variables
 ┣ 📜 .gitignore              # Ignore unnecessary files
 ┣ 📜 package.json            # Dependencies and scripts
 ┣ 📜 tsconfig.json           # TypeScript config
 ┣ 📜 README.md               # Project documentation
 ┗ 📜 nodemon.json            # Nodemon config for development

📌 Explanation of Key Folders
1️⃣ config/ (Configuration Files)
database.ts → Connects to Supabase PostgreSQL
redis.ts → Connects to Redis
env.ts → Loads environment variables
2️⃣ routes/ (API Routes)
index.ts → Registers all API routes
health.ts → Base API to check if the server is running
link.ts → Routes for URL shortener APIs
3️⃣ controllers/ (Business Logic)
link.controller.ts → Handles link-related API logic
user.controller.ts → Handles authentication logic
4️⃣ services/ (Database & Cache Logic)
link.service.ts → Handles PostgreSQL operations for links
user.service.ts → Handles PostgreSQL operations for users
cache.service.ts → Implements Redis caching
5️⃣ models/ (Database Models)
link.model.ts → Defines Link schema
user.model.ts → Defines User schema
6️⃣ tests/ (Unit & API Testing)
link.test.ts → Tests link APIs
user.test.ts → Tests authentication APIs
