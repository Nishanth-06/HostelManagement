from twilio.rest import Client
from django.dispatch import receiver
from Canhost.models import *
from django.db.models.signals import post_save



@receiver(post_save,sender=Student)
def after_user_reg(sender,instance,created,**kwargs):
    if not created:

        # account_sid = 'ACe5540840f09d2c2fc9cabaa750c8d0e3'
        # auth_token = '60383f0809d64833f7cdbe1ebef6ac1a'
        # client = Client(account_sid, auth_token)
        # msg = f'''Dear {instance.student_name} You have registerd sucessfully for Canara Hostel Services Enjoy Your Hostel Life:) '''
        # message = client.messages \
        #     .create(
        #     body=msg,
        #     from_='(938) 300-4223',
        #     to=f'+91{instance.student_mbl_no}'
        # )

        print("------------------------------------")
        print(f'msg sent to {instance.student_mbl_no}')