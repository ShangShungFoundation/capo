from django.conf.urls import patterns, url


urlpatterns = patterns('capo.views',
    url(r'^job/run/$',
        "run_job", name='run_job'),
    url(r'^job/submit/(?P<recipe_id>\d+)/$',
        "submit_job", name='submit_job'),
)
