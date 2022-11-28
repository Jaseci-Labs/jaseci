from django.db import models
import os.path
from ..settings import JSX_STRIPE_DIR


STRIPE_EVENTS_FILE = os.path.join(JSX_STRIPE_DIR, "stripe_events.txt")

COLOR_CHOICES = ()
STRIPE_EVENTS = []

if not os.path.isfile(STRIPE_EVENTS_FILE):
    print("File does not exist.")
else:
    f = open(STRIPE_EVENTS_FILE, "r")
    lines = f.readlines()

    for line in lines:
        STRIPE_EVENTS.append(line.replace("\n", ""))
        COLOR_CHOICES = COLOR_CHOICES + (
            (line.replace("\n", ""), line.replace("\n", "").replace(".", "_").upper()),
        )


class StripeVars(models.Model):
    """Stripe configuration item"""

    name = models.CharField(max_length=31, unique=True, choices=COLOR_CHOICES)
    value = models.TextField(blank=True)
