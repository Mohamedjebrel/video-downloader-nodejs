import requests, time, sys, os
from moviepy.editor import AudioFileClip, VideoFileClip


### global variables ###
a_total_size_in_bytes = 0
v_total_size_in_bytes = 0

achunk_length = 0
vchunk_length = 0


### functions ###
# getting data
def get_data(entry):
    entry = str(entry)
    if "list=" in entry:
        playlist_id = entry.split("list=")[1]
        is_playlist = 1
    else:
        is_playlist = 0

    url = "https://en.fetchfile.net/fetch/"
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01','accept-encoding': 'gzip, deflate, br','accept-language': 'en,en-US;q=0.9,ar;q=0.8','content-length': '95','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','origin': 'https://en.fetchfile.net','referer': f'https://en.fetchfile.net/?url={entry}','sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','same-origin': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    data = {"url":entry, "action": "homePure"}
    response = requests.post(url, data=data, headers=headers)
    return [response, is_playlist]
        
        
# handling data
def handler(response):
    all_formats = []
    if "formats" in response:
        for format in response["formats"]:
            fmt = {"format":format["format"].split("- ")[1], 
                    "filesize":f'{round(format["filesize"]/(1024*1024*1024), 1)} G' if format["filesize"] and (format["filesize"]/(1024*1024))>1024  else f'{round(format["filesize"]/(1024*1024), 1)} M' if format["filesize"] and (format["filesize"]/(1024*1024))<1024 else "",
                    "ext":format["ext"],
                    "url":format["url"]
                    }
            all_formats.append(fmt)

        new_data = {"title":response["title"],
                    "webpage_url":response["webpage_url"],
                    "view_count":f'{response["view_count"]:,d}',
                    "average_rating":round(int(response["average_rating"]),1), 
                    "categories":response["categories"],
                    "channel":response["channel"],
                    "channel_url":response["channel_url"],
                    "dislike_count":f'{response["dislike_count"]:,d}' if "dislike_count" in response else 0,
                    "like_count":f'{response["like_count"]:,d}' if "like_count" in response else 0,
                    "thumbnail":response["thumbnail"],
                    "duration":f'{round(int(response["duration"]))} sec' if round(int(response["duration"])/60) < 1 else f'{round(int(response["duration"])/60, 1)} min' if round(int(response["duration"])/60) >= 1 | round(int(response["duration"])/60) < 60 else f'{round(int(response["duration"])/(60*60), 1)} hr' if round(int(response["duration"])/60) >= 60 else f'{round(int(response["duration"])/(60), 1)} min',
                    "formats":all_formats
                    }
        return new_data

    elif "entries" in response:
        for format in response["entries"][0]["formats"]:
            fmt = {"format":format["format"].split("- ")[1], 
                    "filesize":f'{round(format["filesize"]/(1024*1024*1024),1)} G' if format["filesize"] and (format["filesize"]/(1024*1024))>1024  else f'{round(format["filesize"]/(1024*1024), 1)} M' if format["filesize"] and (format["filesize"]/(1024*1024))<1024 else "",
                    "ext":format["ext"],
                    "url":format["url"]
                    }
            all_formats.append(fmt)
    
        new_data = {"title":response["entries"][0]["title"],
                    "webpage_url":response["entries"][0]["webpage_url"],
                    "view_count":f'{response["entries"][0]["view_count"]:,d}',
                    "average_rating":round(int(response["entries"][0]["average_rating"]),1), 
                    "categories":response["entries"][0]["categories"],
                    "channel":response["entries"][0]["channel"],
                    "channel_url":response["entries"][0]["channel_url"],
                    "dislike_count":f'{response["entries"][0]["dislike_count"]:,d}' if "dislike_count" in response["entries"][0] else 0,
                    "like_count":f'{response["entries"][0]["like_count"]:,d}' if "like_count" in response["entries"][0] else 0,
                    "thumbnail":response["entries"][0]["thumbnail"],
                    "duration":f'{round(int(response["entries"][0]["duration"]))} sec' if round(int(response["entries"][0]["duration"])/60) < 1 else f'{round(int(response["entries"][0]["duration"])/60, 1)} min' if round(int(response["entries"][0]["duration"])/60) >= 1 | round(int(response["entries"][0]["duration"])/60) < 60 else f'{round(int(response["entries"][0]["duration"])/(60*60), 1)} hr' if round(int(response["entries"][0]["duration"])/60) >= 60 else f'{round(int(response["entries"][0]["duration"])/(60), 1)} min',
                    "formats":all_formats
                    }
        return new_data

