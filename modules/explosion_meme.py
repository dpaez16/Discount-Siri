from moviepy.editor import VideoFileClip, concatenate_videoclips

EXPLOSION_CLIP = "./static/explosion_clip.mp4"


def append_explosion_clip(video_file):
    clip1 = VideoFileClip(video_file)
    if clip1 is None:
        return None, "Could not open file!"

    clip2 = VideoFileClip(EXPLOSION_CLIP)
    final_clip = concatenate_videoclips([clip1, clip2])
    final_clip.write_videofile("./output.mp4")
    return "./output.mp4", ""
