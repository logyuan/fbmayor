# coding:utf8
import ExtendedOpenGraph
import json
from collections import OrderedDict
import datetime
from dateutil import parser, tz
import calendar







def index(): return dict(message="hello from ws.py")


def timeseries():
    candidates = ["連勝文","柯文哲"]
    timeseries={}
    result=OrderedDict()
    date1=[]

    rows = fbpl(fbpl.team_counts.team == "連勝文").select(fbpl.team_counts.ALL, orderby=fbpl.team_counts.date_time)
    for row in rows:
        listdate = row.date_time
        date1.append(listdate.strftime('%Y/%m/%d'))
    result.update({"date":date1})
    result.update({"candidates":candidates})
    r1=[]
    r2=[]
    r3=[]
    r4=[]
    r5=[]
    r6=[]
    for row in rows:
        likes = []
        talkingAbout=[]
        totalPosts=[]
        totalPostLikes=[]
        totalPostComments=[]
        totalPostShares=[]

        date = row.date_time
        date1 = date - datetime.timedelta(days=1)
        date2 = date + datetime.timedelta(days=1)
        date3 = date - datetime.timedelta(hours=8)
        date4 = date2 - datetime.timedelta(hours=8)
        
        

        
        
        row1 = fbpl((fbpl.team_counts.team == "連勝文") & (fbpl.team_counts.date_time>=date1)).select(fbpl.team_counts.ALL).first()
        
        talkingAbout.append(row.talking_about_count)
        
        Posts = fbpl((fbpl.post.team == "連勝文") & (fbpl.post.created_time >= date3) & (fbpl.post.created_time < date4) ).select()
        posts_today=len(Posts)
        totalPosts.append(posts_today)
        
        if row1:
            likes.append(row.likes-row1.likes)
            totalPostLikes.append(row.total_post_likes-row1.total_post_likes)
            totalPostComments.append(row.total_post_comments-row1.total_post_comments)
            totalPostShares.append(row.total_post_shares-row1.total_post_shares)
        else:
            likes.append(0)
            totalPostLikes.append(0)
            totalPostComments.append(0)
            totalPostShares.append(0)

        row2 = fbpl((fbpl.team_counts.team == "柯文哲") & (fbpl.team_counts.date_time>=date) ).select(fbpl.team_counts.ALL).first()

        row3 = fbpl((fbpl.team_counts.team == "柯文哲") & (fbpl.team_counts.date_time>=date1) ).select(fbpl.team_counts.ALL).first()
        
        talkingAbout.append(row2.talking_about_count)
        Posts = fbpl((fbpl.post.team == "柯文哲") &  (fbpl.post.created_time >= date3) & (fbpl.post.created_time < date4) ).select()
        posts_today=len(Posts)
        totalPosts.append(posts_today)
        
        if row3:
            likes.append(row2.likes-row3.likes)
            totalPostLikes.append(row2.total_post_likes-row3.total_post_likes)
            totalPostComments.append(row2.total_post_comments-row3.total_post_comments)
            totalPostShares.append(row2.total_post_shares-row3.total_post_shares)

        else:
            likes.append(0)
            totalPostLikes.append(0)
            totalPostComments.append(0)
            totalPostShares.append(0)
        r1.append(likes)
        r2.append(talkingAbout)
        r3.append(totalPosts)
        r4.append(totalPostLikes)
        r5.append(totalPostComments)
        r6.append(totalPostShares)

    result.update({"likes":r1})
    result.update({"talkingAbout":r2})
    result.update({"totalPosts":r3})
    result.update({"totalPostLikes":r4})
    result.update({"totalPostComments":r5})
    result.update({"totalPostShares":r6})




    file=open('/Users/logyuan/Documents/git/ElectionPath/db/taipeimayor_timeseries.JSON','w')
    #file=open('Z:\\pathgeo\\github\\ElectionPath\\db\\taipeimayor_timeseries.JSON','w')
    file.write(json.dumps(result, indent=4 , ensure_ascii=False, separators=(',', ': ')))



    return json.dumps(result, indent=4 , ensure_ascii=False, separators=(',', ':'))


