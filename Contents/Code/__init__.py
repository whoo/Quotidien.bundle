TITLE = 'Quodien Plugin'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
ICON_SEARCH = 'icon-search.png'


####
#import pyquery
###############

url="http://tf1.fr/tmc/quotidien-avec-yann-barthes/"
tb=[]
video=[]

def Start():

    Log.Debug("Start Plugins")
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    #    HTTP.CacheTime = CACHE_1HOUR
    page = HTML.ElementFromURL(url,errors='ignore')
    for a in page.xpath("//a[@class='mosaic_link']"):
        h=a.get('href').split('/')
        gurl=  h[len(h)-1]
        if (gurl[:9] == "quotidien"):
            tb.append(gurl)

    for a in tb:
        item={}
        gurl=url+"videos/"+a
        item['title']=a
        page = HTML.ElementFromURL(gurl,errors='ignore')
        id=page.xpath("//div[@id='zonePlayer']")[0].get('data-src')[-8:]
        title=page.xpath("//title")[0].text
        item['id']=id
        item['title']=title
        item['url']="http://www.wat.tv/get/iphone/"+id+".m3u8"
        video.append(item)

    Log.Debug(video)
            





@handler('/video/quotidien', TITLE)
def MainMenu():
    Log.Debug('Star Main')
    oc = ObjectContainer(title1="Petit Journal")
    
    for a in video:
        tmp=VideoClipObject(
        key=Callback(Lookup, title=a['title'], thumb=R(ICON), rating_key=4, url=a['url'], art=R(ICON), summary=a['title'], tagline=""),
        url=a['url'],
        title=a['title'],
        summary=a['title'],
        thumb=R(ICON),
        items = [
                        MediaObject(parts = [PartObject(key=HTTPLiveStreamURL(Callback(PlayVideo, url=url)))],
                        optimized_for_streaming =False ,
                        )
                ]

        )
        oc.add(tmp)
    
    return oc

ObjectContainer.title1 = TITLE
ObjectContainer.view_group = 'List'
ObjectContainer.art = R(ART)



def Lookup(title, thumb, rating_key, url, art, summary, tagline):
    Log.Debug("Entering Lookup")
    Log.Debug("video %s"%url)
    oc = ObjectContainer()
    oc.add(
        VideoClipObject(
            key         = Callback(Lookup, title=title, thumb=thumb, rating_key=rating_key, url=url, art=art, summary=summary, tagline=tagline),
            title       = title,
            thumb       = thumb,
            tagline     = tagline,
            rating_key  = rating_key,
            summary     = summary,
            art     = art,
            items       = [
                    MediaObject(
                            parts = [PartObject(key=HTTPLiveStreamURL(Callback(PlayVideo, url=url)))],
                            optimized_for_streaming = False,
                    )
            ]
        )
    )

    return oc


@indirect
def PlayVideo(url):
        return IndirectResponse(VideoClipObject, key=HTTPLiveStreamURL(url))

