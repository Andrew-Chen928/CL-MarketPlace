from django.test import TestCase

# ### create customize condition of query
# from autofixture import AutoFixture
# from random import randint
# from sixerrapp.models import Gig
# fixture = AutoFixture(Gig, field_values={'price': randint(2,10)})
# entries = fixture.create(10)

# ### example of date calculation
# yesterday = datetime.date.today() - datetime.timedelta(days=1)

# ### how to filtering only the day of creat_time:
# from django.utils import timezone
# now = timezone.now()
# Gig.objects.filter(create_time__day=now.day)

# ### delete example:
# Gig.objects.get(id = id).delete()
# Gig.objects.filter(create_time__month=now.month).delete()