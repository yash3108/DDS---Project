python -m venv ddsvenv
call ddsvenv/Scripts/activate

pip install -r requirements.txt
python system_boot.py

deactivate