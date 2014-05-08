# -*- coding: utf-8 -*-
import ExtendedOpenGraph
from facebook import GraphAPI, GraphAPIError
import json
from collections import OrderedDict
import datetime
from dateutil import parser

@auth.requires_login()
def test2():
    import time
    graph = getGraph()
    #rows = fbpl().select(fbpl.post.ALL)
    gid = '652438848137404'
    fb_obj = graph.request(gid, args={'fields': 'insights'})
    insights=[]
    insights = fb_obj["insights"]["data"] if  ('insights' in fb_obj) else []
    lifetime_likes = sum(insights[0]["values"][2]["value"].values())
    daily_people_talking = sum(insights[1]["values"][2]["value"].values())
    weekly_people_talking = sum(insights[2]["values"][2]["value"].values())
    monthly_people_talking = sum(insights[3]["values"][2]["value"].values())
    return str(lifetime_likes) + ' ' + str(daily_people_talking) + ' ' + str(weekly_people_talking)+ ' ' +str(monthly_people_talking)

def test():
    date = datetime.datetime.strptime("2014-05-03 08:00:00", '%Y-%m-%d %H:%M:%S')            
    date2 = date + datetime.timedelta(hours=24)
    date3 = date2 + datetime.timedelta(hours=24)
    likes1 = fbpl((fbpl.post_counts.date_time >= date)).select().first()
    likes2 = fbpl((fbpl.post_counts.date_time >= date2) ).select().first()
    Posts = fbpl((fbpl.post.team == '柯文哲') & (fbpl.post.status_type <> '') & (fbpl.post.created_time >= date) & (fbpl.post.created_time < date2) ).select()
    dailyPosts =len(Posts)
    return dict(date=date,date2=date2,likes1=likes1,likes2=likes2,dailyPosts=dailyPosts)

def fixtime():
    #hour48 = (now - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    #hour48 = datetime.datetime.strptime(hour48,'%Y-%m-%d %H:%M:%S')
    rows = fbpl(fbpl.post.id>0).select()
    for row in rows:
        created_time = str(row.created_time)
        #created_time2 = created_time
        #updated_time= row.updated_time.strftime('%Y-%m-%d %H:%M:%S')
        created_time = datetime.datetime.strptime(created_time,'%Y-%m-%d %H:%M:%S')
        #updated_time = datetime.datetime.strptime(updated_time,'%Y-%m-%d %H:%M:%S')

        row.update_record(created_time=created_time)
    return "success"

def fixtime2():

    rows = fbpl(fbpl.post.id>0).select()
    for row in rows:
        updated_time= row.updated_time - datetime.timedelta(hours=7)
        
        
        row.update_record(updated_time=updated_time)
    return "success"

#def postCount(candidate, date):
def postCount():
    #fid ='668137593234196'
    #fid ='668137593234196'
    candidates = []
    candidates.append("連勝文")
    candidates.append("柯文哲")
    candidates.append("顧立雄")
    date = datetime.datetime.strptime("2014-04-25 00:00:00", '%Y-%m-%d %H:%M:%S')
    
    while date <= datetime.datetime.now():
        date2 = date + datetime.timedelta(days=1)
        for candidate in candidates:
            

            #candidate = '柯文哲'
            #date= datetime.datetime.utcnow()
            #date= datetime.datetime.strptime('2014-04-29 08:00:00','%Y-%m-%d %H:%M:%S')
            #date2 = datetime.datetime.strptime('2014-04-30 08:00:00','%Y-%m-%d %H:%M:%S')
            rows = fbpl( (fbpl.post.team == candidate ) & (fbpl.post.tscore > 0 )).select()
            
            total_post_likes =0
            total_post_comments =0
            total_post_shares =0
            pLike1 = 0
            pLike2 = 0
            pComment1 = 0
            pComment2 = 0
            pShare1 = 0
            pShare2 = 0
            
            for row in rows:
                post1 = fbpl( (fbpl.post_counts.fid == row.fid) & (fbpl.post_counts.date_time >= date) & (fbpl.post_counts.date_time < date2)).select().last()
                #post2 = fbpl( (fbpl.post_counts.fid == row.fid) & (fbpl.post_counts.date_time >= date2)).select().first()
                pLike1 = post1.likes_count if post1 else 0
                #pLike2 = post2.likes_count if post2 else 0
                pComment1 = post1.comment_count if post1 else 0
                #pComment2 = post2.comment_count if post2 else 0
                pShare1 = post1.shares_count if post1 else 0
                #pShare2 = post2.shares_count if post2 else 0           
        
             
                    
                    
                total_post_likes = total_post_likes +  pLike1
                total_post_comments = total_post_comments + pComment1
                total_post_shares = total_post_shares +pShare1
                
            #date = datetime.datetime.strptime('2014-05-03 00:00:00','%Y-%m-%d %H:%M:%S')    
            row2 = fbpl( (fbpl.team_counts.team == candidate ) & (fbpl.team_counts.date_time == date )).select().first()
            if row2:
                row2.update_record(total_post_likes=total_post_likes,total_post_comments=total_post_comments, total_post_shares=total_post_shares)
        date = date + datetime.timedelta(days=1)
    return dict(date=date,team=candidate, total_post_likes=total_post_likes, total_post_comments=total_post_comments, total_post_shares=total_post_shares)

#1.這部份排程把所有的專頁的likes 還有 talkingabout更新。
@auth.requires_login()
def countAllPageSocialCount():
    import datetime
    import time

    graph = getGraph()
    rows = fbpl().select(fbpl.page.pageid, orderby=fbpl.page.id)
    start_date_time=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    start_date_time=datetime.datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
    for row in rows:
        gid= row.pageid
        #check if the Facebook has the graphic
        getPageSocialCount(gid)

    message = teamCount()
    end_date_time=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    end_date_time=datetime.datetime.strptime(end_date_time, '%Y-%m-%d %H:%M:%S')
    fbpl.update_log.insert(start_date_time=start_date_time,end_date_time=end_date_time)
    message = 'Successfully update socialcount of pages'
    return dict(message=message)

