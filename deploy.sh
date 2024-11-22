
cd /home/mudae/Documents/code/CPSC-362/auto-trader || exit

# pull latest code
git pull origin main

# install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# install frontent dependencies
npm install
npm run build

# Restart services
sudo systemctl user1000.service
sudo restart nginx