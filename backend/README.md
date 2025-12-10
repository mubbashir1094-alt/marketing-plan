# Marketing Plan Generator - Python Backend

FastAPI backend for the AI Marketing Plan Generator using open-source LLMs.

## Features

- 🚀 FastAPI - Modern, fast Python web framework
- 🤖 Multiple LLM Providers:
  - Together.ai (LLaMA 3)
  - Fireworks.ai (LLaMA 3, Mixtral)
  - Hugging Face Inference API
- 🔒 CORS enabled for frontend integration
- 📝 Auto-generated API documentation
- ⚡ Production-ready

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
LLM_PROVIDER=together
TOGETHER_API_KEY=your_api_key_here
```

### Get Free API Keys

**Together.ai** (Recommended):
1. Visit https://together.ai
2. Sign up for free account
3. Get $25 free credits
4. Copy API key from dashboard

**Fireworks.ai**:
1. Visit https://fireworks.ai
2. Sign up
3. Get free tier credits
4. Copy API key

**Hugging Face**:
1. Visit https://huggingface.co
2. Go to Settings → Access Tokens
3. Create new token
4. Free inference (rate-limited)

### 3. Run Locally

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Or using Python
python main.py
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## API Endpoints

### POST /generate

Generate a marketing plan.

**Request Body:**
```json
{
  "businessName": "Tech Startup Inc",
  "industry": "SaaS",
  "targetAudience": "Small businesses",
  "productService": "Project management software",
  "budget": "$10,000 - $20,000",
  "goals": "Get 1000 signups in 6 months",
  "timeline": "6 months",
  "competitors": "Asana, Monday.com",
  "uniqueSellingPoint": "AI-powered task automation"
}
```

**Response:**
```json
{
  "plan": "# COMPREHENSIVE MARKETING PLAN...",
  "provider": "together"
}
```

### GET /health

Check API health and configuration.

### GET /

API information and available endpoints.

## Deploy to Production

### Option 1: Render (Recommended)

1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service
4. Connect your repo
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `LLM_PROVIDER`
   - `TOGETHER_API_KEY` (or other provider key)
7. Deploy!

Your API will be at: `https://your-app.onrender.com`

### Option 2: Railway

1. Visit https://railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Add environment variables
5. Deploy

### Option 3: Hugging Face Spaces

1. Create new Space at https://huggingface.co/spaces
2. Choose "Docker" template
3. Upload your code
4. Add Dockerfile:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Option 4: Your Own VPS

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## LLM Provider Comparison

| Provider | Model | Free Tier | Speed | Quality |
|----------|-------|-----------|-------|---------|
| Together.ai | LLaMA 3 8B | $25 credits | Fast | Excellent |
| Fireworks.ai | LLaMA 3 / Mixtral | Free tier | Very Fast | Excellent |
| Hugging Face | LLaMA 3 8B | Rate-limited | Medium | Good |

## Switching Providers

Just change the `.env` file:

```env
# Use Together.ai
LLM_PROVIDER=together
TOGETHER_API_KEY=your_key

# Or use Fireworks
LLM_PROVIDER=fireworks
FIREWORKS_API_KEY=your_key

# Or use Hugging Face
LLM_PROVIDER=huggingface
HF_API_KEY=your_key
```

## Testing

Test with curl:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "businessName": "Test Business",
    "industry": "Technology",
    "targetAudience": "Developers",
    "productService": "API tool",
    "budget": "$5000",
    "goals": "100 users",
    "timeline": "3 months"
  }'
```

Or visit http://localhost:8000/docs for interactive testing.

## CORS Configuration

For production, update CORS origins in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    ...
)
```

## Troubleshooting

**API key not working?**
- Verify key is correct in `.env`
- Check you have credits remaining
- Try a different provider

**Slow responses?**
- Normal for first request (cold start)
- Consider paid tier for faster inference
- Try Fireworks.ai for better speed

**Rate limiting?**
- Hugging Face has rate limits on free tier
- Use Together.ai or Fireworks for production

## License

MIT


