yum -y install git
git clone https://github.com/ewmson/glowing-meme.git
cd glowing-meme
yum -y install gcc
yum -y install sysstat
systemctl enable sysstat
pip install -r requirements.txt
pip install --upgrade requests
nohup python eventloop.py </dev/null > hype.log 2>&1 &
