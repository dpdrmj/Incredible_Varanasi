# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
def home():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.flash = "welcome to incredible varanasi"
    #mail.send(to=['mehuljain811@gmail.com'],
          #subject='hello',
          # If reply_to is omitted, then mail.settings.sender is used
          #reply_to='mehuljain811@gmail.com',
          #message='hi there')

    response.files.append(URL('static', 'css/background.css'))
    response.files.append(URL('static', 'css/grid.css'))
    return locals()

@auth.requires_login()
def bank():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "bank":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        bank_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="bank" order by rating desc')
    return locals()

@auth.requires_login()
def bank_place():
    #Note, auth.user refers to a copy of the user record stored in the session, so changing it does not affect the database record.
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
        auth.logout()
    response.files.append(URL('static', 'css/background_bank.css'))
    response.files.append(URL('static', 'css/box_bank.css'))
    response.files.append(URL('static', 'css/box_bank_contact.css'))
    postals = db(db.bank.ID_BK==request.args[0]).select()
    phones = db(db.bank_2.ID_BK_2==request.args[0]).select(db.bank_2.Phone_BK)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.bank.ID_BK==request.args[0]).update(Rating_BK=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()


@auth.requires_login()
def entertainment():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "entertainment":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])

    else:
        enter_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="entertainment" order by rating desc')
    return locals()

@auth.requires_login()
def enter_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_entertainment.css'))
    response.files.append(URL('static', 'css/box_entertainment.css'))
    postals = db(db.entertainment_hub.ID_EH==request.args[0]).select()
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False
    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()
    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.entertainment_hub.ID_EH==request.args[0]).update(Rating_EH=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()


@auth.requires_login()
def fuel_agency():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "fuel agency":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])

    else:
        fag_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="fuel agency" order by rating desc')
    return locals()

@auth.requires_login()
def fuelagency_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_fuelagency.css'))
    response.files.append(URL('static', 'css/box_fuel.css'))
    postals = db(db.fuel_agency.ID_FA==request.args[0]).select()
    x = db.fuel_agency(db.fuel_agency.ID_FA==request.args[0])
    affils = db(db.fuel_company.ID_FC==x.ID_FC_R).select()
    phones = db(db.fuel_agency_2.ID_FA_2==request.args[0]).select(db.fuel_agency_2.Phone_FA,distinct=True)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False
    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False
    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.fuel_agency.ID_FA==request.args[0]).update(Rating_FA=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()



@auth.requires_login()
def fuel_company():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    if check_form.accepted:
        t=form.components[0]
        fc_rows = db(db.place_distance.place2==t).select(db.place_distance.place1,db.place_distance.distance,orderby = db.place_distance.distance)
        #hrei_near_rows = db.executesql('select place1,distance from place_distance where place2=selected_place order by distance')
    else:
        fc_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="fuel company" order by rating desc')
    return locals()


@auth.requires_login()
def fuelcompany_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_fuelcompany.css'))
    response.files.append(URL('static', 'css/box_fuel.css'))
    postals = db(db.fuel_company.ID_FC==request.args[0]).select()
    
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    return locals()

@auth.requires_login()
def handloom():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "handloom":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])

    else:
        hand_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="handloom" order by rating desc')
    return locals()

@auth.requires_login()
def handloom_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_handloom.css'))
    response.files.append(URL('static', 'css/box_handloom.css'))
    postals = db(db.local_handlooms.ID_LH==request.args[0]).select()
    phones = db(db.local_handlooms_2.ID_LH_2==request.args[0]).select(db.local_handlooms_2.Phone_LH)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.local_handlooms.ID_LH==request.args[0]).update(Rating_LH=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()




@auth.requires_login()
def heritage():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()    
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "heritage":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])

    else:
        hrei_rows = db.executesql('select Place_Name as place1,rating,Place_ID from places where Place_Type="heritage" order by rating desc')
    return locals()

