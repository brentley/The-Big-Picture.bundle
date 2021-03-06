BP_PLUGIN_PREFIX   = "/photos/TheBigPicture"
PLUGIN_TITLE       = "The Big Picture"
BP_RSS_FEED        = "http://www.boston.com/bigpicture/index.xml"
NAMESPACES         = { "pheedo": "http://www.pheedo.com/namespace/pheedo" }

ART         = "art-default.jpg"
ICON        = "icon-default.png"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(BP_PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, ICON, ART)
  Plugin.AddViewGroup("ImageStream", viewMode="Pictures", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

  ObjectContainer.art       = R(ART)
  ObjectContainer.title1    = PLUGIN_TITLE
  ObjectContainer.view_group = "InfoList"
  DirectoryObject.thumb      = R(ICON)

####################################################################################################
def MainMenu():
  oc = ObjectContainer(view_group = "InfoList")
  feed = XML.ElementFromURL(BP_RSS_FEED)
  for item in feed.xpath("//rss//channel//item"):
    description = item.xpath(".//description")[0].text.replace('&gt;','>').replace('&lt','<')

    # If no thumb is provided, we can assume no photo is available. This has been found when a daily
    # post was not made, actually due to illness. :(
    try:
      thumb = HTML.ElementFromString(description).xpath(".//div[@class='bpImageTop']//img")[0].get('src')
    except: continue

    url = item.xpath(".//pheedo:origLink", namespaces = NAMESPACES)[0].text
    title = item.xpath(".//title")[0].text
    oc.add(PhotoAlbumObject(url=url, title=title, thumb=thumb))

  return oc