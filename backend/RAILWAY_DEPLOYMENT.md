# Deploying to Railway

This guide walks you through deploying your FastAPI backend to Railway.

## Why Railway?

- ✅ Simpler deployment process than Render
- ✅ Generous free tier ($5 credit/month)
- ✅ Auto-detects FastAPI applications
- ✅ Better developer experience
- ✅ Faster cold starts

## Prerequisites

- A [Railway account](https://railway.app) (sign up with GitHub for easiest setup)
- Your code pushed to GitHub: https://github.com/mubbashir1094-alt/marketing-plan
- Your Google API key ready

## Step 1: Create a New Project on Railway

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account (if first time)
5. Search for and select: `geniusaidigital-pixel/marketingplan-backend`

## Step 2: Railway Auto-Configuration

Railway will automatically:
- ✅ Detect it's a Python/FastAPI application
- ✅ Install dependencies from `requirements.txt`
- ✅ Set up the build environment

**Railway will auto-detect the start command from your code!** If it doesn't, the start command is:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
```

## Step 3: Add Environment Variables

1. In your Railway project, click on your service
2. Go to the **"Variables"** tab
3. Click **"New Variable"**
4. Add the following:

| Variable Name | Value |
|---------------|-------|
| `GOOGLE_API_KEY` | `your-google-api-key-here` |
| `PORT` | `8000` |

## Step 4: Deploy

1. Railway will automatically deploy your app
2. Wait 2-3 minutes for the build and deployment to complete
3. You'll see logs in real-time showing the deployment progress

## Step 5: Get Your Public URL

1. In your Railway service, go to the **"Settings"** tab
2. Scroll down to **"Networking"** or **"Domains"**
3. Click **"Generate Domain"**
4. Railway will give you a URL like: `https://marketing-plan-production.up.railway.app`

## Step 6: Test Your Deployment

Once deployed, test these endpoints:

### Health Check
```bash
curl https://your-app-name.up.railway.app/health
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
curl https://your-app-name.up.railway.app/
```

### Test Marketing Plan Generation
```bash
curl -X POST https://your-app-name.up.railway.app/generate \
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

### Test Blog Generation
```bash
curl -X POST https://your-app-name.up.railway.app/generate-blog \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Digital Marketing Tips",
    "targetKeyword": "digital marketing",
    "targetAudience": "Small business owners",
    "blogLength": "1000-1500",
    "tone": "professional"
  }'
```

## Step 7: Update CORS Settings (Important!)

After deployment, update the CORS settings in `main.py` to include your Railway URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app-name.up.railway.app",
        "https://your-frontend-app.vercel.app",  # Add your frontend URL
        "http://localhost:3000"  # for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push the change - Railway will automatically redeploy.

## Railway Free Tier

Railway provides:
- ✅ $5 of free credit per month
- ✅ No sleep/spin down (unlike Render's free tier!)
- ✅ 512 MB RAM
- ✅ 1 GB Disk
- ✅ Shared CPU

**Note:** Once you use up the $5 credit, the service will pause until next month. For production, consider adding a payment method.

## Troubleshooting

### Deployment Fails

- Check the **"Deployments"** tab for error logs
- Ensure `requirements.txt` has all dependencies
- Verify environment variables are set correctly

### API Key Not Working

- Double-check the `GOOGLE_API_KEY` variable in Railway dashboard
- Make sure there are no extra spaces in the value
- Restart the deployment after adding variables

### 502 Bad Gateway

- Check that the app is binding to `0.0.0.0:$PORT`
- Review application logs in Railway dashboard
- Ensure gunicorn is properly installed in requirements.txt

## Monitoring and Logs

- **View Logs**: Click on your service → "Deployments" tab → Select the latest deployment
- **Metrics**: Railway provides CPU, Memory, and Network metrics in the "Metrics" tab
- **Restart Service**: Settings tab → "Restart" button

## Advantages of Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| **Free Tier** | $5/month credit | 750 hours/month |
| **Cold Starts** | None | 15min inactivity = sleep |
| **Setup** | Auto-detection | Manual configuration |
| **Logs** | Real-time, easy access | Good but less intuitive |
| **Deployment Speed** | Fast | Moderate |

## Next Steps

1. ✅ Deploy your backend to Railway
2. ✅ Generate and test your public URL
3. ✅ Update frontend to use the Railway backend URL
4. ✅ Update CORS settings
5. Consider adding a custom domain (optional)

## Useful Links

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway Docs - Deploy FastAPI](https://docs.railway.app/guides/fastapi)
- [Your GitHub Repo](https://github.com/geniusaidigital-pixel/marketingplan-backend)

Railway makes deployment super simple - just connect your repo and you're done! 🚀
