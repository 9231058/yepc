# In The Name Of God
# ========================================
# [] File Name : main.py
#
# [] Creation Date : 26-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .route import app


def main():
        app.run(host="0.0.0.0", port=8080)