@auth.requires_login()
def heri_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_heritage.css'))
    response.files.append(URL('static', 'css/box_heritage.css'))
    #postal = db.heritage_areas(request.args)
    #posts = db.executesql('select * from heritage_areas where ID_HA="ha1"')
    postals = db(db.heritage_areas.ID_HA==request.args[0]).select()
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.heritage_areas.ID_HA==request.args[0]).update(Rating_HA=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()





@auth.requires_login()
def hotel():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "hotel":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])

    else:
        hotel_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="hotel" order by rating desc')
    return locals()

@auth.requires_login()
def hotel_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_hotel.css'))
    response.files.append(URL('static', 'css/box_entertainment.css'))
    postals = db(db.hotels.ID_HT==request.args[0]).select()
    phones = db(db.hotels_2.ID_HT_2==request.args[0]).select(db.hotels_2.Phone_HT)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.hotels.ID_HT==request.args[0]).update(Rating_HT=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()


@auth.requires_login()
def recreation():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "recreation":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        rec_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="recreation" order by rating desc')
    return locals()

@auth.requires_login()
def recreat_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_recreation.css'))
    response.files.append(URL('static', 'css/box_entertainment.css'))
    postals = db(db.recreation_hub.ID_RH==request.args[0]).select()
    
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.recreation_hub.ID_RH==request.args[0]).update(Rating_RH=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()




@auth.requires_login()
def restaurant():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "restaurant":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        restaur_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="restaurant" order by rating desc')
    return locals()

@auth.requires_login()
def restaur_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_restaurant.css'))
    response.files.append(URL('static', 'css/box_fuel.css'))
    postals = db(db.restaurant.ID_RS==request.args[0]).select()
    phones = db(db.restaurant_2.ID_RS_2==request.args[0]).select(db.restaurant_2.Phone_RS)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.restaurant.ID_RS==request.args[0]).update(Rating_RS=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()


@auth.requires_login()
def spiritual():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "spiritual":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        spirit_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="spiritual" order by rating desc')
    return locals()

@auth.requires_login()
def spirit_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_spiritual.css'))
    response.files.append(URL('static', 'css/box_spiritual.css'))
    postals = db(db.spiritual_hub.ID_SH==request.args[0]).select()
    
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.spiritual_hub.ID_SH==request.args[0]).update(Rating_SH=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()


@auth.requires_login()
def taxi_service():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "taxi service":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        taxi_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="taxi service" order by rating desc')
    return locals()

@auth.requires_login()
def taxi_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_taxiservice.css'))
    response.files.append(URL('static', 'css/box_taxiservice.css'))
    postals = db(db.taxi_service.ID_TS==request.args[0]).select()
    phones = db(db.taxi_service_2.ID_TS_2==request.args[0]).select(db.taxi_service_2.Phone_TS,distinct=True)
    carprices = db(db.taxi_service_2.ID_TS_2==request.args[0]).select(db.taxi_service_2.Car_Price_TS,distinct=True)
    cartypes = db(db.taxi_service_2.ID_TS_2==request.args[0]).select(db.taxi_service_2.Car_Types_TS,distinct=True)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.taxi_service.ID_TS==request.args[0]).update(Rating_TS=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()

@auth.requires_login()
def travel_agency():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    #hrei_rows = db(db.places.place_type=="heritage").select(orderby = ~db.places.rating)
    form = SQLFORM.factory(Field('Current_Location', requires=IS_IN_DB(db, 'places.place_name', '%(place_name)s')))
    check_form = form.process()
    t=1
    t1=[]
    t3=[]
    x = []
    re=""
    i =0
    if check_form.accepted:
        t=form.vars.Current_Location
        t1=db(db.places.place_name==t).select(db.places.Place_ID,db.places.place_type)
        for t2 in t1:
            re = t2.place_type
            enter_rows = db(db.place_distance.place2==t2.Place_ID).select(db.place_distance.place1,db.place_distance.place2,db.place_distance.distance,orderby = db.place_distance.distance)
        #ds = db(enter_rows).select(enter_rows[0],orderby = enter_rows[1])
        ty = db.executesql('select * from places join place_distance on places.Place_ID=place_distance.place1')
        for ent in enter_rows:
            for tr in ty:
               if ent.place1==tr[4] and ent.place2==tr[7]:
                    if tr[2] == "travel agency":
                        xa = tr[1]
                        xb = tr[3]
                        xc = tr[8]
                        xd = tr[4]
                        x.append([xa,xb,xc,xd])
    else:
        travel_rows = db.executesql('select place_name,rating,Place_ID from places where place_type="travel agency" order by rating desc')
    return locals()

@auth.requires_login()
def travel_place():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    response.files.append(URL('static', 'css/background_travelagency.css'))
    response.files.append(URL('static', 'css/box_fuel.css'))
    postals = db(db.travel_agency.ID_TA==request.args[0]).select()
    phones = db(db.Travel_Agency_2.ID_TA_2==request.args[0]).select(db.Travel_Agency_2.Phone_TA,distinct = True)
    tour_package = db(db.Travel_Agency_2.ID_TA_2==request.args[0]).select(db.Travel_Agency_2.Tour_Package_TA,distinct = True)
    db.visit_places.Place_ID.default = request.args[0]
    db.visit_places.Place_ID.readable = False
    db.visit_places.Place_ID.writable = False

    db.visit_places.RU_ID_Place.readable = False
    db.visit_places.RU_ID_Place.writable = False

    form = SQLFORM(db.visit_places).process()
    comments = db(db.visit_places.Place_ID==request.args[0]).select()

    db.visit_places.RU_ID_Place.default = db.visit_places.created_by
    if form.accepted:
        if len(comments)!=0:
            sume=0
            for commente in comments:
                sume+= (commente.User_Rating_Place)
                db(db.travel_agency.ID_TA==request.args[0]).update(Rating_TA=sume/len(comments))
                db(db.places.Place_ID==request.args[0]).update(rating=sume/len(comments))
    return locals()





def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #rows = db(db.blog_post).select()
    #response.flash = T("Welcome to Incredible Varanasi")
    redirect(URL('home'))
    return locals()

@auth.requires_login()
def comment():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    x = request.args[0]
    y = request.args[1]
    postals = db(db.visit_reply.post_id==x).select()
    db.visit_reply.post_id.default = x
    db.visit_reply.post_id.readable = False
    db.visit_reply.post_id.writable = False
    form = SQLFORM(db.visit_reply).process()

    if form.accepted:
        postals = db(db.visit_reply.post_id==request.args[0]).select()
    return locals()
    
def create():
    
    return locals()
def show():
    return "Team MADS"

def user():
    
    rpx = ''
    registerurl=URL('default','user',args='register',vars=dict(_next='/init/default/somepage'))
    if request.vars.token:
        auth.settings.login_form = rpxform
        return dict(form=auth())
    if 'login' in request.args:
        rpx = rpxform.login_form()
        html = DIV(H1('Login'),
               rpx,BR(),BR(),
               H1(A('Click here to register',
                       _href=registerurl),BR(),
                       'Or sign-in using your email and password'),
               auth(),
              )
    else:
        html = auth()

    return dict(form=html)
    return dict(form=auth())

@cache.action()
def edit_post_comment():
    if not db.auth_user[auth.user_id]:
        session.clear()
    elif auth.user and db.auth_user[auth.user_id].registration_key == 'blocked':
       auth.logout()
    id = request.args(0,cast=int)
    form = SQLFORM(db.visit_reply,id).process()
    return locals()

#def edit_post():
#    id = request.args(0,cast=int)
#    form = SQLFORM(db.visit_places,id).process()
#    return locals()

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


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
