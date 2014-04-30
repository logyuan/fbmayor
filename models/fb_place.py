# coding: utf8
#fbpl = DAL("sqlite://storage.sqlite", adapter_args=dict(foreign_keys=False))
fbpl = DAL("mongodb://localhost/fbmayor", adapter_args=dict(foreign_keys=False), db_codec='utf8')
fbpl.define_table('people',Field('uid',unique=True),Field('name'),Field('gender'),Field('hometown'),Field('loc_id'),Field('loc_name'),Field('updated_time'),Field('locale'))


fbpl.define_table('post', Field('fid',unique=True), Field('message'), Field('from_id'), Field('from_name'), Field('created_time'), Field('object_id'), Field('ptype'), Field('status_type'), Field('link'), Field('picture'), Field('shares_count','integer',default=0), Field('updated_time'), Field('likes_count','integer',default=0), Field('comment_count','integer', default=0), Field('likes_sincelastupdate','integer',default=0),  Field('shares_sincelastupdate','integer',default=0), Field('comment_sincelastupdate','integer',default=0), Field('team'), Field('placeid'), Field('placename'),Field('fscore','double',default=0),Field('tscore','double',default=0))

fbpl.define_table('post_counts', Field('fid'), Field('date_time', 'datetime'), Field('shares_count','integer'), Field('updated_time'), Field('likes_count','integer'), Field('comment_count','integer'))


fbpl.define_table('page',Field('about'),Field('can_post'),Field('category'),Field('is_published'),Field('pageid',unique=True),Field('name'),Field('link'),Field('description'),Field('updated_time'),Field('cover_id'),Field('cover_source'),Field('source'),Field('locale'),Field('website'),Field('checkins','integer',default=0),Field('likes','integer',default=0),Field('were_here_count','integer',default=0),Field('talking_about_count','integer',default=0) , Field('likes_sincelastupdate','integer',default=0),  Field('checkins_sincelastupdate','integer',default=0),  Field('were_here_sincelastupdate','integer',default=0), Field('talking_about_sincelastupdate','integer',default=0),  Field('picture'), Field('team'))

fbpl.page.pageid.requires=IS_NOT_EMPTY()
fbpl.page.team.requires=IS_IN_SET(('連勝文','柯文哲','丁守中','顧立雄','All'))

fbpl.define_table('team_counts', Field('team'),Field('date_time', 'datetime'), Field('checkins','integer'),Field('likes','integer'),Field('were_here_count','integer'),Field('talking_about_count','integer'), Field('total_active_posts','integer'), Field('total_post_likes','integer'), Field('total_post_comments','integer'), Field('total_post_shares','integer'), 
Field('hour48_active_posts','integer'), Field('hour48_post_likes','integer'), Field('hour48_post_comments','integer'), Field('hour48_post_shares','integer'), Field('hour48_active_stories','integer'), Field('hour48_story_likes','integer'), Field('hour48_story_comments','integer'), Field('hour48_story_shares','integer'), Field('hour48_active_links','integer'), Field('hour48_link_likes','integer'), Field('hour48_link_comments','integer'), Field('hour48_link_shares','integer'), Field('hour48_active_videos','integer'), Field('hour48_video_likes','integer'), Field('hour48_video_comments','integer'), Field('hour48_video_shares','integer'))



fbpl.team_counts.team.requires=IS_IN_SET(('連勝文','柯文哲','丁守中','顧立雄','All'))

fbpl.define_table('page_insights' , Field('pageid'), Field('lifetime_likes'), Field('daily_people_talking'), Field('days28_people_talking'), Field('monthly_people_talking'), Field('end_time'), Field('location_insights'),Field('team'))


fbpl.define_table('place',Field('placeid', unique=True),Field('name'),Field('street'),Field('city'),Field('state'),Field('country'),Field('latitude', 'float'),Field('longitude','float'),Field('category'),Field('category_list','text'),Field('zip'),Field('link'),Field('website'),Field('phone'),Field('description'),Field('old_ids'),Field('mutiple'), format='%(placename)s')

#fbpl.place.placeid.requires=IS_NOT_EMPTY()

fbpl.place.placeid.requires=IS_NOT_EMPTY()
fbpl.place.name.requires=IS_NOT_EMPTY()
fbpl.place.latitude.requires=IS_NOT_EMPTY()
fbpl.place.longitude.requires=IS_NOT_EMPTY()
fbpl.place.category.requires=IS_NOT_EMPTY()
#fbpl.place.old_ids.requires=IS_IN_DB(fbpl, fbpl.social_counts.placeid)
fbpl.place.link.requires=IS_URL()

fbpl.define_table('social_counts', Field('placeid',fbpl.place),Field('date_time', 'datetime'), Field('checkins','integer'),Field('likes','integer'),Field('were_here_count','integer'),Field('talking_about_count','integer'), Field('updated_time') )

fbpl.social_counts.placeid.requires=IS_NOT_EMPTY()
fbpl.social_counts.placeid.requires=IS_IN_DB(fbpl, fbpl.place.placeid)
fbpl.social_counts.checkins.requires=IS_NOT_EMPTY()
fbpl.social_counts.likes.requires=IS_NOT_EMPTY()
fbpl.social_counts.were_here_count.requires=IS_NOT_EMPTY()


fbpl.define_table('graphAPI_Error', Field('placeid',fbpl.place),Field('date_time', 'datetime', default=request.now), Field('code'),Field('error_msg'))

fbpl.define_table('merged_place', Field('placeid',fbpl.place),Field('date_time', 'datetime', default=request.now), Field('merge_to'),Field('name'),Field('latitude'),Field('longitude'),Field('category'),Field('category_list','text'),Field('zip'),Field('link'),Field('old_ids'))

fbpl.define_table('update_log', Field('start_date_time', 'datetime', default=request.now),Field('end_date_time', 'datetime') )






fbpl.graphAPI_Error.placeid.requires=IS_NOT_EMPTY()

fbpl.merged_place.placeid.requires=IS_NOT_EMPTY()
fbpl.merged_place.merge_to.requires=IS_NOT_EMPTY()


# coding: utf8


fbpl.define_table('event',Field('eventid', unique=True),Field('description'),Field('end_time'), Field('timezone'), Field('location'), Field('name'), Field('ownerid'), Field('ownername'),Field('picture'), Field('privacy'), Field('start_time'), Field('ticket_uri'), Field('updated_time'), Field('venuename'),Field('venueid'), Field('country'), Field('city'), Field('state'), Field('street'), Field('zipcode') , Field('longitude'), Field('latitude'), Field('is_date_only'))

fbpl.define_table('event_counts', Field('eventid'), Field('date_time', 'datetime'), Field('invited_count','integer'), Field('attending_count','integer'), Field('maybe_count','integer'), Field('declined_count','integer'),Field('noreply_count','integer'), Field('updated_time'))
