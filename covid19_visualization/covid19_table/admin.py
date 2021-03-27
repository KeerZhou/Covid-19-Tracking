from django.contrib import admin
#定义Admin模块管理对象
# Register your models here.

from .models import Article
from .models import News
from .models import Research
from .models import Predict_result
from .models import Confirmed_data

admin.site.register(Article)

admin.site.register(News)

admin.site.register(Research)

admin.site.register(Predict_result)

admin.site.register(Confirmed_data)
