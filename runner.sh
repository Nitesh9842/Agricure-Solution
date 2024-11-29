# Install cloudflared
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
rm -rf cloudflared.deb log.txt

# Start cloudflared tunnel
sudo cloudflared service install eyJhIjoiYjM3MjBhOGFhMzU4YmY3NmFjZTE3MTg0ZGY0YmIwMmIiLCJ0IjoiYzI2NzM0NGYtZmNhYy00YmZmLWI0OWEtMGNkMWYxMmE4ZTBjIiwicyI6Ik16Z3pPRFV3TmpVdE1tRmhOUzAwTWpWbUxUaGpNMlV0TmpBeE1EVm1PVEU0TWpObCJ9

# Run the app
gunicorn app:app