#2.get likes , checkins, were_here_count, talking_about_count, 
@auth.requires_login()
def getPageSocialCount(gid):
    import datetime
    import time
    graph = getGraph()
    try:
        if gid:
            oid = gid
        else:
            message='failure, please check your placeid!'
            return dict(message=message)
        pid = checkGraphId(oid)
        if pid <> '0':
            if pid <> oid :
                record2 = fbpl(fbpl.page.pageid==pid).select().first()
                if not (record2) :
                   getPage(pid)
                   time.sleep(1)
                   fbpl(fbpl.page.pageid==oid).delete()
            fb_obj = graph.request(pid ,args={'fields': 'id,name, category, about, can_post, checkins, talking_about_count, were_here_count, link,description, cover, website, picture.type(large), is_published,likes.limit(1).summary(true), insights'})
            checkins =  fb_obj["checkins"] if  ('checkins' in fb_obj) else 0
            likes= fb_obj["likes"] if  ('likes' in fb_obj) else 0
            were_here_count= fb_obj["were_here_count"] if  ('were_here_count' in fb_obj) else 0
            talking_about_count	 = fb_obj["talking_about_count"] if  ('talking_about_count' in fb_obj) else 0
            updated_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000')
            updated_time = datetime.datetime.strptime(updated_time,'%Y-%m-%dT%H:%M:%S+0000')
            date_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')
            cover_id = fb_obj["cover"]["cover_id"] if ('cover' in fb_obj) else ''
            source = fb_obj["cover"]["source"] if ('cover' in fb_obj) else ''
            picture = fb_obj["picture"]["data"]["url"] if ('picture' in fb_obj) else ''
            row = fbpl.page(pageid=pid)
            checkins24= 0
            likes24 = 0
            were_here_count24 = 0
            talking_about_count24 = 0
            if row:
                fbpl.social_counts.insert(placeid=pid,checkins = checkins,likes=likes,date_time=date_time,were_here_count=were_here_count,updated_time=updated_time,talking_about_count=talking_about_count)
                fbpl.commit()
                likes_sincelastupdate = int(likes)-int(row.likes) if likes else 0
                checkins_sincelastupdate = int(checkins)-int(row.checkins) if checkins else 0
                talking_about_sincelastupdate = int(talking_about_count)-int(row.talking_about_count) if talking_about_count else 0
                were_here_sincelastupdate = int(were_here_count)-int(row.were_here_count) if were_here_count else 0
                plist = getPageCount(gid, 0 , 1)
                checkins24= plist[0]
                likes24 = plist[1]
                were_here_count24= plist[2]
                talking_about_count24= plist[3]
                #now = datetime.datetime.now()
                #hour24 = hourdiff(now,24)
                #row2 = fbpl((fbpl.social_counts.date_time <= hour24) & (fbpl.social_counts.placeid==pid) ).select(fbpl.social_counts.ALL).last()
                #if row2:
                #    likes_sincelastupdate = int(likes)-int(row2.likes) if likes else 0
                #    checkins_sincelastupdate = int(checkins)-int(row2.checkins) if checkins else 0
                #    talking_about_sincelastupdate = int(talking_about_count)-int(row2.talking_about_count) if talking_about_count else 0
                #    were_here_sincelastupdate = int(were_here_count)-int(row2.were_here_count) if were_here_count else 0
                #else:  #if no record can be found in the social_counts then use the last time number
                #    likes_sincelastupdate = int(likes)-int(row.likes) if likes else 0
                #    checkins_sincelastupdate = int(checkins)-int(row.checkins) if checkins else 0
                #    talking_about_sincelastupdate = int(talking_about_count)-int(row.talking_about_count) if talking_about_count else 0
                #    were_here_sincelastupdate = int(were_here_count)-int(row.were_here_count) if were_here_count else 0
                row.update_record(checkins = checkins, likes=likes, date_time=date_time, were_here_count=were_here_count, updated_time=updated_time, talking_about_count=talking_about_count, likes_sincelastupdate=likes_sincelastupdate, talking_about_sincelastupdate=talking_about_sincelastupdate, checkins_sincelastupdate=checkins_sincelastupdate, were_here_sincelastupdate=were_here_sincelastupdate , checkins24=checkins24, likes24=likes24, were_here_count24=were_here_count24, talking_about_count24=talking_about_count24, cover_id=cover_id, source=source, picture=picture )
            else:
                likes_sincelastupdate =  0
                checkins_sincelastupdate =  0
                talking_about_sincelastupdate = 0
                were_here_sincelastupdate = 0
                fbpl.page.insert(pageid=pid, checkins = checkins, likes=likes, date_time=date_time, were_here_count=were_here_count, updated_time=updated_time, talking_about_count=talking_about_count, likes_sincelastupdate=likes_sincelastupdate, talking_about_sincelastupdate=talking_about_sincelastupdate, checkins_sincelastupdate=checkins_sincelastupdate, were_here_sincelastupdate=were_here_sincelastupdate, cover_id=cover_id, source=source, picture=picture )
                fbpl.commit()
                fbpl.social_counts.insert(placeid=pid,checkins = checkins,likes=likes,date_time=date_time,were_here_count=were_here_count,updated_time=updated_time,talking_about_count=talking_about_count)
                fbpl.commit()
            time.sleep(1.1)
            message='Successfully update the PageSocialCount'
            return dict(message=message)
        else:
            return dict(message='failure, please check your placeid!')

    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=pid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()


    #response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=message)  #dict(message=str[9])

#3.檢查各個專頁是否有新文章
@auth.requires_login()
def collect_posts():
    import time
    rows = fbpl().select(fbpl.page.pageid)
    for row in rows:
        getPagePosts(row.pageid)
        time.sleep(1)
    return "All page posts Finished"