def checkURL(user_input):
    while True:
        data = get_data(user_input)
        response = get_data(user_input)[0]
        if response.status_code==200:
            response = response.json()
            if "status" in response:
                if response["status"] == "wait":
                    print("wait response during fetching url. Retrying...")
                    time.sleep(1)
                    pass
            else:
                print("Data Ready! handling...")
                global final_data
                final_data = handler(response)
                print("Data Handled!")
                return {"status":1, "data":final_data, "is_playlist":data[1]}
                break

def downloadFile(user_option, data) :
    # extracting the url
    def extract_data():
        selected_option = user_option.split(",")
        for format in data["formats"]:
            if selected_option[0] in format["ext"] and selected_option[1] in format["format"] and selected_option[2] in format["filesize"] :
                if "audio" in selected_option[1]:
                    type = "audio"
                    aurl = data["formats"][0]["url"]
                    vurl = ""
                    return {"aurl":aurl, "vurl":vurl, "ext":format["ext"], "type":type}
                else:
                    type = "video"
                    aurl = data["formats"][0]["url"]
                    vurl = format["url"]
                    return {"aurl":aurl, "vurl":vurl, "ext":format["ext"], "type":type}
            else:
                pass
        return "invalid user input!"

    extracted_data = extract_data()      
    if extracted_data["vurl"] == "":
        with open(f"{data['title']}.{extracted_data['ext']}", 'wb') as f:
            r = requests.get(extracted_data["aurl"], stream=True)
            print("Downloading Audio...")
            f.write(r.content)
            print('Audio is downloaded')

    elif extracted_data["vurl"] != "":

        audio = requests.get(extracted_data["aurl"], stream=True)
        a_total_size_in_bytes= int(audio.headers.get('content-length', 0))
        block_size = 1024 * 1024 #1 Mb
        global achunk_length
        print("Downloading Audio...")
        with open(f"{data['title']}_audio.{extracted_data['ext']}", 'wb') as f:
            for achunk in audio.iter_content(block_size):
                achunk_length = achunk_length + len(achunk)
                f.write(achunk)


        video = requests.get(extracted_data["vurl"], stream=True)
        v_total_size_in_bytes= int(video.headers.get('content-length', 0))
        block_size = 1024 * 1024 #1 Mb
        global vchunk_length
        print("Downloading Video...")
        with open(f"{data['title']}_video.{extracted_data['ext']}", 'wb') as f:
            for vchunk in video.iter_content(block_size):
                vchunk_length = vchunk_length + len(vchunk)
                f.write(vchunk)

        # collecting and forming the final video
        print('Generating the full video...')
        video = f"{data['title']}_video.{extracted_data['ext']}"
        audio = f"{data['title']}_audio.{extracted_data['ext']}"
        output_path_name = f"C:\\Users\\HP\\Desktop\\youtube video downloader\\{data['title']}.mp4"
        video_clip = VideoFileClip(video)
        audio_clip = AudioFileClip(audio)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path_name, codec='libx264', audio_codec="aac")
        # deleting old files
        os.remove(f"{data['title']}_video.{extracted_data['ext']}")
        os.remove(f"{data['title']}_audio.{extracted_data['ext']}")
        print('Full video is generated')

def download_progress():
    total_files_size_in_Mb = (a_total_size_in_bytes + v_total_size_in_bytes)/(1024 * 1024)
    total_downloaded_in_Mb = achunk_length + vchunk_length

    progress = (total_downloaded_in_Mb / total_files_size_in_Mb) * 100
    return progress