# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from facebook import GraphAPI, GraphAPIError
import datetime



@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()

    """
    pages = fbpl().select(fbpl.page.ALL, orderby=fbpl.page.id)
    user = auth.user
    if user:
        response.flash = T('You are %(name)s', dict(name=user['first_name']))
        return dict(message=T('Hello, Facebook is telling that you are %(first_name)s %(last_name)s', dict(first_name=user['first_name'], last_name=user['last_name'])),pages=pages)
    response.flash = T('Welcome to web2py')

    return dict(message=T('Hello, please login'),pages=pages)

#@auth.requires_login()

@auth.requires_login()
def display_form():
    allplaces = SQLFORM.grid(fbpl.place,user_signature=False, create=False, deletable=True, editable=False,paginate=10, maxtextlength = 100, orderby = 'id DESC')

    return dict(allplaces=allplaces)

def display_page():
    #allpages = SQLFORM.grid(fbpl.page,user_signature=False, create=False, deletable=True, editable=False,paginate=10, maxtextlength = 100, orderby = 'id DESC')
    allpages= fbpl().select(fbpl.page.ALL, orderby=~fbpl.page.likes_sincelastupdate,limitby=(0, 100))
    return dict(allpages=allpages)

def display_people():
    allpeople = SQLFORM.grid(fbpl.people,user_signature=False, create=False, deletable=True, editable=False,paginate=10, maxtextlength = 100, orderby = 'id DESC')

    return dict(allpeople=allpeople)

def display_post():
    #allposts = SQLFORM.grid(fbpl.post,user_signature=False, create=False, deletable=True, editable=False,paginate=10, maxtextlength = 100, orderby = 'id DESC')
    allposts= fbpl(fbpl.post.status_type <> '' and fbpl.post.fscore > 0).select(fbpl.post.ALL, orderby=~fbpl.post.fscore,limitby=(0, 1000))
    return dict(allposts=allposts)

def display_event():
    allevents = SQLFORM.grid(fbpl.event,user_signature=False, create=False, deletable=True, editable=False,paginate=10, maxtextlength = 100, orderby = 'id DESC')

    return dict(allevents=allevents)


@auth.requires_login()
def addplace():
    form = FORM('Facebook place id or Name',
              INPUT(_name='placeid', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        placeid= request.vars['placeid']
        message = getP(placeid)
        response.flash = str(message) #'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def addpage():
    form = FORM('Facebook page id or Name',
              INPUT(_name='pageid', requires=IS_NOT_EMPTY()), '請輸入陣營',
              INPUT(_name='team', requires=IS_IN_SET(['連勝文','柯文哲','丁守中','顧立雄'])),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        gid= request.vars['pageid']
        team =request.vars['team']
        message = getPage(gid,team)
        response.flash = str(message) #'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def addpeople():
    form = FORM('Facebook user id or Name',
              INPUT(_name='uid', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        gid= request.vars['uid']
        message = getPeople(gid)
        response.flash = str(message) #'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def addpost():
    form = FORM('Facebook post id',
              INPUT(_name='uid', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        gid= request.vars['uid']
        message = getPost(gid)
        response.flash = str(message) #'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def addevent():
    form = FORM('Facebook event id',
              INPUT(_name='uid', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        gid= request.vars['uid']
        message = getEvent(gid)
        response.flash = str(message) #'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)


@auth.requires_login()
def getP(gid):
    graph = getGraph()
    try:
        if gid:
            fb_obj = graph.get_object(gid)
            id= fb_obj["id"]
            row = fbpl.place(placeid=id)
            if not row:
                name =  fb_obj["name"]
                category = fb_obj["category"]
                category_list =  fb_obj["category_list"]
                checkins= fb_obj["checkins"]
                zip= fb_obj["location"]["zip"]
                latitude= fb_obj["location"]["latitude"]
                longitude= fb_obj["location"]["longitude"]
                link= fb_obj["link"]
                old_ids = ''
                fbpl.place.insert(placeid=id,name = name,latitude=latitude,longitude=longitude,category=category,category_list=category_list,zip=zip,link=link,old_ids=old_ids)

            fbpl.commit()
            message='Successfully adding new place into the database'
        else:
            message='failure, please check your placeid!'
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()
    except :
        message = "unknown error"

    return dict(message=message)

@auth.requires_login()
def getPage(gid,team):
    graph = getGraph()
    try:
        if gid:
            fb_obj = graph.request(gid ,args={'fields': 'id, name, category, about, can_post, talking_about_count, were_here_count, link,description, cover, website, picture.type(large), is_published,likes.limit(1).summary(true)'})
            id= fb_obj["id"]
            pageid = fb_obj["id"]
            name =  fb_obj["name"] if ('name' in fb_obj) else ''
            category = fb_obj["category"] if ('category' in fb_obj) else ''
            about = fb_obj["about"] if ('about' in fb_obj) else ''
            can_post = fb_obj["can_post"] if ('can_post' in fb_obj) else ''
            is_published = fb_obj["is_published"] if ('is_published' in fb_obj) else ''
            talking_about_count = fb_obj["talking_about_count"] if ('talking_about_count' in fb_obj) else 0
            were_here_count = fb_obj["were_here_count"] if ('were_here_count' in fb_obj) else 0
            link = fb_obj["link"] if ('link' in fb_obj) else ''
            likes = fb_obj["likes"] if ('likes' in fb_obj) else ''
            description = fb_obj["description"] if ('description' in fb_obj) else ''                
            cover_id = fb_obj["cover"]["cover_id"] if ('cover' in fb_obj) else ''
            source = fb_obj["cover"]["source"] if ('cover' in fb_obj) else ''
            picture = fb_obj["picture"]["data"]["url"] if ('picture' in fb_obj) else ''
            team=team    
            website = fb_obj["website"] if ('website' in fb_obj) else ''
            row = fbpl(fbpl.page.pageid==id).select().first()
            if row :
                row.update_record(name=name, category=category, about=about, can_post=can_post, is_published=is_published, link=link, description=description, cover_id=cover_id, source=source,website=website,talking_about_count=talking_about_count,were_here_count=were_here_count,picture=picture,team=team)
            else:
                fbpl.page.insert(pageid=pageid,name=name, category=category, about=about, can_post=can_post, is_published=is_published, link=link, description=description, cover_id=cover_id, source=source,website=website,talking_about_count=talking_about_count,were_here_count=were_here_count,picture=picture,team=team)
            fbpl.commit()
            message='Successfully adding new page into the database'
        else:
            message='failure, please check your pageid!'
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()


    return dict(message=message)

@auth.requires_login()
def getPost(gid):
    graph = getGraph()
    try:
        if gid:       
            fb_obj = graph.request(gid,args={'fields': 'id, message, updated_time, from, created_time, status_type, type, link, likes.limit(1).summary(true), shares, comments.limit(1).summary(true), object_id, picture'})
            fid= fb_obj["id"]
            message =  fb_obj["message"] if ('message' in fb_obj) else ''
            updated_time = fb_obj["updated_time"] if ('updated_time' in fb_obj) else 0
            from_id = fb_obj["from"]["id"] if ('from' in fb_obj) else ''
            from_name = fb_obj["from"]["name"] if ('from' in fb_obj) else ''
            created_time = fb_obj["created_time"] if ('created_time' in fb_obj) else ''
            status_type = fb_obj["status_type"] if ('status_type' in fb_obj) else ''
            ptype = fb_obj["type"] if ('type' in fb_obj) else ''
            status_type = fb_obj["status_type"] if ('status_type' in fb_obj) else ''
            link =  fb_obj["link"] if ('link' in fb_obj) else ''
            picture =  fb_obj["picture"] if ('picture' in fb_obj) else ''
            shares_count = fb_obj["shares"]['count'] if ('shares' in fb_obj) else 0
            likes_count = fb_obj["likes"]["summary"]["total_count"] if ('summary' in fb_obj) else 0
            comment_count = fb_obj["comments"]["summary"]["total_count"] if ('summary' in fb_obj) else 0
            object_id = fb_obj["object_id"] if ('object_id' in fb_obj) else ''
            row=fbpl(fbpl.page.pageid==from_id).select().first()
            team = row['team']
            row = fbpl(fbpl.post.fid==from_id).select().first()
            if row:
                row.update_record(fid=fid, message=message,from_id=from_id, from_name=from_name, created_time=created_time,object_id=object_id,ptype=ptype,status_type=status_type, link=link, picture=picture ,shares_count=shares_count,likes_count=likes_count,comment_count=comment_count,team=team, updated_time=updated_time)
            else:
                fbpl.post.insert(fid=fid, message=message,from_id=from_id, from_name=from_name, created_time=created_time,object_id=object_id,ptype=ptype,status_type=status_type, link=link, picture=picture ,shares_count=shares_count,likes_count=likes_count,comment_count=comment_count,team=team, updated_time=updated_time)
                fbpl.commit()
            message='Successfully adding new post into the database'            
        else:
            message='failure, please check your postid!'       
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit() 
    
    
    return dict(message=message) 



@auth.requires_login()
def getPeople(gid):
    graph = getGraph()
    try:
        if gid:       
            fb_obj = graph.get_object(gid)
            id= fb_obj["id"]
            row = fbpl.people(uid=id)
            if not row: 
                uid = fb_obj["id"]
                name =  fb_obj["name"] if ('name' in fb_obj) else ''
                gender = fb_obj["gender"] if ('gender' in fb_obj) else ''
                hometown = fb_obj["hometown"] if ('hometown' in fb_obj) else ''
                loc_id = fb_obj["location"]["id"] if ('location' in fb_obj) else ''
                loc_name = fb_obj["location"]["name"] if ('location' in fb_obj) else ''
                updated_time = fb_obj["updated_time"] if ('updated_time' in fb_obj) else ''
                locale = fb_obj["locale"] if ('locale' in fb_obj) else ''
                fbpl.people.insert(uid=uid, name=name, gender=gender, hometown=hometown, loc_id=loc_id, loc_name=loc_name, updated_time=updated_time, locale=locale)
            
            fbpl.commit()
            message='Successfully adding new people into the database'            
        else:
            message='failure, please check your userid!'       
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit() 
    
    
    return dict(message=message) 

@auth.requires_login()
def getEvent(eid):
    graph = getGraph()
    event= graph.get_object(eid)
    eventid = event["id"] if 'id' in event else ''
    row = fbpl.event(eventid=eventid)
    try:
        description = event["description"] if 'description' in event else ''
        end_time  = event["end_time"] if 'end_time' in event else ''
        timezone = event["timezone"] if 'timezone' in event else ''
        name = event["name"] if 'name' in event else ''
        location = event["location"] if 'location' in event else ''
        ownerid = event["owner"]["id"] if 'owner' in event else ''
        ownername = event["owner"]["name"] if 'owner' in event else ''
        picture = event["picture"] if 'picture' in event else ''
        privacy = event["privacy"] if 'privacy' in event else ''
        start_time = event["start_time"] if 'start_time' in event else ''
        ticket_uri = event["ticket_uri"] if 'ticket_uri' in event else ''
        updated_time = event["updated_time"] if 'updated_time' in event else ''
        is_date_only  = event["is_date_only"] if 'is_date_only' in event else ''
        if 'venue' in event:
            venueid  = event["venue"]["id"] if 'id' in event["venue"] else ''
            venuename = event["venue"]["name"] if 'name' in event["venue"] else ''
            country = event["venue"]["country"] if 'country' in event["venue"] else ''
            city = event["venue"]["city"] if 'city' in event["venue"] else ''
            state  = event["venue"]["state"] if 'state' in event["venue"] else ''
            street = event["venue"]["street"] if 'street' in event["venue"] else ''
            zipcode = event["venue"]["zip"] if 'zip' in event["venue"] else ''
            longitude = event["venue"]["longitude"] if 'longitude' in event["venue"] else ''
            latitude  = event["venue"]["latitude"] if 'latitude' in event["venue"] else ''        
        if not row:
            fbpl.event.insert(eventid=eventid, description=description, end_time=end_time, timezone=timezone, name=name, location=location, ownerid=ownerid, ownername= ownername, picture=picture, privacy=privacy, start_time=start_time, ticket_uri=ticket_uri, updated_time=updated_time, is_date_only=is_date_only, venuename=venuename, venueid=venueid, country=country, city=city, state=state, street=street, zipcode=zipcode, longitude=longitude, latitude=latitude)
            fbpl.commit()
            message='Successfully adding new event into the database'    
        else:
            row.update_record(eventid=eventid, description=description, end_time=end_time, timezone=timezone, name=name, location=location, ownerid=ownerid, ownername= ownername, picture=picture, privacy=privacy, start_time=start_time, ticket_uri=ticket_uri, updated_time=updated_time, is_date_only=is_date_only, venuename=venuename, venueid=venueid, country=country, city=city, state=state, street=street, zipcode=zipcode, longitude=longitude, latitude=latitude)
            message='Successfully updated new event into the database'       
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit() 
    
    
    return dict(message=message) 

@auth.requires_login()
def social_counts_pages():
    from datetime import datetime ,date
    from time import strptime
    from dateutil.relativedelta import relativedelta

    pageid = request.args(0)  or redirect(URL('index'))
    pagename = fbpl(fbpl.page.pageid== pageid).select()[0].name

    #social_counts = fbpl(fbpl.social_counts.placeid== placeid).select()
    query = fbpl.social_counts.placeid == pageid
    #social_counts = SQLFORM.smartgrid(fbpl.social_counts,constraints = {'social_counts':query},user_signature=False, create=False, deletable=False, editable=False, maxtextlength = 240)
    social_counts = SQLFORM.grid(query,fbpl.social_counts,user_signature=False, create=False, deletable=False, editable=False,paginate=240, maxtextlength = 240, orderby = 'id DESC')
    first_rec = fbpl(fbpl.social_counts.placeid== pageid).select(fbpl.social_counts.ALL,limitby=(0, 2)).first().date_time
    year = first_rec.year
    month = first_rec.month
    dt = datetime.now()
    year2 = dt.year
    month2 = dt.month
    dtlist = []
    while (year <= year2) :
        if (year == year2):
            if (month <= month2):
                m_str = '0' + str(month) if month < 10 else str(month)
                dtlist.append(str(year) + '-' + str(m_str))
        else:
            dtlist.append(str(year) + '-' + str(month))
        first_rec = first_rec + relativedelta(months = 1)
        year = first_rec.year
        month = first_rec.month
    return dict(social_counts=social_counts, pagename=pagename,dtlist=dtlist,pageid=pageid)

@auth.requires_login()
def social_counts():
    from datetime import datetime ,date
    from time import strptime
    from dateutil.relativedelta import relativedelta

    placeid = request.args(0)  or redirect(URL('index'))
    placename = fbpl(fbpl.place.placeid== placeid).select()[0].name

    #social_counts = fbpl(fbpl.social_counts.placeid== placeid).select()
    query = fbpl.social_counts.placeid == placeid
    #social_counts = SQLFORM.smartgrid(fbpl.social_counts,constraints = {'social_counts':query},user_signature=False, create=False, deletable=False, editable=False, maxtextlength = 240)
    social_counts = SQLFORM.grid(query,fbpl.social_counts,user_signature=False, create=False, deletable=False, editable=False,paginate=240, maxtextlength = 240, orderby = 'id DESC')
    first_rec = fbpl(fbpl.social_counts.placeid== placeid).select(fbpl.social_counts.ALL,limitby=(0, 2)).first().date_time
    year = first_rec.year
    month = first_rec.month
    dt = datetime.now()
    year2 = dt.year
    month2 = dt.month
    dtlist = []
    while (year <= year2) :
        if (year == year2):
            if (month <= month2):
                m_str = '0' + str(month) if month < 10 else str(month)
                dtlist.append(str(year) + '-' + str(m_str))
        else:
            dtlist.append(str(year) + '-' + str(month))
        first_rec = first_rec + relativedelta(months = 1)
        year = first_rec.year
        month = first_rec.month
    latitude =  fbpl(fbpl.place.placeid== placeid).select().first().latitude
    longitude =  fbpl(fbpl.place.placeid== placeid).select().first().longitude
    return dict(social_counts=social_counts, placename=placename,latitude=latitude,longitude=longitude,dtlist=dtlist,placeid=placeid)

@auth.requires_login()
def social_counts_month():
    from datetime import datetime ,date
    pageid = request.args(0) or redirect(URL('index'))
    pagename = fbpl(fbpl.page.pageid== pageid).select()[0].name
    year = request.args(1).split('-')[0]
    month = request.args(1).split('-')[1]
    from_date = datetime.strptime(str(year) + '-'+ str(month) +'-01 00:00:00','%Y-%m-%d %H:%M:%S')
    month2 = int(month) +1 if int(month) < 12 else 1
    year2 = int(year) if int(month) < 12 else int(year)+1
    to_date = datetime.strptime(str(year2) + '-'+ str(month2) +'-01 00:00:00','%Y-%m-%d %H:%M:%S')
    pagename = fbpl(fbpl.page.pageid== pageid).select()[0].name
    #rec = fbpl.social_counts.placeid == placeid
    #rec1= fbpl.social_counts.date_time >= from_date
    #rec2= fbpl.social_counts.date_time < to_date
    #constraints = {'social_counts':rec & rec1 & rec2}
    rows = fbpl((fbpl.social_counts.placeid == pageid) & (fbpl.social_counts.date_time >= from_date) & (fbpl.social_counts.date_time < to_date)).select()
    #social_counts = SQLFORM.smartgrid(fbpl.social_counts,constraints = constraints,args=[request.args(0),request.args(1)],user_signature=False, create=False, deletable=False, editable=False,paginate=240, maxtextlength = 240, orderby = 'id DESC')
    return dict(pagename=pagename,date = request.args(1),rows=rows)

@auth.requires_login()
def social_countsall_month():
    from datetime import datetime ,date
    year = request.args(0).split('-')[0]
    month = request.args(0).split('-')[1]
    from_date = datetime.strptime(str(year) + '-'+ str(month) +'-01 00:00:00','%Y-%m-%d %H:%M:%S')
    month2 = int(month) +1 if int(month) < 12 else 1
    year2 = int(year) if int(month) < 12 else int(year)+1
    to_date = datetime.strptime(str(year2) + '-'+ str(month2) +'-01 00:00:00','%Y-%m-%d %H:%M:%S')
    rows = fbpl((fbpl.social_counts.date_time >= from_date) & (fbpl.social_counts.date_time < to_date)).select()
    #query = ( fbpl.social_counts.date_time >= from_date) & (fbpl.social_counts.date_time < to_date)
    #social_counts = SQLFORM.grid(query,fbpl.social_counts,user_signature=False, create=False, deletable=False, editable=False,paginate=240, maxtextlength = 240, orderby = 'id DESC')
    return dict(date=request.args(0),rows=rows)

@auth.requires_login()
def social_counts_all():
    from datetime import datetime ,date
    from time import strptime
    from dateutil.relativedelta import relativedelta
    first_rec = fbpl().select(fbpl.social_counts.ALL,limitby=(0, 2)).first().date_time
    year = first_rec.year
    month = first_rec.month
    dt = datetime.now()
    year2 = dt.year
    month2 = dt.month
    dtlist = []
    while (year <= year2) :
        if (year == year2):
            if (month <= month2):
                m_str = '0' + str(month) if month < 10 else str(month)
                dtlist.append(str(year) + '-' + str(m_str))
        else:
            dtlist.append(str(year) + '-' + str(month))
        first_rec = first_rec + relativedelta(months = 1)
        year = first_rec.year
        month = first_rec.month
    social_counts = SQLFORM.grid(fbpl.social_counts,user_signature=False, create=False, deletable=False, editable=False,paginate=100, maxtextlength = 240, orderby = 'id DESC')
    return dict(social_counts=social_counts,dtlist=dtlist)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