#4.
@auth.requires_login()
def getPagePosts(pageid):
    import time
    try:
        graph = getGraph()
        posts_data=graph.request(pageid + '/posts', args={'fields':'id, place, message, updated_time, from, created_time, status_type, type, link, picture, likes.limit(1).summary(true), shares, comments.limit(1).summary(true), object_id'})
        data = []
        data = posts_data["data"]
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=pageid,date_time=datetime.datetime.utcnow(),error_msg=message)
        fbpl.commit()

    try:
        for post in data:
            fid = post["id"].split('_')[1]
            row = fbpl.post(fid=fid)
            if row:
                #fbupdated_time = datetime.datetime.strptime(post["updated_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('updated_time' in post) else ''
                pass
                #message =  post["message"] if ('message' in post) else ''
                #updated_time = datetime.datetime.strptime(post["updated_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('updated_time' in post) else ''
                #likes_count = post["likes"]["summary"]["total_count"] if ('likes' in post) else 0
                #comment_count = post["comments"]["summary"]["total_count"] if ('comments' in post) else 0
                #shares_count = post["shares"]['count'] if ('shares' in post) else 0
                #now = datetime.datetime.utcnow()
                #hour48 = hourdiff(now,48)
                #row2 = fbpl((fbpl.post_counts.date_time <= hour48) & (fbpl.post_counts.fid==fid) ).select(fbpl.post_counts.ALL).last()
                #if row2:
                #    likes_sincelastupdate = int(likes_count)-int(row2.likes_count) if likes_count else 0
                #    shares_sincelastupdate = int(shares_count)-int(row2.shares_count) if shares_count else 0
                #    comment_sincelastupdate = int(comment_count)-int(row2.comment_count) if comment_count else 0
                #else:  #if no record can be found in the post_counts then use the last time number
                #    likes_sincelastupdate = int(likes_count)-int(row.likes_count) if likes_count else 0
                #    shares_sincelastupdate = int(shares_count)-int(row.shares_count) if shares_count else 0
                #    comment_sincelastupdate = int(comment_count)-int(row.comment_count) if comment_count else 0
                #likes_sincelastupdate = int(likes_count)-int(row.likes_count) if likes_count else 0
                #shares_sincelastupdate = int(shares_count)-int(row.shares_count) if shares_count else 0
                #comment_sincelastupdate = int(comment_count)-int(row.comment_count) if comment_count else 0                

                #link= row["link"]
                #object_id = row["object_id"]
                #------------ after update it can be deleted
                #ptype = row.ptype
                #if (ptype == 'link' ) | (ptype == 'video'):
                #    try:
                #        picture =getOpengraphImage(link)
                #        if picture == '':
                #            picture = post["picture"] if ('picture' in post) else ''
                #    except:
                #        picture = post["picture"] if ('picture' in post) else ''
                #elif (ptype == 'photo' ) :
                #    try:
                #        images=[]
                #        images =graph.request(object_id , args={'fields':'images'})["images"]
                #        for image in images:
                #            if (image["height"] > 200) & (image["width"] > 150):
                #                picture = image["source"]
                        #time.sleep(1)
                #    except:
                #       picture = post["picture"] if ('picture' in post) else ''
                #else:
                #    picture = post["picture"] if ('picture' in post) else ''

                #row.update_record(fbupdated_time=fbupdated_time)
            else:
                message =  post["message"] if ('message' in post) else ''
                from_id = post["from"]["id"] if ('from' in post) else ''
                from_name = post["from"]["name"] if ('from' in post) else ''
                created_time = datetime.datetime.strptime(post["created_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('created_time' in post) else ''
                fbupdated_time = datetime.datetime.strptime(post["updated_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('updated_time' in post) else ''
                updated_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                updated_time = datetime.datetime.strptime(updated_time,'%Y-%m-%d %H:%M:%S' )
                status_type = post["status_type"] if ('status_type' in post) else ''
                ptype = post["type"] if ('type' in post) else ''
                status_type = post["status_type"] if ('status_type' in post) else ''
                link = post["link"] if ('link' in post) else ''
                shares_count = post["shares"]['count'] if ('shares' in post) else 0
                likes_count = post["likes"]["summary"]["total_count"] if ('likes' in post) else 0
                comment_count = post["comments"]["summary"]["total_count"] if ('comments' in post) else 0
                object_id = post["object_id"] if ('object_id' in post) else ''
                placeid = post["place"]["id"] if ('place' in post) else ''
                placename = post["place"]["name"] if ('place' in post) else ''
                tscore = shares_count*0.5 + comment_count*0.3 + likes_count*0.2
                if placeid != '' :
                    getPlace(placeid)
                    time.sleep(1)
                row=fbpl(fbpl.page.pageid==from_id).select().first()
                team = row['team']
                likes_sincelastupdate=0
                shares_sincelastupdate=0
                comment_sincelastupdate=0
                if (ptype == 'link' ) | (ptype == 'video'):
                    try:
                        picture =getOpengraphImage(link)
                        if picture == '':
                            picture = post["picture"] if ('picture' in post) else ''
                    except:
                        picture = post["picture"] if ('picture' in post) else ''
                elif (ptype == 'photo' ) :
                    try:
                        images=[]
                        images =graph.request(object_id , args={'fields':'images'})["images"]
                        for image in images:
                            if (image["height"] > 200) & (image["width"] > 150):
                                picture = image["source"]
                        #time.sleep(1)
                    except:
                        picture = post["picture"] if ('picture' in post) else ''
                else:
                    picture = post["picture"] if ('picture' in post) else ''
                
                fbpl.post.insert(fid=fid, message=message,from_id=from_id, from_name=from_name, created_time=created_time,object_id=object_id,ptype=ptype,status_type=status_type, link=link, picture=picture ,shares_count=shares_count, likes_count=likes_count, comment_count=comment_count, likes_sincelastupdate=likes_sincelastupdate, shares_sincelastupdate=shares_sincelastupdate, comment_sincelastupdate=comment_sincelastupdate, team=team, placeid=placeid, placename=placename, updated_time=updated_time, tscore=tscore, fbupdated_time=fbupdated_time)
                fbpl.commit()

        message = "all posts finished"
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=fid,date_time=datetime.datetime.utcnow(),error_msg=message)
        fbpl.commit()


    return dict(message=message)

#5.
@auth.requires_login()
def getPostSocialCount(from_id,fid):
    import datetime
    import time
    graph = getGraph()
    try:
        if fid:
            fb_obj = graph.request(from_id + '_' + fid ,args={'fields': 'id, shares, updated_time,comments.limit(1).summary(true), message, likes.limit(1).summary(true)'})

            shares_count = int(fb_obj["shares"]["count"]) if ('shares' in fb_obj) else 0
            fbupdated_time = datetime.datetime.strptime(fb_obj["updated_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('updated_time' in fb_obj) else ''
            likes_count = int(fb_obj["likes"]["summary"]["total_count"]) if ('likes' in fb_obj) else 0
            comment_count = int(fb_obj["comments"]["summary"]["total_count"]) if ('comments' in fb_obj) else 0
            date_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S' )
            updated_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            updated_time = datetime.datetime.strptime(updated_time,'%Y-%m-%d %H:%M:%S' )
            row = fbpl(fbpl.post.fid==str(fid)).select().first()
            if row :
                fbpl.post_counts.insert(fid=fid, updated_time=updated_time, shares_count=shares_count, date_time=date_time, likes_count=likes_count, comment_count=comment_count)
                fbpl.commit()
                #post used s local_time, it is better in the future all the Fields use the UTC time format
            #    now = datetime.datetime.now()
            #    hour48 = hourdiff(now,48)
            #    row2 = fbpl((fbpl.post_counts.date_time >= hour48) & (fbpl.post_counts.fid==fid) ).select(fbpl.post_counts.ALL).first()
            #    if row2:
            #        likes_sincelastupdate = int(likes_count)-int(row2.likes_count) if likes_count else 0
            #        shares_sincelastupdate = int(shares_count)-int(row2.shares_count) if shares_count else 0
            #        comment_sincelastupdate = int(comment_count)-int(row2.comment_count) if comment_count else 0
            #    else:  #if no record can be found in the post_counts then use the last time number
            #        likes_sincelastupdate = int(likes_count)-int(row.likes_count) if likes_count else 0
            #        shares_sincelastupdate = int(shares_count)-int(row.shares_count) if shares_count else 0
            #        comment_sincelastupdate = int(comment_count)-int(row.comment_count) if comment_count else 0
            #
                likes_sincelastupdate = int(likes_count)-int(row.likes_count) if likes_count else 0
                shares_sincelastupdate = int(shares_count)-int(row.shares_count) if shares_count else 0
                comment_sincelastupdate = int(comment_count)-int(row.comment_count) if comment_count else 0
                list1 = getPostCount(fid, 0, 2)
                likes_count48= list1[0]
                comment_count48= list1[1]
                shares_count48= list1[2]
                fscore = shares_count48*0.5 + comment_count48*0.3 + likes_count48*0.2
                tscore = shares_count*0.5 + comment_count*0.3 + likes_count*0.2
                row.update_record(fbupdated_time=fbupdated_time,updated_time=updated_time, shares_count=shares_count, likes_count=likes_count, comment_count=comment_count,likes_sincelastupdate=likes_sincelastupdate,shares_sincelastupdate=shares_sincelastupdate,comment_sincelastupdate=comment_sincelastupdate, fscore=fscore, likes_count48=likes_count48, comment_count48=comment_count48, shares_count48=shares_count48, tscore=tscore)


            time.sleep(1)
            message='Successfully update the PostSocialCount'
            return dict(message=message)
        else:
            return dict(message='failure, please check your placeid!')

    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=fid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()

    #response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=message)  #dict(message=str[9])



#6

@auth.requires_login()
def countAllPostSocialCount():
    import datetime
    import time
    now = datetime.datetime.utcnow()
    #Only do the update when the tscore > 0 or the post is updated in the last two weeks
    week2 = (now - datetime.timedelta(hours=24*14)).strftime('%Y-%m-%d %H:%M:%S+0000')
    rows = fbpl(( fbpl.post.tscore <> 0) | (fbpl.post.updated_time > week2 ) ).select(fbpl.post.fid,fbpl.post.from_id, orderby=fbpl.post.id)
    start_date_time=datetime.datetime.today()

    for row in rows:
        gid= row.fid
        from_id = row.from_id
        #check if the Facebook has the graphic
        getPostSocialCount(from_id,gid)


    end_date_time=datetime.datetime.today()
    fbpl.update_log.insert(start_date_time=start_date_time,end_date_time=end_date_time)
    message = 'Successfully update socialcount of posts'
    return dict(message=message)

#7
def teamCount():
    errorMsg="success made the teamCount"
    candidates = []
    candidates.append("連勝文")
    candidates.append("柯文哲")
    candidates.append("顧立雄")
    
    results=OrderedDict()
    try:
        for candidate in candidates:

            total_active_posts = 0
            total_post_likes = 0
            total_post_comments = 0
            total_post_shares = 0
            rows = fbpl( (fbpl.post.team == candidate ) & (fbpl.post.tscore > 0 )).select()
            for row in rows:
                total_post_likes += row.likes_count
                total_post_comments += row.comment_count
                total_post_shares += row.shares_count

            total_active_posts = len(rows)
#---------------------------------------------------------------------------------------------#
            hour48_active_posts =0
            hour48_post_likes = 0
            hour48_post_comments = 0
            hour48_post_shares = 0

            rows = fbpl( ((fbpl.post.team == candidate) & ( fbpl.post.fscore > 0))  ).select()

            for row in rows:
                hour48_post_likes += row.likes_count48
                hour48_post_comments += row.comment_count48
                hour48_post_shares += row.shares_count48

            hour48_active_posts = len(rows)

#---------------------------------------------------------------------------------------------#
            hour48_active_stories =0
            hour48_story_likes = 0
            hour48_story_comments = 0
            hour48_story_shares = 0

            rows = fbpl( ((fbpl.post.team == candidate) & ( fbpl.post.fscore > 0)) & ((fbpl.post.ptype == 'photo') | ( fbpl.post.ptype == 'status'))  ).select()
            for row in rows:
                hour48_story_likes += row.likes_count48
                hour48_story_comments += row.comment_count48
                hour48_story_shares += row.shares_count48

            hour48_active_stories = len(rows)


#---------------------------------------------------------------------------------------------#
            hour48_active_links =0
            hour48_link_likes = 0
            hour48_link_comments = 0
            hour48_link_shares = 0

            rows = fbpl( ((fbpl.post.team == candidate) & ( fbpl.post.fscore > 0) &( fbpl.post.ptype == 'link') ) ).select() #| ((fbpl.post.team == candidate) & (fbpl.post.created_time >= week ))
            for row in rows:
                hour48_link_likes += row.likes_count48
                hour48_link_comments += row.comment_count48
                hour48_link_shares += row.shares_count48

            hour48_active_links = len(rows)

#---------------------------------------------------------------------------------------------#
            hour48_active_videos =0
            hour48_video_likes = 0
            hour48_video_comments = 0
            hour48_video_shares = 0

            rows = fbpl( ((fbpl.post.team == candidate) & ( fbpl.post.fscore > 0) &( fbpl.post.ptype == 'video') )  ).select() #| ((fbpl.post.team == candidate) & (fbpl.post.created_time >= week ))
            for row in rows:
                hour48_video_likes += row.likes_count48
                hour48_video_comments += row.comment_count48
                hour48_video_shares += row.shares_count48

            hour48_active_videos = len(rows)

            date_time = datetime.datetime.utcnow().strftime('%Y%m%d')
            date_time = datetime.datetime.strptime(date_time, '%Y%m%d')
            
            checkins=0
            likes=0
            were_here_count=0
            talking_about_count=0
            checkins24=0
            likes24=0
            were_here_count24=0
            talking_about_count24=0
            
            
            Pages = fbpl(fbpl.page.team == candidate).select()
            
            for page in Pages:
                
                checkins += page.checkins
                likes += page.likes
                were_here_count += page.were_here_count
                talking_about_count += page.talking_about_count
                checkins24 += page.checkins24
                likes24 += page.likes24
                were_here_count24 += page.were_here_count24
                talking_about_count24 += page.talking_about_count24

            # check it team_counts has data in the same date, if YES, update the record, if NOT, then insert the new records.

            row = fbpl( ((fbpl.team_counts.team == candidate)  & ( fbpl.team_counts.date_time == date_time))).select().first()
            
            if row:
                row.update_record(checkins=checkins, likes=likes, were_here_count=were_here_count, talking_about_count=talking_about_count, total_active_posts=total_active_posts, total_post_likes=total_post_likes, total_post_comments=total_post_comments ,total_post_shares=total_post_shares, hour48_post_likes=hour48_post_likes, hour48_post_comments=hour48_post_comments, hour48_post_shares=hour48_post_shares, hour48_active_posts = hour48_active_posts, hour48_active_links =hour48_active_links, hour48_link_likes = hour48_link_likes, hour48_link_comments = hour48_link_comments, hour48_link_shares = hour48_link_shares, hour48_active_videos = hour48_active_videos, hour48_video_likes = hour48_video_likes, hour48_video_comments = hour48_video_comments, hour48_video_shares = hour48_video_shares, hour48_active_stories = hour48_active_stories, hour48_story_likes = hour48_story_likes, hour48_story_comments = hour48_story_comments, hour48_story_shares = hour48_story_shares, checkins24=checkins24, likes24=likes24, were_here_count24=were_here_count24, talking_about_count24=talking_about_count24)
            else:
                fbpl.team_counts.insert( team = candidate, date_time = date_time, checkins=checkins, likes=likes, were_here_count=were_here_count, talking_about_count=talking_about_count, total_active_posts=total_active_posts, total_post_likes=total_post_likes, total_post_comments=total_post_comments ,total_post_shares=total_post_shares, hour48_post_likes=hour48_post_likes, hour48_post_comments=hour48_post_comments, hour48_post_shares=hour48_post_shares, hour48_active_posts = hour48_active_posts, hour48_active_links =hour48_active_links, hour48_link_likes = hour48_link_likes, hour48_link_comments = hour48_link_comments, hour48_link_shares = hour48_link_shares, hour48_active_videos = hour48_active_videos, hour48_video_likes = hour48_video_likes, hour48_video_comments = hour48_video_comments, hour48_video_shares = hour48_video_shares, hour48_active_stories = hour48_active_stories, hour48_story_likes = hour48_story_likes, hour48_story_comments = hour48_story_comments, hour48_story_shares = hour48_story_shares, checkins24=checkins24, likes24=likes24, were_here_count24=were_here_count24, talking_about_count24=talking_about_count24)
                fbpl.commit()
            
    except:
        raise
        #errorMsg=  "Unexpected error:", sys.exc_info()[0]
    return errorMsg


#8
def dailySum():
    

    
    candidates = []
    candidates.append("連勝文")
    candidates.append("柯文哲")
    candidates.append("顧立雄")
    date = datetime.datetime.strptime("2014-04-29 00:00:00", '%Y-%m-%d %H:%M:%S')
    
    while date <= datetime.datetime.now():
        #list=[]
        for candidate in candidates:
            dailyPagelikes=0
            talkingAbout=0
            dailyPosts = 0
            dailyPostLikes=0
            dailyPostComments=0
            dailyPostShares=0
            pages = fbpl(fbpl.page.team == candidate).select(fbpl.page.ALL)
            date2 = date + datetime.timedelta(hours=24)
            #date3 = date - datetime.timedelta(hours=24)
            for page in pages:
                likes1 = fbpl((fbpl.social_counts.placeid == page.pageid) & (fbpl.social_counts.updated_time >= date) ).select().first()
                likes2 = fbpl((fbpl.social_counts.placeid == page.pageid) & (fbpl.social_counts.updated_time >= date2)).select().first()
                
                
                
                if likes1:
                    if likes2 :
                        dailyPagelikes += (likes2.likes - likes1.likes)
                        talkingAbout += (likes1.talking_about_count + likes2.talking_about_count)/2
                
                post1 =  fbpl((fbpl.post.from_id == str(page.pageid))).select()
                list= []
                for post in post1:
                    list = getPostCountDate(post.fid, date.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d'))
                   
                    dailyPostLikes = dailyPostLikes +  list[0]
                    dailyPostComments =  dailyPostComments  +  list[1]
                    dailyPostShares = dailyPostShares  +  list[2]
                    
                    
            Posts = fbpl((fbpl.post.team == candidate) & (fbpl.post.status_type <> '') & (fbpl.post.created_time >= date) & (fbpl.post.created_time < date2) ).select()
            dailyPosts =len(Posts)
            
            row = fbpl((fbpl.dailySum.date == date) & (fbpl.dailySum.team == candidate) ).select().first()
            if row:
                row.update_record(dailyPagelikes=dailyPagelikes, talkingAbout=talkingAbout,team=candidate, dailyPosts=dailyPosts, dailyPostLikes=dailyPostLikes, dailyPostComments=dailyPostComments, dailyPostShares=dailyPostShares)
            else:
                fbpl.dailySum.insert(date=date,dailyPagelikes=dailyPagelikes, talkingAbout=talkingAbout,team=candidate, dailyPosts=dailyPosts, dailyPostLikes=dailyPostLikes, dailyPostComments=dailyPostComments, dailyPostShares=dailyPostShares)
                fbpl.commit()
        date += datetime.timedelta(hours=24) 
    return "OK"



#Field('dailyPagelikes','integer'), Field('talkingAbout','integer'), Field('dailyPosts','integer'),Field('dailyPostLikes','integer'), #Field('dailyPostComments','integer'), Field('dailyPostShares','integer')



def test2():
    now= datetime.datetime.utcnow()
    #month2 = (now - datetime.timedelta(hours=24*28*2)).strftime('%Y-%m-%dT%H:%M:%S') #2014-04-24T17:57:21+0000
    #hour48 = (now - datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
    #hour48 = datetime.datetime.strptime(hour48,'%Y-%m-%d %H:%M:%S')
    #now= datetime.datetime.utcnow()
    #week2 = (now - datetime.timedelta(hours=24*14)).strftime('%Y-%m-%dT%H:%M:%S+0000') #2014-04-24T17:57:21+0000
    #month2 = datetime.datetime.strptime(month2,'%Y-%m-%dT%H:%M:%S+0000')
    now = datetime.datetime.utcnow()
    week2 = (now - datetime.timedelta(hours=24*14)).strftime('%Y-%m-%d %H:%M:%S+0000')
    rows = fbpl(( fbpl.post.tscore <> 0) | (fbpl.post.created_time > week2 ) ).select(fbpl.post.fid)

    #row = fbpl(fbpl.post.created_time >= week2).select(fbpl.post.ALL).first()
    return str(rows) #row.date_time



def hourdiff(now, hour):
    hour = (now - datetime.timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.strptime(hour,'%Y-%m-%d %H:%M:%S')

    return hour




def getOpengraphImage(url):
    op={}
    image=''
    if (url and url<>""):
        try:
            op = ExtendedOpenGraph.parse(url)
            image = op['image']
        except:
            image=''
    return image


@auth.requires_login()
def index():
    user = auth.user
    response.flash = T('You are %(name)s', dict(name=user['first_name']))
    if  len(request.args) >= 2 and request.args[0] == 'id':
        fb_id = request.args[1]
    else:
        fb_id = 'me'

    graph = getGraph()
    try:
        fb_obj = graph.get_object(fb_id, metadata=1)
    except GraphAPIError, e:
        response.flash = "%s [%s: %s]" % (T("Logging you out!"),__name__, e)
        redirect(auth.url(f='user', args='logout'))

    response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=T('You are at  %(fb_id)s', dict(fb_id=fb_id)))

@auth.requires_login()
def connection():
    user = auth.user
    if not len(request.args) >= 2:
        return None
    fb_id = request.args[0]
    fb_connection_name = request.args[1]
    try:
        connections = getGraph().get_connections(fb_id, fb_connection_name)
    except GraphAPIError, e:
        response.flash = "%s [%s: %s]" % (T("Logging you out!"),__name__, e)
        redirect(auth.url(f='user', args='logout'))


    response.menu=[[v['name'], False, URL(r=request, f='index', args=['id', v['id']])]  for v in connections['data']]
    return dict(message=T('Looking list of %(conn_name)s of %(id)s', dict(conn_name=fb_connection_name, id=fb_id)))




@auth.requires_login()
def loading_list():
    user = auth.user
    import csv, sys
    import datetime
    import time

    graph = getGraph()
    reader = open('/Users/logyuan/Dropbox/FB_socialcount/keelung.csv', "U")
    errorMsg = ''
    for fbplace in csv.reader(reader):
        try:
            id = str(fbplace[0])
            row = fbpl.place(placeid=id)
            if not row:
                try:
                    fb_obj = graph.get_object(str(fbplace[0]))
                    #id= fb_obj["id"]
                    name =  fb_obj["name"]
                    category = fb_obj["category"]
                    link= fb_obj["link"]
                    #checkins= fb_obj["checkins"]
                    zip= fb_obj["location"]["zip"]
                    try:
                        category_list =  fb_obj["category_list"]
                    except:
                        category_list = ''
                    try:
                        latitude= fb_obj["location"]["latitude"]
                        longitude= fb_obj["location"]["longitude"] if (fb_obj["location"]["longitude"]) else ""
                    except:
                        latitude =''
                        longitude=''
                    fbpl.place.insert(placeid=id,name = name,latitude=latitude,longitude=longitude,category=category,category_list=category_list,zip=zip,link=link)
                except GraphAPIError, e:
                    errorMsg = errorMsg + 'errorID:'  + str(fbplace[0]) + 'errorMessage: ' +  str(e) + ','
                fbpl.commit()
                message='Successfully adding new place into the database'

                time.sleep(8)
        except GraphAPIError, e:
            errorMsg = errorMsg + 'errorID:'  + str(fbplace[0])  + ' errorMessage:'  +  str(e) + ','
    reader.close()
        # or "rU"

    return dict(message=T('list complete'),errorMsg=errorMsg )




@auth.requires_login()
def getPost(gid):
    graph = getGraph()
    try:
        if gid:
            fb_obj = graph.request(gid,args={'fields': 'id, message, updated_time, from, created_time, status_type, type, link, likes.limit(1).summary(true), shares, comments.limit(1).summary(true), object_id, picture'})
            fid= fb_obj["id"]
            message =  fb_obj["message"] if ('message' in fb_obj) else ''
            created_time = datetime.datetime.strptime(fb_obj["created_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('created_time' in fb_obj) else ''
            updated_time = datetime.datetime.strptime(fb_obj["updated_time"],'%Y-%m-%dT%H:%M:%S+0000') if  ('updated_time' in fb_obj) else ''
            from_id = fb_obj["from"]["id"] if ('from' in fb_obj) else ''
            from_name = fb_obj["from"]["name"] if ('from' in fb_obj) else ''
            status_type = fb_obj["status_type"] if ('status_type' in fb_obj) else ''
            ptype = fb_obj["type"] if ('type' in fb_obj) else ''
            status_type = fb_obj["status_type"] if ('status_type' in fb_obj) else ''
            link =  fb_obj["link"] if ('link' in fb_obj) else ''
            #picture =  fb_obj["picture"] if ('picture' in fb_obj) else ''
            shares_count = fb_obj["shares"]['count'] if ('shares' in fb_obj) else 0
            likes_count = fb_obj["likes"]["summary"]["total_count"] if ('summary' in fb_obj) else 0
            comment_count = fb_obj["comments"]["summary"]["total_count"] if ('summary' in fb_obj) else 0
            object_id = fb_obj["object_id"] if ('object_id' in fb_obj) else ''
            row=fbpl(fbpl.page.pageid==from_id).select().first()
            team = row['team']
            if (ptype == 'link' ) | (ptype == 'video'):
                try:
                    picture =getOpengraphImage(link)
                    if picture == '':
                        picture = post["picture"] if ('picture' in post) else ''
                except:
                    picture = post["picture"] if ('picture' in post) else ''
            elif (ptype == 'photo' ) :
                try:
                    images=[]
                    images =graph.request(object_id , args={'fields':'images'})["images"]
                    for image in images:
                        if (image["height"] > 200):
                            picture = image["source"]
                except:
                    picture = post["picture"] if ('picture' in post) else ''
            else:
                picture = post["picture"] if ('picture' in post) else ''


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
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.utcnow(),error_msg=message)
        fbpl.commit()


    return dict(message=message)


@auth.requires_login()
def getPage(gid,team):
    graph = getGraph()
    try:
        if gid:
            fb_obj = graph.request(gid ,args={'fields': 'id, name, category, about, can_post, checkins, talking_about_count, were_here_count, link,description, cover, website, picture.type(large), is_published,likes.limit(1).summary(true), insights'})
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
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.utcnow(),error_msg=message)
        fbpl.commit()


    return dict(message=message)
















@auth.requires_login()
def getPlace(gid):
    import datetime
    import time
    graph = getGraph()
    try:
        gid = checkGraphId(gid)
        if gid <> '0':
            fb_obj = graph.get_object(gid)
            row = fbpl.place(placeid=gid)
            if not row:
                name =  fb_obj["name"] if ('name' in fb_obj) else ''
                category = fb_obj["category"] if ('category' in fb_obj) else ''
                category_list =  fb_obj["category_list"] if ('category_list' in fb_obj) else ''
                link= fb_obj["link"] if ('link' in fb_obj) else ''
                website =fb_obj["website"] if ('website' in fb_obj) else ''
                phone =fb_obj["phone"] if ('phone' in fb_obj) else ''
                description =fb_obj["description"] if ('description' in fb_obj) else ''

                if ('location' in fb_obj):
                    zip= fb_obj["location"]["zip"] if ('zip' in fb_obj["location"]) else ''
                    street= fb_obj["location"]["street"] if ('street' in fb_obj["location"]) else ''
                    city= fb_obj["location"]["city"] if ('city' in fb_obj["location"]) else ''
                    state= fb_obj["location"]["state"] if ('state' in fb_obj["location"]) else ''
                    country=fb_obj["location"]["country"] if ('country' in fb_obj["location"]) else ''
                    latitude= fb_obj["location"]["latitude"] if ('latitude' in fb_obj["location"]) else ''
                    longitude= fb_obj["location"]["longitude"] if ('longitude' in fb_obj["location"]) else ''
                    mutiple = 'No'
                else:
                    zip= ''
                    street= ''
                    city= ''
                    state= ''
                    country= ''
                    latitude= ''
                    longitude= ''
                old_ids = ''
                fbpl.place.insert(placeid=gid,name = name,latitude=latitude,longitude=longitude,category=category,category_list=category_list,zip=zip,link=link,old_ids=old_ids)

            fbpl.commit()
            message='Successfully adding new place into the database'
        else:
            message='failure, please check your placeid!'
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=gid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()


    return dict(message=message)


@auth.requires_login()
def getPlace_f():
    graph = getGraph()
    try:
        if request.vars['gid']:
            gid = request.vars['gid']
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
        fbpl.graphAPI_Error.insert(placeid=pid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()


    return dict(message=message)

@auth.requires_login()
def getEvent(eid):
    graph = getGraph()
    try:
        event= graph.get_object(eid)
        eventid = event["id"] if 'id' in event else ''
        row = fbpl.event(eventid=eventid)
        if not row:
            description = event["description"] if 'description' in event else ''
            end_time  = event["end_time"] if 'end_time' in event else ''
            timezone = event["timezone"] if 'timezone' in event else ''
            name = event["name"] if 'name' in event else ''
            location = event["location"] if 'location' in event else ''
            ownerid = event["owner"]["id"] if 'owner' in event else ''
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
            fbpl.event.insert(eventid=eventid, description=description, end_time=end_time, timezone=timezone, name=name, location=location, ownerid=ownerid, picture=picture, privacy=privacy, start_time=start_time, ticket_uri=ticket_uri, updated_time=updated_time, is_date_only=is_date_only, venuename=venuename, venueid=venueid, country=country, city=city, state=state, street=street, zipcode=zipcode, longitude=longitude, latitude=latitude)
            fbpl.commit()
            message='Successfully adding new event into the database'
        else:
            message='failure, please check your eventid!'
    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=eventid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()
    return dict(message=message)

@auth.requires_login()
def getSocialCount():
    import datetime
    import time
    graph = getGraph()
    try:
        if request.vars['gid']:
            oid = request.vars['gid']
        else:
            message='failure, please check your placeid!'
            return dict(message=message)
        pid = checkGraphId(oid)
        if pid <> '0':
            if pid <> oid :
                record = fbpl(fbpl.place.placeid==oid).select().first()
                record2 = fbpl(fbpl.place.placeid==pid).select().first()
                if not (record2) :
                   getPlace(pid)
                   time.sleep(1)
                   record2 = fbpl(fbpl.place.placeid==pid).select().first()
                   oids = []
                   oids.append(oid)
                   record2.update_record(old_ids=oids)
                   fbpl(fbpl.place.placeid==oid).delete()
                else:
                   fbpl(fbpl.place.placeid==oid).delete()
                   oids = []
                   oids.append(record2.old_ids)
                   oids.append(oid)
                   record2.update_record(old_ids=oids)
            fb_obj = graph.get_object(pid)
            try:
                checkins =  fb_obj["checkins"]
            except:
                checkins=''
            try:
                likes= fb_obj["likes"]
            except:
                likes=''
            try:
                were_here_count= fb_obj["were_here_count"]
            except:
                were_here_count=''
            date_time = datetime.datetime.utcnow()
            fbpl.social_counts.insert(placeid=pid,checkins = checkins,likes=likes,date_time=date_time,were_here_count=were_here_count)
            fbpl.commit()
            time.sleep(1.1)
            message='Successfully found the place'
            return dict(message=message)
        else:
            return dict(message='failure, please check your placeid!')

    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=pid,date_time=datetime.datetime.utcnow(),error_msg=message)
        fbpl.commit()

    #response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=message)  #dict(message=str[9])

@auth.requires_login()
def getSocialCount_f(gid):
    import datetime
    import time
    graph = getGraph()
    try:
        if gid:
            oid = gid
        else:
            message='failure, please check your placeid!'
            return dict(message=message)
        pid = checkGraphId(oid)
        if pid <> '0':
            if pid <> oid :
                record = fbpl(fbpl.place.placeid==oid).select().first()
                record2 = fbpl(fbpl.place.placeid==pid).select().first()
                if not (record2) :
                    getPlace(pid)
                    time.sleep(1)
                    record2 = fbpl(fbpl.place.placeid==pid).select().first()
                    oids = []
                    oids.append(oid)
                    record2.update_record(old_ids=oids)
                    fbpl(fbpl.place.placeid==oid).delete()
                else:
                   fbpl(fbpl.place.placeid==oid).delete()
                   oids = []
                   oids.append(record2.old_ids)
                   oids.append(oid)
                   record2.update_record(old_ids=oids)
            fb_obj = graph.get_object(pid)
            try:
                checkins =  fb_obj["checkins"]
            except:
                checkins=''
            try:
                likes= fb_obj["likes"]
            except:
                likes=''
            try:
                were_here_count= fb_obj["were_here_count"]
            except:
                were_here_count=''
            date_time = datetime.datetime.today()
            fbpl.social_counts.insert(placeid = pid, checkins = checkins,likes=likes,date_time=date_time,were_here_count=were_here_count)
            fbpl.commit()
            time.sleep(1.1)
            message='Successfully found the place'
            return dict(message=message)
        else:
            return dict(message='failure, please check your placeid!')

    except GraphAPIError, e:
        message=e.result
        fbpl.graphAPI_Error.insert(placeid=pid,date_time=datetime.datetime.today(),error_msg=message)
        fbpl.commit()
    except:
        raise

    #response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=message)  #dict(message=str[9])





@auth.requires_login()
def checkGraphId_f():
    import datetime
    import time
    graph = getGraph()
    if request.vars['gid']:
        graphid = request.vars['gid']
    else:
        return dict(message='failure, please check your placeid!')

    new_graphid = graphid
    try:
        fb_obj = graph.get_object(graphid)
    except GraphAPIError, r:
        message=r.result
        code =message['error']['code']
        fbpl.graphAPI_Error.insert(placeid=graphid,date_time=datetime.datetime.today(),code =code,error_msg=message)
        fbpl.commit()
        if code == 21:
            id=message['error']['message'].split(' ')
            new_graphid = id[9].strip('.')
            try:
                fb_obj = graph.get_object(new_graphid)
            except GraphAPIError, e:
                time.sleep(1)
                new_graphid = checkGraphId(new_graphid)
            try:
                row = fbpl.place(placeid=graphid)
                fbpl.merged_place.insert(placeid=graphid,date_time=datetime.datetime.today(),merge_to = new_graphid,name = row.name, latitude=row.latitude,longitude=row.longitude,category=row.category,category_list=row.category_list,zip=row.zip,link=row.link,old_ids=row.old_ids)
            except:
                message = 'No this id in the DB'
        else:
            new_graphid = '0'

    return new_graphid




@auth.requires_login()
def checkGraphId(graphid):
    import datetime
    import time
    graph = getGraph()
    new_graphid = graphid
    try:
        fb_obj = graph.get_object(graphid)
    except GraphAPIError, r:
        message=r.result
        code =message['error']['code']
        fbpl.graphAPI_Error.insert(placeid=graphid,date_time=datetime.datetime.today(),code =code,error_msg=message)
        fbpl.commit()
        if code == 21:
            id=message['error']['message'].split(' ')
            new_graphid = id[9].strip('.')
            try:
                fb_obj = graph.get_object(new_graphid)
            except GraphAPIError, e:
                time.sleep(1)
                new_graphid = checkGraphId(new_graphid)
            try:
                row = fbpl.place(placeid=graphid)
                fbpl.merged_place.insert(placeid=graphid,date_time=datetime.datetime.today(),merge_to = new_graphid,name = row.name, latitude=row.latitude,longitude=row.longitude,category=row.category,category_list=row.category_list,zip=row.zip,link=row.link,old_ids=row.old_ids)
            except:
                message = 'No this id in the DB'
        else:
            new_graphid = '0'

    return new_graphid


@auth.requires_login()
def countAllPlaceSocialCount():
    import datetime
    import time

    graph = getGraph()
    rows = fbpl().select(fbpl.place.placeid,fbpl.place.old_ids, orderby=fbpl.place.id)
    start_date_time=datetime.datetime.today()

    for row in rows:
        pid= row.placeid
        #check if the Facebook has the graphic
        getSocialCount_f(pid)

    end_date_time=datetime.datetime.today()
    fbpl.update_log.insert(start_date_time=start_date_time,end_date_time=end_date_time)
    message = 'Successfully update socialcount of places'
    return dict(message=message)









@auth.requires_login()
def countTscore():
    #fbpl(fbpl.post.id>0).update(tscore= fbpl.post.likes_count*0.2+fbpl.post.shares_count*0.5+fbpl.post.comment_count*0.3)
    rows= fbpl().select(fbpl.post.ALL)
    for row in rows:
        tscore = row.shares_count*0.5 + row.comment_count*0.3 + row.likes_count*0.2
        row.update_record(tscore=tscore)
    return "success"



@auth.requires_login()
def getPageCount(fid, hour, day):

    now = datetime.datetime.now()
    hours = hour + day*24
    from_date = hourdiff(now,hours)

    rows = fbpl((fbpl.social_counts.placeid==fid) & (fbpl.social_counts.date_time >= from_date )).select( orderby= ~fbpl.social_counts.date_time)
    if rows:
        total_page_checkins= rows.first()['checkins'] - rows.last()['checkins']
        total_page_likes = rows.first()['likes'] - rows.last()['likes']
        total_page_whc = rows.first()['were_here_count'] - rows.last()['were_here_count']
        total_page_tac = rows.first()['talking_about_count'] - rows.last()['talking_about_count']
    else:
        total_page_checkins= 0
        total_page_likes = 0
        total_page_whc = 0
        total_page_tac = 0
    result = [total_page_checkins,total_page_likes,total_page_whc,total_page_tac]
    return result



@auth.requires_login()
def getPostCount(fid, hour, day):
    #fid, hour, day
    #hour =96
    #day = 0
    #fid = '466328090135843'

    now = datetime.datetime.now()
    hours = hour + day*24
    from_date = hourdiff(now,hours)

    rows = fbpl((fbpl.post_counts.fid==fid) & (fbpl.post_counts.date_time >= from_date )).select( orderby= ~fbpl.post_counts.date_time)
    if rows:
        total_post_likes = rows.first()['likes_count'] - rows.last()['likes_count']
        total_post_comments = rows.first()['comment_count'] - rows.last()['comment_count']
        total_post_shares = rows.first()['shares_count'] - rows.last()['shares_count']
    else:
        total_post_likes = ''
        total_post_comments = ''
        total_post_shares = ''
    result = [total_post_likes,total_post_comments,total_post_shares]
    return result



@auth.requires_login()
def getPageCountDate(fid, from_date, to_date):
    #fid, from_date, to_date
    #fid = '543656759040101'
    #from_date = '2014-4-25'
    #to_date = '2014-4-30'
    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d')
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d')

    rows = fbpl((fbpl.social_counts.placeid==fid) & (fbpl.social_counts.date_time >= from_date ) & (fbpl.social_counts.date_time <= to_date )).select()

    if rows:
        total_page_checkins= rows.first()['checkins'] - rows.last()['checkins']
        total_page_likes = rows.first()['likes'] - rows.last()['likes']
        total_page_whc = rows.first()['were_here_count'] - rows.last()['were_here_count']
        total_page_tac = (rows.first()['talking_about_count'] + rows.last()['talking_about_count'])/2
    else:
        total_page_checkins=''
        total_page_likes = ''
        total_page_whc = ''
        total_page_tac = ''

    result = [total_page_checkins,total_page_likes,total_page_whc,total_page_tac]
    return result

@auth.requires_login()
def getPostCountDate(fid, from_date, to_date):

    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d')
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d')

    rows = fbpl((fbpl.post_counts.fid==fid) & (fbpl.post_counts.updated_time >= from_date ) ).select()
    rows1 = fbpl((fbpl.post_counts.fid==fid) & (fbpl.post_counts.updated_time >= to_date )).select()
    if rows:
        if rows1:
            total_post_likes = rows1.first()['likes_count'] - rows.first()['likes_count']
            total_post_comments = rows1.first()['comment_count'] - rows.first()['comment_count']
            total_post_shares = rows1.first()['shares_count'] - rows.first()['shares_count']
        else:
            total_post_likes = rows.last()['likes_count'] - rows.first()['likes_count']
            total_post_comments = rows.last()['comment_count'] - rows.first()['comment_count']
            total_post_shares = rows.last()['shares_count'] - rows.first()['shares_count']            
    else:
        total_post_likes = 0
        total_post_comments = 0
        total_post_shares = 0

    result = [total_post_likes,total_post_comments,total_post_shares]
    return result
