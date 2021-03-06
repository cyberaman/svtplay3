import mc

def category_to_list_item(item):
    list_item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    return list_item

def show_to_list_item(item):
    list_item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    if item["thumbnail_url"] != "http://www.svtplay.se/public/images/play_default_large.jpg":
        # Set thumbnail only if it is not the default svt image. UI can handle
        # it better when it can detect whether a real thumb exists or not.
        list_item.SetThumbnail(get_image_size(item["thumbnail_url"], "medium"))
        #list_item.SetIcon(get_image_size(item["thumbnail_url"], "medium")) # ListItem.Icon in UI shows the Thumbnail ...
    return list_item

def episode_to_list_item(item):
    if item["kind_of"] == 1: # EPISODE
        list_item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_EPISODE)
        list_item.SetProperty("episode", "true")
    else: # CLIP
        list_item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        list_item.SetProperty("clip", "true")
    if item["recommended"]: list_item.SetProperty("recommended", "true")
    if item["viewable_in"] == 1: list_item.SetProperty("viewable_in_world", "true")
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    list_item.SetPath(item["url"])
    list_item.SetDescription(item["description"], False)
    list_item.SetProperty("date_available_until", item["date_available_until"])
    list_item.SetProperty("date_broadcasted", item["date_broadcasted"])
    date_array = item["date_broadcasted"].split("T")[0].split("-")
    list_item.SetDate(int(date_array[0]),
                      int(date_array[1]),
                      int(date_array[2]))
    list_item.SetProperty("length", item["length"])
    duration_array = item["length"].split()
    duration = sum(map(parse_duration, zip(duration_array[1::2], duration_array[::2])))
    list_item.SetDuration(duration)
    info = "Längd: " + item["length"]
    info += "\nSändningsstart: " + item["date_broadcasted"].split("T")[0]
    info += "\nTillgänglig till och med " + item["date_available_until"].split("T")[0]
    info += {
        1: "\nTyp: Avsnitt",
        2: "\nTyp: Klipp"
    }[item["kind_of"]]
    info += {
        1: "\nKan ses i hela världen",
        2: "\nKan bara ses i Sverige"
    }[item["viewable_in"]]
    list_item.SetStudio(info)
    list_item.SetThumbnail(get_image_size(item["thumbnail_url"], "medium"))
    #list_item.SetIcon(get_image_size(item["thumbnail_url"], "medium")) # ListItem.Icon in UI shows the Thumbnail ...
    return list_item

def get_image_size(url, size):
    parts = url.split("/")
    if "ALTERNATES" in parts:
        size_position = parts.index("ALTERNATES") + 1
        parts[size_position] = size
    return "/".join(parts)

def parse_duration((identifier, value)):
    if identifier == "h":
        return int(value) * 3600
    if identifier == "min":
        return int(value) * 60
    if identifier == "sek":
        return int(value)

