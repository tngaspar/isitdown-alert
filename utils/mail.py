import yagmail

class SendEmail:
    """ A class used to send emails
    """
    def __init__(self, sender_email: str, app_passwd: str, receivers: str or list):
        """Constructs class used to send emails to a given receiver

        Args:
            sender_email (str): The sender email address
            app_passwd (str): The sender email app password
            receivers (str or list): The receivers email addresses
        """
        self.yag = yagmail.SMTP(sender_email, app_passwd)
        if type(receivers) is str:
            receivers = [receivers]
        self.receivers = receivers
        
    def send(self, subject: str, body: str):
        """Sends email 

        Args:
            subject (str): Email subject
            body (str): Email body
        """
        self.yag.send(
            to=self.receivers,
            subject=subject,
            contents=body
        )
    