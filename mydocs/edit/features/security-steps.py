# -*- coding: utf-8 -*-
from lettuce import *

from django.core.urlresolvers import reverse
from mydocs.edit.models import Document
from mydocs.edit.features.common import login_as, goto_url
