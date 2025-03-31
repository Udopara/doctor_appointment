#!/usr/bin/python3
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, get_email, prompt_for_credentials
import sqlite3
import re
from email.message import EmailMessage
import ssl
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
