
cd /home/mudae/Documents/code/CPSC-362-auto-trader/ || exit

# pull latest code
git pull origin main

# install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd /home/mudae/Documents/code/CPSC-362-auto-trader/auto-trader || exit

# install frontent dependencies
npm install
npm run build

# Restart services ~only for aws machine
# sudo systemctl restart user1000.service
# sudo systemctl restart nginx