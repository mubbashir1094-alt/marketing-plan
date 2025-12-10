# Deploying to Render

This guide walks you through deploying your FastAPI backend to Render.

## Prerequisites

- A [Render account](https://render.com) (free tier available)
- Your backend code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- Your Google API key ready

## Step 1: Push Your Code to Git

If you haven't already, initialize a git repository and push your code:

```bash
cd "c:\Users\Admin\OneDrive\Desktop\marketingplan backend\backend"
git init
git add .
git commit -m "Initial commit - FastAPI backend"
```

Create a `.gitignore` file to exclude sensitive files:

```
__pycache__/
*.pyc
.env
*.log
.DS_Store
```

Push to your preferred Git hosting service (GitHub, GitLab, etc.).

## Step 2: Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** and select **"Web Service"**
3. Connect your Git repository
4. Select your repository from the list

## Step 3: Configure Your Web Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `marketing-plan-backend` (or your preferred name) |
| **Region** | Choose closest to your users |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | Leave empty (or `backend` if it's in a subdirectory) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT` |

## Step 4: Add Environment Variables

In the "Environment Variables" section, add:

| Key | Value |
|-----|-------|
| `GOOGLE_API_KEY` | Your Google API key from `.env` file |
| `PYTHON_VERSION` | `3.11.0` |

**Important:** Copy the value from your `.env` file: `AIzaSyCbL25eXVOx2F67Uj46meMImYNgrYpRM1g`

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy your app
3. Wait for the deployment to complete (usually 2-5 minutes)
4. You'll receive a URL like: `https://marketing-plan-backend.onrender.com`

## Step 6: Test Your Deployment

Once deployed, test these endpoints:

### Health Check
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "llm_provider": "Google Generative AI (Gemini)",
  "api_key_configured": true
}
```

### API Info
```bash
curl https://your-app-name.onrender.com/
```

### Test Marketing Plan Generation
```bash
curl -X POST https://your-app-name.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{
    "businessName": "Test Business",
    "industry": "Technology",
    "productService": "SaaS Product",
    "targetAudience": "Small businesses",
    "budget": "$5000",
    "goals": "Increase brand awareness",
    "timeline": "3 months"
  }'
```

## Step 7: Update CORS Settings (Important!)

After deployment, update the CORS settings in `main.py` to restrict origins to your actual frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-app.vercel.app",
        "http://localhost:3000"  # for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push this change and Render will automatically redeploy.

## Troubleshooting

### Deployment Fails

- Check the "Logs" tab in Render dashboard
- Ensure all dependencies in `requirements.txt` are correct
- Verify Python version compatibility

### API Key Not Working

- Double-check the `GOOGLE_API_KEY` environment variable
- Ensure there are no extra spaces or quotes in the value
- Check the logs for any API-related errors

### 502 Bad Gateway

- Check that the start command is correct
- Verify the app is binding to `0.0.0.0:$PORT`
- Review the application logs in Render

## Free Tier Limitations

Render's free tier includes:

- ✅ 750 hours/month of running time
- ✅ Automatic HTTPS
- ✅ Auto-deploys from Git
- ⚠️ Spins down after 15 minutes of inactivity (cold starts)
- ⚠️ Limited to 512 MB RAM

For production use, consider upgrading to a paid plan for 24/7 uptime.

## Next Steps

1. Update your frontend to use the new backend URL
2. Set up custom domain (optional)
3. Monitor logs and performance
4. Consider adding health check endpoints for monitoring

## Useful Links

- [Render Dashboard](https://dashboard.render.com/)
- [Render Docs - Deploy FastAPI](https://render.com/docs/deploy-fastapi)
- [Your App Logs](https://dashboard.render.com/web/your-service-id/logs)
