from worker import celery
from app import app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from flask_sse import sse
import csv
import os
from datetime import datetime
import requests
from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML
import smtplib

@celery.task()
def export_posts_to_csv(user_id):
    from models import User
    user = User.query.get(user_id)
    posts = user.posts
    # create csv file of posts of current user and write to it
    path='static/csv/{}.csv'.format(user.id)
    # if folder doesn't exist, create it
    if not os.path.exists('static/csv'):
        os.makedirs('static/csv')
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'caption', 'imageURL', 'time'])
        for post in posts:
            writer.writerow([post.id, post.title, post.caption, post.imageURL, post.time])
    sse.publish({'path': path}, type='export_posts'+str(user.id))
    return path

@app.route('/export', methods=['GET'])
@jwt_required()
def export_posts():
    user_id = get_jwt_identity()
    job = export_posts_to_csv.delay(user_id)
    return {'jobId': job.id}


@celery.task()
def daily_reminder():
    from models import User
    link = 'https://chat.googleapis.com/v1/spaces/AAAA-IWyE9g/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=3TpvKR9K9426l-2O0E0daRuLG1znBN0rS4uUixWA4uk%3D'
    users = User.query.all()
    for user in users:
        # if latest post is not today
        posts = user.posts
        posts = sorted(posts, key=lambda post: post.time, reverse=True)
        if len(posts) == 0 or posts[0].time.date() != datetime.now().date():
            requests.post(link, json={ 'text': 'Hello, {}!\nKindly Login and post something today'.format(user.username) })


@app.route('/daily_reminder', methods=['GET'])
def daily_reminder_route():
    # ONLY FOR TESTING, TO BE RUN AUTOMATICALLY
    job = daily_reminder.delay()
    return {'jobId': job.id}

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # send daily reminder to all users at 19:00
    sender.add_periodic_task(crontab(hour=19, minute=0, day_of_week='*'), daily_reminder.s())

@celery.task()
def monthly_report():
    from models import User, Post, Comment, Vote
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    users = User.query.all()
    posts = Post.query.all()
    comments = Comment.query.all()
    votes = Vote.query.all()
    # create report
    with open('templates/monthly.html') as file:
        template=Template(file.read())
        htmlstring = template.render(users=users, posts=posts, comments=comments, votes=votes)
        html = HTML(string=htmlstring)
        filename = 'static/pdf/{}.pdf'.format(datetime.now().strftime('%Y-%m-%d'))
        if not os.path.exists('static/pdf'):
            os.makedirs('static/pdf')
        html.write_pdf(filename)
        msg = MIMEMultipart()
        msg['From'] = app.config['SMTP_SERVER_EMAIL']
        msg['To'] = 'admin@localhost'
        msg['Subject'] = 'Monthly Report'
        msg.attach(MIMEText(htmlstring, 'html'))
        with open(filename, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))
        msg.attach(attachment)
        server = smtplib.SMTP(host=app.config['SMTP_SERVER_HOST'], port=app.config['SMTP_SERVER_PORT'])
        server.login(app.config['SMTP_SERVER_EMAIL'], app.config['SMTP_SERVER_PASSWORD'])
        server.send_message(msg)
        server.quit()

@app.route('/monthly_report', methods=['GET'])
def monthly_report_route():
    # ONLY FOR TESTING, TO BE RUN AUTOMATICALLY
    job = monthly_report.delay()
    return {'jobId': job.id}