from moviepy.editor import AudioFileClip, VideoFileClip




def main():
    print('Generating the full video...')
    video = r"C:\Users\HP\Desktop\youtube video downloader\v.webm"
    audio = r"C:\Users\HP\Desktop\youtube video downloader\a.webm"
    output_path_name = r"C:\Users\HP\Desktop\youtube video downloader\final.wav"

    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path_name, codec='libx264', audio_codec="aac")
    print('Full video is generated')


if __name__ == "__main__":
    main()




       elif extracted_data["vurl"] != "":
        with open(f"{data['title']}_audio.{extracted_data['ext']}", 'wb') as f:
            audio_ = requests.get(extracted_data["aurl"], stream=True)
            audio = audio_.content

        with open(f"{data['title']}.{extracted_data['ext']}", 'wb') as f:
            video_ = requests.get(extracted_data["vurl"], stream=True)
            video = video_.content

        print('Generating the full video...')
        output_path_name = f"C:\\Users\\HP\\Desktop\\youtube video downloader\\{data['title']}.mp4"
        video_clip = VideoFileClip(video)
        audio_clip = AudioFileClip(audio)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path_name, codec='libx264', audio_codec="aac")
        print('Full video is generated')