def utc_time(strtime):
    #from_zone = tz.tzutc()
    #to_zone = tz.gettz("CST")
    #utctimestamp = calendar.timegm(parser.parse(strtime).timetuple())
    utctime = datetime.datetime.strptime( strtime, '%Y-%m-%d %H:%M:%S')  #2014-04-19T20:30:00-0700
    #utctime = utctime.replace(tzinfo=from_zone)
    # Convert time zone
    central = (utctime + datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')
    #central = utctime.astimezone(to_zone).strftime('%Y-%m-%dT%H:%M:%S')
    return central





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


def exportElectionPath():

    colors={"連勝文":'#018CD5',"柯文哲":'#1ACD02',"顧立雄":'#1ACDCD'}


    candidates = []
    candidates.append("連勝文")
    candidates.append("柯文哲")
    candidates.append("顧立雄")
    results=OrderedDict()

    for candidate in candidates:

        result=OrderedDict()
        likes=0
        talking_about_count=0
        likes_sincelastupdate=0
        talking_about_sincelastupdate=0

        picture=''
        url_facebook=''
        

        
        Pages = fbpl(fbpl.page.team == candidate).select(orderby=fbpl.page.likes)
        for page in Pages:
            ts=OrderedDict()
            likes += page.likes
            talking_about_count+= page.talking_about_count
            likes_sincelastupdate += page.likes24
            talking_about_sincelastupdate += page.talking_about_count24

        FPage = fbpl(fbpl.page.team == candidate).select(orderby=fbpl.page.likes).last()

        ts=OrderedDict()
        ts.update({"name": candidate})
        ts.update({"backgroundColor": colors[candidate]})
        ts.update({"image": FPage.picture})
        updateTime = str(FPage.updated_time)
        ts.update({"updatedTime": utc_time(updateTime)})
        ts.update({"likes": likes})
        #ts.update({"were_here_count": were_here_count})
        ts.update({"talking_about_count": talking_about_count})
        ts.update({"likes_sincelastupdate": likes_sincelastupdate})
        #ts.update({"were_here_sincelastupdate": were_here_sincelastupdate})
        ts.update({"talking_about_sincelastupdate": talking_about_sincelastupdate})
        result.update(ts)
        
        
        
        
        ts=OrderedDict()
        ts.update({"name": FPage.name})
        ts.update({"url": FPage.link})
        since = '2014-03-19' if candidate == '連勝文' else '2011-10-20'
        ts.update({"since": since})
        ts.update({"likes": FPage.likes})
        ts.update({"talking_about_count": FPage.talking_about_count})
        ts.update({"likes_sincelastupdate":FPage.likes24})
        ts.update({"talking_about_sincelastupdate": FPage.talking_about_count24})
        
        result.update({'officialPage':ts})
        
        fanPages=[]
        for page in Pages.exclude(lambda page: page.pageid<>FPage.pageid):
            ts=OrderedDict()
            ts.update({"name": page.name})
            ts.update({"url": page.link})
            ts.update({"since": '2014'})
            ts.update({"likes": page.likes})
            ts.update({"talking_about_count": page.talking_about_count})
            ts.update({"likes_sincelastupdate":page.likes24})
            ts.update({"talking_about_sincelastupdate": page.talking_about_count24})
            fanPages.append(ts)
            
        result.update({'fanPages':fanPages})



#--------------------------------------------------------------------------------------------------------------#

        team_counts = fbpl(fbpl.team_counts.team == candidate).select(orderby=~fbpl.team_counts.date_time).first()
        total_active_posts=team_counts.total_active_posts
        total_post_likes=team_counts.total_post_likes
        total_post_comments=team_counts.total_post_comments
        total_post_shares=team_counts.total_post_shares

        hour48_active_posts=team_counts.hour48_active_posts
        hour48_post_likes=team_counts.hour48_post_likes
        hour48_post_comments=team_counts.hour48_post_comments
        hour48_post_shares=team_counts.hour48_post_shares

        hour48_active_stories=team_counts.hour48_active_stories
        hour48_story_likes=team_counts.hour48_story_likes
        hour48_story_comments=team_counts.hour48_story_comments
        hour48_story_shares=team_counts.hour48_story_shares

        hour48_active_links=team_counts.hour48_active_links
        hour48_link_likes=team_counts.hour48_link_likes
        hour48_link_comments=team_counts.hour48_link_comments
        hour48_link_shares=team_counts.hour48_link_shares

        hour48_active_videos=team_counts.hour48_active_videos
        hour48_video_likes=team_counts.hour48_video_likes
        hour48_video_comments=team_counts.hour48_video_comments
        hour48_video_shares=team_counts.hour48_video_shares

#--------------------------------------------------------------------------------------------------------------#
        ts=OrderedDict()
        ts.update({"total_active_posts": total_active_posts})
        ts.update({"total_post_likes": total_post_likes})
        ts.update({"total_post_comments": total_post_comments})
        ts.update({"total_post_shares": total_post_shares})

        result.update({'TopPost_count':ts})
#--------------------------------------------------------------------------------------------------------------#
        TopPost=[]
        Posts = fbpl((fbpl.post.team == candidate)).select( orderby =~fbpl.post.tscore  ,limitby=(0,3))
        i=1

        for Post in Posts:
            ts=OrderedDict()
            ts.update({"rank": i})
            ts.update({"score": Post['tscore']})
            ts.update({"tscore": Post['tscore']})
            ts.update({"fscore": Post['fscore']})
            ts.update({"message": Post['message']})
            ts.update({"from_id": Post['from_id']})
            from_picture=fbpl(fbpl.page.pageid==Post['from_id']).select(fbpl.page.picture).first()["picture"]
            ts.update({"from_picture": from_picture})
            ts.update({"from_name": Post['from_name']})
            created_time = str(Post['created_time'])
            ts.update({"created_time": utc_time(created_time)})
            updated_time = str(Post['updated_time'])
            ts.update({"updated_time": utc_time(updated_time)})
            ts.update({"shares_count": Post['shares_count']})
            ts.update({"comment_count": Post['comment_count']})
            ts.update({"likes_count": Post['likes_count']})
            ts.update({"shares_sincelastupdate": Post['shares_count48']})
            ts.update({"comment_sincelastupdate": Post['comment_count48']})
            ts.update({"likes_sincelastupdate": Post['likes_count48']})
            ts.update({"link": Post['link']})
            ts.update({"picture": Post['picture']})
            #picture = getOpengraphImage(story['link'])
            #ts.update({"picture": picture})

            i=i+1
            TopPost.append(ts)

        result.update({'TopPost':TopPost})
#--------------------------------------------------------------------------------------------------------------#
        ts=OrderedDict()
        ts.update({"hour48_active_stories": hour48_active_stories})
        ts.update({"hour48_post_likes": hour48_post_likes})
        ts.update({"hour48_post_comments": hour48_post_comments})
        ts.update({"hour48_post_shares": hour48_post_shares})

        result.update({'HotStory_count':ts})
#--------------------------------------------------------------------------------------------------------------#

        HotStory=[]
        Stories = fbpl( ((fbpl.post.ptype == 'status') | (fbpl.post.ptype == 'photo' )) & (fbpl.post.team == candidate) & (fbpl.post.fscore > 0.0 )).select( orderby =~fbpl.post.fscore , groupby = fbpl.post.object_id ,limitby=(0,10))
        i=1

        for story in Stories:
            ts=OrderedDict()
            ts.update({"rank": i})
            ts.update({"score": story['fscore']})
            ts.update({"tscore": story['tscore']})
            ts.update({"fscore": story['fscore']})
            ts.update({"message": story['message']})
            ts.update({"from_id": story['from_id']})
            from_picture=fbpl(fbpl.page.pageid==story['from_id']).select(fbpl.page.picture).first()["picture"]
            ts.update({"from_picture": from_picture})
            ts.update({"from_name": story['from_name']})
            created_time = str(story['created_time'])
            ts.update({"created_time": utc_time(created_time)})
            updated_time = str(story['updated_time'])
            ts.update({"updated_time": utc_time(updated_time)})
            ts.update({"shares_count": story['shares_count']})
            ts.update({"comment_count": story['comment_count']})
            ts.update({"likes_count": story['likes_count']})
            ts.update({"shares_sincelastupdate": story['shares_count48']})
            ts.update({"comment_sincelastupdate": story['comment_count48']})
            ts.update({"likes_sincelastupdate": story['likes_count48']})
            ts.update({"link": story['link']})
            ts.update({"picture": story['picture']})
            i=i+1
            HotStory.append(ts)

        result.update({'HotStory':HotStory})

#--------------------------------------------------------------------------------------------------------------#
        ts=OrderedDict()
        ts.update({"hour48_active_links": hour48_active_links})
        ts.update({"hour48_link_likes": hour48_link_likes})
        ts.update({"hour48_link_comments": hour48_link_comments})
        ts.update({"hour48_link_shares": hour48_link_shares})

        result.update({'HotLink_count':ts})
#--------------------------------------------------------------------------------------------------------------#

        HotLink=[]
        Links = fbpl((fbpl.post.team == candidate) & (fbpl.post.ptype == 'link') & (fbpl.post.fscore > 0.0 ) ).select( orderby =~fbpl.post.fscore, groupby = fbpl.post.object_id ,limitby=(0,10))
        i=1
        for link in Links:
            ts=OrderedDict()
            ts.update({"rank": i})
            ts.update({"score": link['fscore']})
            ts.update({"tscore": link['tscore']})
            ts.update({"fscore": link['fscore']})
            ts.update({"message": link['message']})
            ts.update({"from_id": link['from_id']})
            from_picture=fbpl(fbpl.page.pageid==story['from_id']).select(fbpl.page.picture).first()["picture"]
            ts.update({"from_picture": from_picture})
            ts.update({"from_name": link['from_name']})
            created_time = str(link['created_time'])
            ts.update({"created_time": utc_time(created_time)})
            updated_time = str(link['updated_time'])
            ts.update({"updated_time": utc_time(updated_time)})
            ts.update({"shares_count": link['shares_count']})
            ts.update({"comment_count": link['comment_count']})
            ts.update({"likes_count": link['likes_count']})
            ts.update({"shares_sincelastupdate": link['shares_count48']})
            ts.update({"comment_sincelastupdate": link['comment_count48']})
            ts.update({"likes_sincelastupdate": link['likes_count48']})
            ts.update({"link": link['link']})
            ts.update({"picture": link['picture']})
            #picture = getOpengraphImage(link['link'])
            #if picture == '':
            #    picture =link['picture']
            #ts.update({"picture": picture})
            i=i+1
            HotLink.append(ts)


        result.update({'HotLink':HotLink})

#--------------------------------------------------------------------------------------------------------------#
        ts=OrderedDict()
        ts.update({"hour48_active_videos": hour48_active_videos})
        ts.update({"hour48_video_likes": hour48_video_likes})
        ts.update({"hour48_video_comments": hour48_video_comments})
        ts.update({"hour48_video_shares": hour48_video_shares})

        result.update({'HotVideo_count':ts})
#--------------------------------------------------------------------------------------------------------------#


        HotVideo=[]
        Videos = fbpl((fbpl.post.team == candidate)  & (fbpl.post.ptype == 'video') & (fbpl.post.fscore > 0.0 ) ).select( orderby =~fbpl.post.fscore, groupby = fbpl.post.object_id ,limitby=(0,5))
        i=1
        for video in Videos:
            ts=OrderedDict()
            ts.update({"rank": i})
            ts.update({"score": video['fscore']})
            ts.update({"tscore": video['tscore']})
            ts.update({"fscore": video['fscore']})
            ts.update({"message": video['message']})
            ts.update({"from_id": video['from_id']})
            from_picture=fbpl(fbpl.page.pageid==story['from_id']).select(fbpl.page.picture).first()["picture"]
            ts.update({"from_picture": from_picture})
            ts.update({"from_name": video['from_name']})
            created_time = str(video['created_time'])
            ts.update({"created_time": utc_time(created_time)})
            updated_time = str(video['updated_time'])
            ts.update({"updated_time": utc_time(updated_time)})
            ts.update({"shares_count": video['shares_count']})
            ts.update({"comment_count": video['comment_count']})
            ts.update({"likes_count": video['likes_count']})
            ts.update({"shares_sincelastupdate": video['shares_count48']})
            ts.update({"comment_sincelastupdate": video['comment_count48']})
            ts.update({"likes_sincelastupdate": video['likes_count48']})
            ts.update({"link": video['link']})
            ts.update({"picture": video['picture']})
            #picture = getOpengraphImage(link['link'])
            #if picture == '':
            #    picture =video['picture']
            #ts.update({"picture": picture})
            i=i+1
            HotVideo.append(ts)

        result.update({'HotVideo':HotVideo})

        RecentlyVisited=[]
        Visited = fbpl((fbpl.post.team == candidate)  & (fbpl.post.placeid != '') ).select( orderby =~fbpl.post.id, groupby = fbpl.post.placeid ,limitby=(0,5))
        i=1
        for visit in Visited:
            ts=OrderedDict()
            ts.update({"rank": i})
            ts.update({"from_id": visit['from_id']})
            from_picture=fbpl(fbpl.page.pageid==story['from_id']).select(fbpl.page.picture).first()["picture"]
            ts.update({"from_picture": from_picture})
            ts.update({"from_name": visit['from_name']})
            created_time = str(visit['created_time'])
            ts.update({"created_time": utc_time(created_time)})
            ts.update({"placeid": visit['placeid']})
            ts.update({"placename": visit['placename']})
            row = fbpl(fbpl.place.placeid==visit['placeid']).select().first()
            if row:
                ts.update({"latitude": row.latitude})
                ts.update({"longitude": row.longitude})
            else:
                ts.update({"latitude": None})
                ts.update({"longitude": None})
            i=i+1
            RecentlyVisited.append(ts)

        result.update({'RecentlyVisited':RecentlyVisited})
        results.update({candidate:result})
        file=open('/Users/logyuan/Documents/git/ElectionPath/db/taipeimayor.JSON','w')
        #file=open('Z:\\pathgeo\\github\\ElectionPath\\db\\taipeimayor.JSON','w')
        file.write(json.dumps(results, indent=4 , ensure_ascii=False, separators=(',', ': ')))
        file.close()
        test = timeseries()
    return dict(results=results)
