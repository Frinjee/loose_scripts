from moviepy import VideoFileClip, VideoClip, ImageClip, CompositeVideoClip, vfx

import random, string
import numpy as np

MAX_DURATION = 15
SHIFT_UP_PX = 50
INTRO_DURATION = 3
ON_INTERVAL = 1.2
REPEAT_INTERVAL = 2.7

video = VideoFileClip('assets/sweetiebabie.mp4')

end_time = min(MAX_DURATION, video.duration)

if hasattr(video, 'subclipped'):
    video = video.subclipped(0, end_time)
else:
    video = video.subclip(0, end_time) # pyright: ignore[reportAttributeAccessIssue]

frame = ImageClip('assets/overlay.png').with_duration(video.duration).with_fps(video.fps)

W, H = frame.size
vw, vh = video.size

x = (W-vw) // 2
y = (H-vh) // 2 - SHIFT_UP_PX

video = video.with_position((x, y))

glitter_fx = VideoFileClip('assets/glitter.mov', audio=False)

if glitter_fx.duration < video.duration:
    glitter_fx = glitter_fx.with_effects([vfx.Loop(duration=video.duration)])
else:
    if hasattr(glitter_fx, 'subclipped'):
        glitter_fx = glitter_fx.subclipped(0, video.duration)
    else:
        glitter_fx = glitter_fx.subclip(0, video.duration) # type: ignore

glitter_fx = glitter_fx.resized(frame.size).with_position((0, 0)) # type: ignore

mask = glitter_fx.to_mask().with_opacity(0.5) if hasattr(glitter_fx, 'with_opacity') else glitter_fx.to_mask().set_opacity(0.5)
glitter_fx = glitter_fx.with_mask(mask) if hasattr(glitter_fx, 'with_mask') else glitter_fx.set_mask(mask)

hearts_fx = VideoFileClip('assets/hearts_alpha.mov', audio=False)

if hearts_fx.duration < video.duration:
    hearts_fx = hearts_fx.with_effects([vfx.Loop(duration=video.duration)])
else:
    if hasattr(hearts_fx, 'subclipped'):
        hearts_fx = hearts_fx.subclipped(0, video.duration)
    else:
        hearts_fx = hearts_fx.subclip(0, video.duration) # type: ignore

hearts_fx = hearts_fx.resized(frame.size).with_position((0, 0)) # type: ignore


def hearts_gate(t):
    return 1.0 if (t % REPEAT_INTERVAL) < ON_INTERVAL else 0.0

hearts_fx_mask = VideoClip(
    frame_function=lambda t: np.ones((H, W), dtype=float) * hearts_gate(t),
    is_mask=True,
    duration=video.duration,
)

hearts_fx = hearts_fx.with_mask(hearts_fx_mask) if hasattr(hearts_fx, 'with_mask') else hearts_fx.set_mask(hearts_fx_mask)

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_out_back(t, s=1.4):
    t -= 1
    return 1 + t * t * ((s + 1) * t + s)

banner = ImageClip('assets/hvd-text.png', transparent=True).with_duration(video.duration)

def scale_at(t):
    if t < 0.5:
        u = t / 0.5
        return lerp(0.92, 1.00, ease_out_back(u))
    return 1.00 + 0.02 * (0.5 - abs(((t - 0.8) % 1.0) - 0.5))

banner = banner.resized(width=int(W* 0.76))

target_y = int(H * 0.04)
start_y = -banner.h

def pos_at(t):
    if t < 0.8:
        u = t / 0.8
        y = int(lerp(start_y, target_y, ease_out_back(u)))
    else:
        y = target_y
    return('center', y)

banner = banner.with_position(pos_at)

banner = banner.with_effects([
    vfx.FadeIn(0.35),
    vfx.FadeOut(0.6)
])

msg = ImageClip('assets/msg.png', transparent=True).with_duration(INTRO_DURATION)
msg = msg.resized(frame.size).with_position((0, 0))
msg = msg.with_effects([
    vfx.FadeIn(0.2),
    vfx.FadeOut(0.3)
])

main = CompositeVideoClip([video, frame, glitter_fx], size=frame.size)
main = CompositeVideoClip([main, banner], size=frame.size)
main = main.with_start(INTRO_DURATION).with_effects([vfx.FadeIn(0.6)])

total_duration = INTRO_DURATION + video.duration

suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
output_fName = f'output/sweetiebabie_edit_{suffix}.mp4'

final = CompositeVideoClip([msg, main], size=frame.size).with_duration(total_duration)
final.write_videofile(output_fName, codec='libx264', audio_codec='aac')