# Deploying codeX to Streamlit Cloud

This guide provides detailed instructions for deploying your codeX application to Streamlit Cloud.

## Prerequisites

- A GitHub account
- Your codeX project code pushed to a GitHub repository
- Basic knowledge of Git commands

## Step 1: Prepare Your Code for Deployment

1. Ensure your app is working correctly locally by running:

   ```
   streamlit run app.py
   ```

2. Verify all the required packages are listed in `requirements.txt`:

   ```
   streamlit==1.24.0
   openai==0.27.8
   pandas==2.0.3
   numpy==1.24.3
   Pillow==9.5.0
   ```

3. Make sure `runtime.txt` specifies a Python version supported by Streamlit Cloud:
   ```
   python-3.9.18
   ```

## Step 2: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in.
2. Click on the "+" icon in the upper right corner and select "New repository".
3. Name your repository (e.g., "codex-app").
4. Choose visibility (public or private).
5. Click "Create repository".

## Step 3: Push Your Code to GitHub

If you're setting up a new repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

If you're updating an existing repository:

```bash
git add .
git commit -m "Ready for deployment"
git push
```

## Step 4: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud).
2. Sign in with your GitHub account.
3. Click "New app".
4. Select your repository from the list.
5. Configure your app:

   - Repository: Select your repository
   - Branch: main (or your preferred branch)
   - Main file path: app.py
   - App URL: Choose a custom URL or use the default
   - Python version: Should match your runtime.txt
   - Advanced settings:
     - Set any environment variables needed (e.g., OPENAI_API_KEY)

6. Click "Deploy".
7. Wait for deployment to complete (usually 2-5 minutes).

## Step 5: Test Your Deployed App

1. Once deployed, Streamlit Cloud will provide you with a URL to access your application.
2. Open the URL in your browser and verify all functionality works correctly.
3. Test the login, code editor, and chatbot features.

## Troubleshooting

- **Application Error**: Check the logs in the Streamlit Cloud dashboard.
- **Missing Dependencies**: Verify all dependencies are listed in requirements.txt.
- **Environment Variables**: Ensure all required environment variables are set in the Streamlit Cloud settings.
- **Performance Issues**: Consider optimizing your code for better performance in production.

## Updating Your Deployed App

Whenever you push changes to your GitHub repository, Streamlit Cloud will automatically redeploy your application with the new changes.

To update your app:

1. Make your code changes locally.
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Streamlit Cloud will detect the changes and redeploy your app automatically.

## Custom Domain (Optional)

Streamlit Cloud allows you to use a custom domain for your app:

1. In the Streamlit Cloud dashboard, navigate to your app settings.
2. Under "Custom domain", enter your domain name.
3. Follow the DNS configuration instructions provided.

## Monitoring and Analytics

1. Streamlit Cloud provides basic analytics in the dashboard.
2. For more detailed analytics, consider integrating Google Analytics or a similar service.
