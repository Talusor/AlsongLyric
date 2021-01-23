from alsong.lyrics import GetLyricList, GetLyric

lyrics = GetLyricList("곡예사")

if len(lyrics) != 0:
    for i in lyrics:
        print(i["title"] + " / " + i["lyricId"])
    lyric = GetLyric(lyrics[0]["lyricId"])
    print(lyric)