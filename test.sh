source install.sh
sudo rm database_test.db
sudo cp database.db database_test.db
python test_app.py