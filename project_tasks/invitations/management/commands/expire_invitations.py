from django.core.management.base import BaseCommand
from django.utils import timezone
from invitations.models import Invitation

class Command(BaseCommand):
    help = 'Marks expired invitations as expired'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_invitations = Invitation.objects.filter(
            status='pending',
            expiration_date__lt=now
        )
        count = expired_invitations.update(status='expired')
        self.stdout.write(self.style.SUCCESS(f'Successfully marked {count} invitations as expired'))