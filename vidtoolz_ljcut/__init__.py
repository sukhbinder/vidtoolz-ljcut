import vidtoolz
from moviepy import (
    CompositeAudioClip,
    CompositeVideoClip,
    VideoFileClip,
    afx,
)
from vidtoolz.utils import determine_output_path


def j_cut(
    first_clip_path,
    second_clip_path,
    output_path,
    overlap_duration=1.0,
    duck_volume=0.35,
    audio_fade=0.25,
):
    clip_a = VideoFileClip(first_clip_path)
    clip_b = VideoFileClip(second_clip_path)

    overlap_duration = min(
        overlap_duration,
        clip_a.duration,
        clip_b.duration,
    )

    overlap_start = clip_a.duration - overlap_duration

    clip_b_video = clip_b.with_start(overlap_start)

    final_video = CompositeVideoClip(
        [
            clip_a,
            clip_b_video,
        ]
    )

    # Clip A audio (normal, full length)
    clip_a_audio = clip_a.audio

    # Duck ONLY during overlap by layering a reduced copy
    clip_a_audio_duck = (
        clip_a.audio.subclipped(overlap_start, clip_a.duration)
        .with_start(overlap_start)
        .with_effects(
            [
                afx.MultiplyVolume(duck_volume),
                afx.AudioFadeOut(audio_fade),
            ]
        )
    )

    # Clip B audio (starts early, fades in)
    clip_b_audio = clip_b.audio.with_start(overlap_start).with_effects(
        [
            afx.AudioFadeIn(audio_fade),
        ]
    )

    final_audio = CompositeAudioClip(
        [
            clip_a_audio,
            clip_a_audio_duck,
            clip_b_audio,
        ]
    )

    final = final_video.with_audio(final_audio)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
    )


# Example usage
# j_cut(
#     first_clip_path="IMG_9615.MOV",
#     second_clip_path="IMG_9613.MOV",
#     output_path="outputjcut.mp4",
#     overlap_duration=1.0,
#     duck_volume=0.3,
#     audio_fade=0.3,
# )


def l_cut(
    first_clip_path,
    second_clip_path,
    output_path,
    overlap_duration=1.0,
    audio_fade=0.3,
):
    """
    L-cut:
    - Video switches to clip B early
    - Audio from clip A continues after the cut
    """

    clip_a = VideoFileClip(first_clip_path)
    clip_b = VideoFileClip(second_clip_path)

    overlap_duration = min(
        overlap_duration,
        clip_a.duration,
        clip_b.duration,
    )

    # Clip B video starts BEFORE clip A audio ends
    clip_b_video_start = clip_a.duration - overlap_duration
    clip_b_video = clip_b.with_start(clip_b_video_start)

    final_video = CompositeVideoClip(
        [
            clip_a,
            clip_b_video,
        ]
    )

    # Clip A audio continues AFTER video cut
    clip_a_audio = clip_a.audio.with_effects(
        [
            afx.AudioFadeOut(audio_fade),
        ]
    )

    # Clip B audio starts normally (at video cut)
    clip_b_audio = clip_b.audio.with_start(clip_b_video_start)

    final_audio = CompositeAudioClip(
        [
            clip_a_audio,
            clip_b_audio,
        ]
    )

    final = final_video.with_audio(final_audio)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
    )


# l_cut(
#     first_clip_path="IMG_9615.MOV",
#     second_clip_path="IMG_9613.MOV",
#     output_path="outputlcut.mp4",
#     overlap_duration=2.0,
#     # duck_volume=0.3,
#     audio_fade=0.3,
# )


def create_parser(subparser):
    parser = subparser.add_parser("jcut", description="L-cut J-cut using moviepy")
    # Add subprser arguments here.
    parser.add_argument("input", help="Input video file (e.g., input.mp4)")
    parser.add_argument(
        "--output",
        default=None,
        help="Output video file name (default: output_overlay.mp4)",
    )
    return parser


class ViztoolzPluginJcut:
    """L-cut J-cut using moviepy"""

    __name__ = "jcut"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # add actual call here
        output_file = determine_output_path(args.input, args.output, "jcut")
        pass

    def hello(self, args):
        # this routine will be called when "vidtoolz "jcut is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


class ViztoolzPluginLcut:
    """L-cut J-cut using moviepy"""

    __name__ = "lcut"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # add actual call here
        output_file = determine_output_path(args.input, args.output, "lcut")
        lcut()
        pass

    def hello(self, args):
        # this routine will be called when "vidtoolz "jcut is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


jcut_plugin = ViztoolzPluginJcut()
lcut_plugin = ViztoolzPluginLcut()
