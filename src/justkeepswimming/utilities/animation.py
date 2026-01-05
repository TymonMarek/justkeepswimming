import enum
import logging

from pygame import Surface

from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.image import Frame, Image
from justkeepswimming.utilities.signal import Signal


class Keyframe:
    def __init__(self, timestamp: float, region: Frame) -> None:
        self.timestamp: float = timestamp
        self.region: Frame = region


class AnimationPriority(enum.Enum):
    RESERVED = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0


class KeyframeSequence:
    def __init__(self, keyframes: list[Keyframe]) -> None:
        self.keyframes: list[Keyframe] = sorted(
            keyframes, key=lambda keyframe: keyframe.timestamp
        )
        self.duration: float = max(keyframe.timestamp for keyframe in self.keyframes)

    def reverse(self) -> "KeyframeSequence":
        reversed_keyframes = [
            Keyframe(self.duration - keyframe.timestamp, keyframe.region)
            for keyframe in reversed(self.keyframes)
        ]
        return KeyframeSequence(reversed_keyframes)


class Animation:

    def __init__(
        self,
        image: Image,
        priority: AnimationPriority,
        looped: bool,
        speed: float,
        sequence: KeyframeSequence,
    ) -> None:
        self.image: Image = image
        self.sequence: KeyframeSequence = sequence
        self.priority: AnimationPriority = priority
        self.looped: bool = looped
        self.speed: float = speed


class AnimationType(enum.Enum):
    IDLE = enum.auto()
    WALK = enum.auto()
    ATTACK = enum.auto()
    HURT = enum.auto()
    DEATH = enum.auto()


class AnimationTrackState(enum.Enum):
    STOPPED = enum.auto()
    PLAYING = enum.auto()
    PAUSED = enum.auto()
    FINISHED = enum.auto()
    CANCELLED = enum.auto()


class AnimationTrack:
    def __init__(self, animator: "Animator", animation: Animation) -> None:
        self.animation: Animation = animation
        self.state: AnimationTrackState = AnimationTrackState.STOPPED
        self.logger = logging.getLogger("AnimationTrack")
        self.priority: AnimationPriority = animation.priority
        self.looped: bool = animation.looped
        self.speed: float = animation.speed

        self.animator: Animator = animator
        self.frames: dict[float, Surface] = {}
        self.on_playing = Signal()
        self.on_looped = Signal()
        self.on_finished = Signal()
        self.time: float = 0.0

    async def load(self) -> None:
        for keyframe in self.animation.sequence.keyframes:
            frame_surface = await keyframe.region.slice(self.animation.image)
            self.frames[keyframe.timestamp] = frame_surface
        self.logger.debug(
            f"Loaded animation track for animation with {len(self.frames)} frames."
        )

    async def get_current_frame(self) -> Surface | None:
        if not self.frames:
            return None
        keyframes = self.animation.sequence.keyframes
        for index in range(len(keyframes) - 1):
            start_keyframe = keyframes[index]
            end_keyframe = keyframes[index + 1]
            if start_keyframe.timestamp <= self.time < end_keyframe.timestamp:
                return self.frames[start_keyframe.timestamp]

    async def play(self) -> None:
        if self.state == AnimationTrackState.PLAYING:
            return
        self.state = AnimationTrackState.PLAYING
        self.time = 0.0
        await self.on_playing.emit(self)

    async def pause(self) -> None:
        if self.state != AnimationTrackState.PLAYING:
            return
        self.state = AnimationTrackState.PAUSED

    async def stop(self) -> None:
        if self.state == AnimationTrackState.STOPPED:
            return
        self.state = AnimationTrackState.STOPPED
        self.time = 0.0

    async def cancel(self) -> None:
        if self.state == AnimationTrackState.CANCELLED:
            return
        self.state = AnimationTrackState.CANCELLED

    async def update(self, delta_time: float) -> None:
        if self.state != AnimationTrackState.PLAYING:
            return
        self.time += delta_time * self.speed
        if self.time > self.animation.sequence.duration:
            if self.looped:
                self.time = self.time % self.animation.sequence.duration
                await self.on_looped.emit(self)
            else:
                self.time = self.animation.sequence.duration
                self.state = AnimationTrackState.FINISHED
                await self.on_finished.emit(self)


class Animator:
    def __init__(self) -> None:
        self.tracks: dict[Animation, AnimationTrack] = {}
        self.logger = logging.getLogger("Animator")

    async def load_animation(self, animation: Animation) -> AnimationTrack:
        if animation in self.tracks:
            return self.tracks[animation]
        track = AnimationTrack(self, animation)
        await track.load()
        self.tracks[animation] = track
        return track

    async def get_current_frame(self) -> Surface | None:
        active_track = await self.get_active_track()
        if active_track is None:
            self.logger.debug("No active animation track found.")
            return None
        return await active_track.get_current_frame()

    async def get_active_track(self) -> AnimationTrack | None:
        if not self.tracks:
            return None
        active_track = max(
            self.tracks.values(),
            key=lambda track: track.priority.value,
        )
        return active_track

    async def update(self, tick: TickContext) -> None:
        for track in self.tracks.values():
            await track.update(tick.delta_time)
