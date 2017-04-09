sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
sudo /sbin/mkswap /var/swap.1
sudo chmod 600 /var/swap.1
sudo /sbin/swapon /var/swap.1

dd if=/dev/zero of=upload_test bs=400000000 count=1

python swap.py 500 &
python swap.py 500 &
python swap.py 500 &
python swap.py 500 &
python disk.py &
python spin.py &
