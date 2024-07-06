from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import traceback
import os
from dotenv import load_dotenv
from prometheus_client import Counter, start_http_server
from prometheus_flask_exporter import PrometheusMetrics

# Compteur pour le nombre total de requêtes
REQUESTS = Counter('http_request_total', 'Total number of requests')

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Fonction pour incrémenter le compteur de requêtes
def increment_request_counter():
    REQUESTS.inc()

def send_email(to_address, subject, body):
    from_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Attempting to send email...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erreur d'authentification SMTP: {e}")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP: {e}")
    except Exception as e:
        print(f"Erreur inconnue: {e}")
        traceback.print_exc()
        raise

def receive_email():
    try:
        print("Attempting to receive emails...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        print("Connected to IMAP server")
        try:
            mail.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
            print("Logged in to IMAP server")
            mail.select('inbox')
            print("Selected inbox")
        except imaplib.IMAP4.error as e:
            print(f"IMAP login error: {e}")
            raise

        print("Searching for emails...")
        status, data = mail.search(None, 'ALL')
        print("Search complete")
        mail_ids = data[0].split()
        print("Found {} emails".format(len(mail_ids)))

        emails = []

        for mail_id in mail_ids:
            print("Fetching email {}".format(mail_id))
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            print("Fetched email {}".format(mail_id))
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            subject = email_message['Subject']
            from_addr = email_message['From']
            body = ''

            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))

                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = email_message.get_payload(decode=True).decode()

            emails.append({
                'subject': subject,
                'from': from_addr,
                'body': body
            })

        print("Emails received successfully.")
        return emails
    except Exception as e:
        print(f"Failed to receive emails: {e}")
        traceback.print_exc()
        raise

@app.route("/")
def index():
    increment_request_counter()
    return render_template('index.html')
    

@app.route('/send', methods=['POST'])
def send_email_route():
    increment_request_counter()
    try:
        print("Received request to send email.")
        data = request.json
        to_address = data.get('to_address')
        subject = data.get('subject')
        body = data.get('body')
        if to_address and subject and body:
            send_email(to_address, subject, body)
            return jsonify({'message': 'Email envoyé!'})
        else:
            return jsonify({'message': 'Invalid request'}), 400
    except Exception as e:
        print(f"Error in /send route: {e}")
        traceback.print_exc()
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/receive', methods=['GET'])
def receive_email_route():
    increment_request_counter()
    try:
        print("Received request to receive emails.")
        emails = receive_email()
        return jsonify({'emails': emails})
    except Exception as e:
        print(f"Error in /receive route: {e}")
        traceback.print_exc()
        return jsonify({'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    # Démarrer un serveur HTTP pour exposer les métriques sur le port 8000
#    app.debug = True
    start_http_server(8001) #, addr='localhost')
    app.run(host='0.0.0.0', port=5001)