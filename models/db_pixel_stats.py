#!/usr/bin/python
# -*- coding: utf-8 -*-

db1 = DAL(settings.database_uri_pixel, check_reserved=['postgres', 'mysql'], migrate_enabled=False, migrate=False)

##compartir a un amigo
db1.define_table('pixel_stats',
    Field('page_key','string',required=True,label=T('key')),
    Field('hits','integer',label=T('hits')),
    Field('datetime_ts','datetime',writable=False,readable=False,default=request.now),
    Field('date_day','date',writable=False,readable=False,default=request.now),
    Field('day_of_the_month','integer',writable=False,readable=False),
    Field('month_of_the_year','integer',writable=False,readable=False),
    Field('year','integer',writable=False,readable=False),
    Field('week_of_the_year','integer',writable=False,readable=False)
)


